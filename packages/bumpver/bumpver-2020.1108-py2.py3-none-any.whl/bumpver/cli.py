#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This file is part of the pycalver project
# https://github.com/mbarkhau/pycalver
#
# Copyright (c) 2018-2020 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT
"""cli module for BumpVer."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import io
import sys
import typing as typ
import logging
import datetime as dt
import subprocess as sp
import click
import colorama
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import pkg_resources
str = getattr(builtins, 'unicode', str)
from . import vcs
from . import config
from . import rewrite
from . import version
from . import patterns
from . import regexfmt
from . import v1rewrite
from . import v1version
from . import v2rewrite
from . import v2version
from . import v1patterns
from . import v2patterns
try:
    import pretty_traceback
    pretty_traceback.install()
except ImportError:
    pass
click.disable_unicode_literals_warning = True
logger = logging.getLogger('bumpver.cli')
_VERBOSE = 0


def _configure_logging(verbose=0):
    global _VERBOSE
    _VERBOSE = verbose
    if verbose >= 2:
        log_format = (
            '%(asctime)s.%(msecs)03d %(levelname)-7s %(name)-17s - %(message)s'
            )
        log_level = logging.DEBUG
    elif verbose == 1:
        log_format = '%(levelname)-7s - %(message)s'
        log_level = logging.INFO
    else:
        log_format = '%(levelname)-7s - %(message)s'
        log_level = logging.INFO
    logging.basicConfig(level=log_level, format=log_format, datefmt=
        '%Y-%m-%dT%H:%M:%S')
    logger.debug('Logging configured.')


VALID_RELEASE_TAG_VALUES = 'alpha', 'beta', 'rc', 'post', 'final'
_current_date = dt.date.today().isoformat()


def _validate_date(date, pin_date):
    if date and pin_date:
        logger.error(
            "Can only use either --pin-date or --date='{0}', not both.".
            format(date))
        sys.exit(1)
    if date is None:
        return None
    try:
        dt_val = dt.datetime.strptime(date, '%Y-%m-%d')
        return dt_val.date()
    except ValueError:
        logger.error(
            "Invalid parameter --date='{0}', must match format YYYY-0M-0D."
            .format(date), exc_info=True)
        sys.exit(1)


def _validate_release_tag(tag):
    if tag is None:
        return
    if tag in VALID_RELEASE_TAG_VALUES:
        return
    logger.error('Invalid argument --tag={0}'.format(tag))
    logger.error('Valid arguments are: {0}'.format(', '.join(
        VALID_RELEASE_TAG_VALUES)))
    sys.exit(1)


def _validate_flags(raw_pattern, major, minor, patch):
    if '{' in raw_pattern and '}' in raw_pattern:
        return
    valid = True
    if major and 'MAJOR' not in raw_pattern:
        logger.error("Flag --major is not applicable to pattern '{0}'".
            format(raw_pattern))
        valid = False
    if minor and 'MINOR' not in raw_pattern:
        logger.error("Flag --minor is not applicable to pattern '{0}'".
            format(raw_pattern))
        valid = False
    if patch and 'PATCH' not in raw_pattern:
        logger.error("Flag --patch is not applicable to pattern '{0}'".
            format(raw_pattern))
        valid = False
    if not valid:
        sys.exit(1)


def _log_no_change(subcmd, version_pattern, old_version):
    msg = "Invalid version '{0}' and/or pattern '{1}'.".format(old_version,
        version_pattern)
    logger.error(msg)
    is_semver = ('{semver}' in version_pattern or 'MAJOR' in
        version_pattern and 'MAJOR' in version_pattern and 'PATCH' in
        version_pattern)
    if is_semver:
        logger.warning(
            'bumpver {0} [--major/--minor/--patch] required for use with SemVer.'
            .format(subcmd))
    else:
        available_flags = [('--' + part.lower()) for part in ['MAJOR',
            'MINOR', 'PATCH'] if part in version_pattern]
        if available_flags:
            available_flags_str = '/'.join(available_flags)
            logger.info('Perhaps try: bumpver {0} {1} '.format(subcmd,
                available_flags_str))


def _get_normalized_pattern(raw_pattern, version_pattern):
    is_version_pattern_required = ('{version}' in raw_pattern or 
        '{pep440_version}' in raw_pattern)
    if is_version_pattern_required and version_pattern is None:
        logger.error(
            'Argument --version-pattern=<PATTERN> is required for placeholders: {version}/{pep440_version}.'
            )
        sys.exit(1)
    elif version_pattern is None:
        _version_pattern = 'INVALID'
    else:
        _version_pattern = version_pattern
    if is_version_pattern_required:
        return v2patterns.normalize_pattern(_version_pattern, raw_pattern)
    else:
        return raw_pattern


verbose_option = click.option('-v', '--verbose', count=True, help=
    'Control log level. -vv for debug level.')
dry_option = click.option('-d', '--dry', default=False, is_flag=True, help=
    "Display diff of changes, don't rewrite files.")
fetch_option = click.option('-f/-n', '--fetch/--no-fetch', is_flag=True,
    default=True, help='Sync tags from remote origin.')


def version_options(function):
    decorators = [click.option('--major', is_flag=True, default=False, help
        ='Increment major component.'), click.option('-m', '--minor',
        is_flag=True, default=False, help='Increment minor component.'),
        click.option('-p', '--patch', is_flag=True, default=False, help=
        'Increment patch component.'), click.option('-t', '--tag', default=
        None, metavar='<NAME>', help=
        'Override release tag of current_version. Valid options are: {0}.'.
        format(', '.join(VALID_RELEASE_TAG_VALUES))), click.option(
        '--tag-num', is_flag=True, default=False, help=
        'Increment release tag number (rc1, rc2, rc3..).'), click.option(
        '--pin-date', is_flag=True, default=False, help=
        'Leave date components unchanged.'), click.option('--date', default
        =None, metavar='<ISODATE>', help=
        'Set explicit date in format YYYY-0M-0D (e.g. {0}).'.format(
        _current_date)), click.option('--set-version', default=None,
        metavar='<VERSION>', help='Set version explicitly.')]
    decorated = function
    for decorator in decorators:
        decorated = decorator(decorated)
    return decorated


@click.group()
@click.version_option(version='2020.1108')
@click.help_option()
@verbose_option
def cli(verbose=0):
    """Automatically update version strings in plaintext files."""
    if verbose:
        _configure_logging(verbose=max(_VERBOSE, verbose))


@cli.command()
@click.argument('old_version')
@click.argument('pattern')
@verbose_option
@version_options
def test(old_version, pattern, verbose=0, major=False, minor=False, patch=
    False, tag=None, tag_num=False, pin_date=False, date=None, set_version=None
    ):
    """Increment a version number for demo purposes."""
    _configure_logging(verbose=max(_VERBOSE, verbose))
    _validate_release_tag(tag)
    raw_pattern = pattern
    _validate_flags(raw_pattern, major, minor, patch)
    _date = _validate_date(date, pin_date)
    if set_version is None:
        new_version = incr_dispatch(old_version, raw_pattern=raw_pattern,
            major=major, minor=minor, patch=patch, tag=tag, tag_num=tag_num,
            pin_date=pin_date, date=_date)
    else:
        new_version = set_version
    if new_version is None:
        _log_no_change('test', raw_pattern, old_version)
        sys.exit(1)
    if not _is_valid_version(raw_pattern, old_version, new_version):
        if set_version:
            logger.error("Invalid argument --set-version='{0}'".format(
                set_version))
        sys.exit(1)
    pep440_version = version.to_pep440(new_version)
    click.echo('New Version: {0}'.format(new_version))
    if new_version != pep440_version:
        click.echo('PEP440     : {0}'.format(pep440_version))


def _grep_text(pattern, text, color):
    all_lines = text.splitlines()
    for match in pattern.regexp.finditer(text):
        match_start, match_end = match.span()
        line_idx = text[:match_start].count('\n')
        line_start = text.rfind('\n', 0, match_start) + 1
        line_end = text.find('\n', match_end, -1)
        if color:
            matched_line = text[line_start:match_start
                ] + colorama.Style.BRIGHT + text[match_start:match_end
                ] + colorama.Style.RESET_ALL + text[match_end:line_end]
        else:
            matched_line = text[line_start:match_start] + text[match_start:
                match_end] + text[match_end:line_end]
        lines_offset = max(0, line_idx - 1) + 1
        lines = all_lines[line_idx - 1:line_idx + 2]
        if line_idx == 0:
            lines[0] = matched_line
        else:
            lines[1] = matched_line
        prefixed_lines = ['{0:>4}: {1}'.format(lines_offset + i, line) for 
            i, line in enumerate(lines)]
        yield '\n'.join(prefixed_lines)


def _grep(raw_pattern, file_ios, color):
    pattern = v2patterns.compile_pattern(raw_pattern)
    match_count = 0
    for file_io in file_ios:
        text = file_io.read()
        match_strs = list(_grep_text(pattern, text, color))
        if len(match_strs) > 0:
            if len(file_ios) > 1:
                print(file_io.name)
            for match_str in match_strs:
                print(match_str)
            print()
        match_count += len(match_strs)
    if match_count == 0:
        logger.error("Pattern not found: '{0}'".format(raw_pattern))
    if match_count == 0 or _VERBOSE:
        pyexpr_regex = regexfmt.pyexpr_regex(pattern.regexp.pattern)
        print('# ' + regexfmt.regex101_url(pattern.regexp.pattern))
        print(pyexpr_regex)
        print()
    if match_count == 0:
        sys.exit(1)


@cli.command()
@verbose_option
@click.option('--version-pattern', default=None, metavar='<PATTERN>', help=
    'Pattern to use for placeholders: {version}/{pep440_version}')
@click.argument('pattern')
@click.argument('files', nargs=-1, type=click.File('r'))
def grep(pattern, files, version_pattern=None, verbose=0):
    """Search file(s) for a version pattern."""
    verbose = max(_VERBOSE, verbose)
    _configure_logging(verbose)
    raw_pattern = pattern
    normalized_pattern = _get_normalized_pattern(raw_pattern, version_pattern)
    isatty = getattr(sys.stdout, 'isatty', lambda : False)
    if isatty():
        colorama.init()
        try:
            _grep(normalized_pattern, files, color=True)
        finally:
            colorama.deinit()
    else:
        _grep(normalized_pattern, files, color=False)


@cli.command()
@verbose_option
@fetch_option
def show(verbose=0, fetch=True):
    """Show current version of your project."""
    _configure_logging(verbose=max(_VERBOSE, verbose))
    _, cfg = config.init(project_path='.')
    if cfg is None:
        logger.error(
            "Could not parse configuration. Perhaps try 'bumpver init'.")
        sys.exit(1)
    cfg = _update_cfg_from_vcs(cfg, fetch)
    click.echo('Current Version: {0}'.format(cfg.current_version))
    click.echo('PEP440         : {0}'.format(cfg.pep440_version))


def _colored_diff_lines(diff):
    for line in diff.splitlines():
        if line.startswith('+++') or line.startswith('---'):
            yield line
        elif line.startswith('+'):
            yield '\x1b[32m' + line + '\x1b[0m'
        elif line.startswith('-'):
            yield '\x1b[31m' + line + '\x1b[0m'
        elif line.startswith('@'):
            yield '\x1b[36m' + line + '\x1b[0m'
        else:
            yield line


def _v2_get_diff(cfg, new_version):
    old_vinfo = v2version.parse_version_info(cfg.current_version, cfg.
        version_pattern)
    new_vinfo = v2version.parse_version_info(new_version, cfg.version_pattern)
    return v2rewrite.diff(old_vinfo, new_vinfo, cfg.file_patterns)


def _v1_get_diff(cfg, new_version):
    old_vinfo = v1version.parse_version_info(cfg.current_version, cfg.
        version_pattern)
    new_vinfo = v1version.parse_version_info(new_version, cfg.version_pattern)
    return v1rewrite.diff(old_vinfo, new_vinfo, cfg.file_patterns)


def get_diff(cfg, new_version):
    if cfg.is_new_pattern:
        return _v2_get_diff(cfg, new_version)
    else:
        return _v1_get_diff(cfg, new_version)


def _print_diff_str(diff):
    colored_diff = '\n'.join(_colored_diff_lines(diff))
    if sys.stdout.isatty():
        click.echo(colored_diff)
    else:
        click.echo(diff)


def _print_diff(cfg, new_version):
    try:
        diff = get_diff(cfg, new_version)
        _print_diff_str(diff)
    except OSError as err:
        logger.error(str(err))
        sys.exit(1)
    except rewrite.NoPatternMatch as ex:
        logger.error(str(ex))
        sys.exit(1)


def _is_valid_version(raw_pattern, old_version, new_version):
    is_new_pattern = '{' not in raw_pattern and '}' not in raw_pattern
    try:
        if is_new_pattern:
            v2version.parse_version_info(new_version, raw_pattern)
        else:
            v1version.parse_version_info(new_version, raw_pattern)
    except version.PatternError:
        logger.error("Invalid version '{0}' for pattern '{1}'".format(
            new_version, raw_pattern))
        return False
    if pkg_resources.parse_version(new_version) <= pkg_resources.parse_version(
        old_version):
        logger.error(
            'Invariant violated: New version must be greater than old version '
            )
        logger.error("  Failed Invariant: '{0}' > '{1}'".format(new_version,
            old_version))
        return False
    else:
        return True


def incr_dispatch(old_version, raw_pattern, **kwargs):
    major = kwargs.get('major', False)
    minor = kwargs.get('minor', False)
    patch = kwargs.get('patch', False)
    tag = kwargs.get('tag', None)
    tag_num = kwargs.get('tag_num', False)
    pin_date = kwargs.get('pin_date', False)
    date = kwargs.get('date', None)
    v1_parts = list(v1patterns.PART_PATTERNS) + list(v1patterns.
        FULL_PART_FORMATS)
    has_v1_part = any('{' + part + '}' in raw_pattern for part in v1_parts)
    if _VERBOSE:
        if has_v1_part:
            pattern = v1patterns.compile_pattern(raw_pattern)
        else:
            pattern = v2patterns.compile_pattern(raw_pattern)
        logger.info('Using pattern ' + raw_pattern)
        logger.info('regex = ' + regexfmt.pyexpr_regex(pattern.regexp.pattern))
    if has_v1_part:
        new_version = v1version.incr(old_version, raw_pattern=raw_pattern,
            major=major, minor=minor, patch=patch, tag=tag, tag_num=tag_num,
            pin_date=pin_date, date=date)
    else:
        new_version = v2version.incr(old_version, raw_pattern=raw_pattern,
            major=major, minor=minor, patch=patch, tag=tag, tag_num=tag_num,
            pin_date=pin_date, date=date)
    return new_version


def _update(cfg, new_version, commit_message, allow_dirty=False):
    vcs_api = None
    if cfg.commit:
        try:
            vcs_api = vcs.get_vcs_api()
        except OSError:
            logger.warning('Version Control System not found, skipping commit.'
                )
    filepaths = set(cfg.file_patterns.keys())
    if vcs_api:
        vcs.assert_not_dirty(vcs_api, filepaths, allow_dirty)
    try:
        if cfg.is_new_pattern:
            new_v2_vinfo = v2version.parse_version_info(new_version, cfg.
                version_pattern)
            v2rewrite.rewrite_files(cfg.file_patterns, new_v2_vinfo)
        else:
            new_v1_vinfo = v1version.parse_version_info(new_version, cfg.
                version_pattern)
            v1rewrite.rewrite_files(cfg.file_patterns, new_v1_vinfo)
    except rewrite.NoPatternMatch as ex:
        logger.error(str(ex))
        sys.exit(1)
    if vcs_api:
        vcs.commit(cfg, vcs_api, filepaths, new_version, commit_message)


def _try_update(cfg, new_version, commit_message, allow_dirty=False):
    try:
        _update(cfg, new_version, commit_message, allow_dirty)
    except sp.CalledProcessError as ex:
        logger.error('Error running subcommand: {0}'.format(ex.cmd))
        if ex.stdout:
            sys.stdout.write(ex.stdout.decode('utf-8'))
        if ex.stderr:
            sys.stderr.write(ex.stderr.decode('utf-8'))
        sys.exit(1)


@cli.command()
@verbose_option
@dry_option
def init(verbose=0, dry=False):
    """Initialize [bumpver] configuration."""
    _configure_logging(verbose=max(_VERBOSE, verbose))
    ctx, cfg = config.init(project_path='.', cfg_missing_ok=True)
    if cfg:
        logger.error('Configuration already initialized in {0}'.format(ctx.
            config_rel_path))
        sys.exit(1)
    if dry:
        click.echo("Exiting because of '-d/--dry'. Would have written to {0}:"
            .format(ctx.config_rel_path))
        cfg_text = config.default_config(ctx)
        click.echo('\n    ' + '\n    '.join(cfg_text.splitlines()))
        sys.exit(0)
    config.write_content(ctx)


def get_latest_vcs_version_tag(cfg, fetch):
    all_tags = vcs.get_tags(fetch=fetch)
    if cfg.is_new_pattern:
        version_tags = [tag for tag in all_tags if v2version.is_valid(tag,
            cfg.version_pattern)]
    else:
        version_tags = [tag for tag in all_tags if v1version.is_valid(tag,
            cfg.version_pattern)]
    if version_tags:
        version_tags.sort(key=pkg_resources.parse_version, reverse=True)
        _debug_tags = ', '.join(version_tags[:3])
        logger.debug('found tags: {0} ... ({1} in total)'.format(
            _debug_tags, len(version_tags)))
        return version_tags[0]
    else:
        return None


def _update_cfg_from_vcs(cfg, fetch):
    latest_version_tag = get_latest_vcs_version_tag(cfg, fetch)
    if latest_version_tag is None:
        logger.debug('no vcs tags found')
        return cfg
    else:
        latest_version_pep440 = version.to_pep440(latest_version_tag)
        if latest_version_tag <= cfg.current_version:
            return cfg
        else:
            logger.info('Working dir version        : {0}'.format(cfg.
                current_version))
            logger.info('Latest version from VCS tag: {0}'.format(
                latest_version_tag))
            return cfg._replace(current_version=latest_version_tag,
                pep440_version=latest_version_pep440)


@cli.command()
@dry_option
@fetch_option
@verbose_option
@click.option('--allow-dirty', default=False, is_flag=True, help=
    'Commit even when working directory is has uncomitted changes. (WARNING: The commit will still be aborted if there are uncomitted to files with version strings.'
    )
@version_options
def update(dry=False, allow_dirty=False, fetch=True, verbose=0, major=False,
    minor=False, patch=False, tag=None, tag_num=False, pin_date=False, date
    =None, set_version=None):
    """Update project files with the incremented version string."""
    verbose = max(_VERBOSE, verbose)
    _configure_logging(verbose)
    _validate_release_tag(tag)
    _date = _validate_date(date, pin_date)
    _, cfg = config.init(project_path='.')
    if cfg is None:
        logger.error(
            "Could not parse configuration. Perhaps try 'bumpver init'.")
        sys.exit(1)
    cfg = _update_cfg_from_vcs(cfg, fetch)
    old_version = cfg.current_version
    if set_version is None:
        new_version = incr_dispatch(old_version, raw_pattern=cfg.
            version_pattern, major=major, minor=minor, patch=patch, tag=tag,
            tag_num=tag_num, pin_date=pin_date, date=_date)
    else:
        new_version = set_version
    if new_version is None:
        _log_no_change('update', cfg.version_pattern, old_version)
        sys.exit(1)
    if not _is_valid_version(cfg.version_pattern, old_version, new_version):
        if set_version:
            logger.error("Invalid argument --set-version='{0}'".format(
                set_version))
        sys.exit(1)
    logger.info('Old Version: {0}'.format(old_version))
    logger.info('New Version: {0}'.format(new_version))
    if dry or verbose >= 2:
        _print_diff(cfg, new_version)
    if dry:
        return
    commit_message_kwargs = {'new_version': new_version, 'old_version':
        old_version, 'new_version_pep440': version.to_pep440(new_version),
        'old_version_pep440': version.to_pep440(old_version)}
    commit_message = cfg.commit_message.format(**commit_message_kwargs)
    _try_update(cfg, new_version, commit_message, allow_dirty)


if __name__ == '__main__':
    cli()
