# -*- coding: utf-8 -*-
# This file is part of the pretty-traceback project
# https://github.com/mbarkhau/pretty-traceback
#
# Copyright (c) 2020 Manuel Barkhau (mbarkhau@gmail.com) - MIT License
# SPDX-License-Identifier: MIT

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import os
import re
import sys
import types
import typing as typ
import logging
import traceback as tb
import subprocess as sp
import collections
import colorama
try:
    import builtins
except ImportError:
    import __builtin__ as builtins
import itertools
import pretty_traceback.common as com
str = getattr(builtins, 'unicode', str)
zip = getattr(itertools, 'izip', zip)


def _get_terminal_width():
    try:
        columns = int(os.environ['COLUMNS'])
        return columns
    except (KeyError, ValueError):
        pass
    if hasattr(os, 'get_terminal_size'):
        try:
            size = os.get_terminal_size(0)
            return size.columns
        except OSError:
            pass
    try:
        size_output = sp.check_output(['stty', 'size']).decode()
        _, columns = [int(val) for val in size_output.strip().split()]
        return columns
    except sp.CalledProcessError:
        pass
    except IOError:
        pass
    return 0


FMT_MODULE = (colorama.Fore.CYAN + colorama.Style.NORMAL + '{0}' + colorama
    .Style.RESET_ALL)
FMT_CALL = (colorama.Fore.YELLOW + colorama.Style.NORMAL + '{0}' + colorama
    .Style.RESET_ALL)
FMT_LINENO = (colorama.Fore.MAGENTA + colorama.Style.NORMAL + '{0}' +
    colorama.Style.RESET_ALL)
FMT_CONTEXT = '{0}'
FMT_ERROR_NAME = (colorama.Fore.RED + colorama.Style.BRIGHT + '{0}' +
    colorama.Style.RESET_ALL)
FMT_ERROR_MSG = colorama.Style.BRIGHT + '{0}' + colorama.Style.RESET_ALL
Row = typ.NamedTuple('Row', [('alias', str), ('short_module', str), (
    'full_module', str), ('call', str), ('lineno', str), ('context', str)])
PaddedRow = typ.NamedTuple('PaddedRow', [('alias', str), ('module', str), (
    'call', str), ('lineno', str), ('context', str)])
Alias = str
Prefix = str
AliasPrefixes = typ.List[typ.Tuple[Alias, Prefix]]
Context = typ.NamedTuple('Context', [('rows', typ.List[Row]), ('aliases',
    AliasPrefixes), ('max_row_width', int), ('is_wide_mode', bool), (
    'max_short_module_len', int), ('max_full_module_len', int), (
    'max_lineno_len', int), ('max_call_len', int), ('max_context_len', int)])


def _iter_entry_paths(entries):
    for entry in entries:
        module_abspath = os.path.abspath(entry.module)
        is_valid_abspath = module_abspath != entry.module and os.path.exists(
            module_abspath)
        if is_valid_abspath:
            yield module_abspath
        else:
            yield entry.module


TEST_PATHS = []
PWD = os.getcwd()


def _py_paths():
    if TEST_PATHS:
        return TEST_PATHS
    paths = list(sys.path)
    paths.sort(key=len, reverse=True)
    if '' in paths:
        paths.remove('')
    return paths


def _init_aliases(entry_paths):
    _uniq_entry_paths = set(entry_paths)
    alias_index = 0
    aliases = []
    for py_path in _py_paths():
        is_path_used = False
        for entry_path in list(_uniq_entry_paths):
            if entry_path.startswith(py_path):
                is_path_used = True
                _uniq_entry_paths.remove(entry_path)
        if not is_path_used:
            continue
        if py_path.endswith('site-packages'):
            alias = '<sitepkg>'
        elif py_path.endswith('dist-packages'):
            alias = '<distpkg>'
        elif re.search('lib/python\\d.\\d+$', py_path):
            alias = '<py>'
        elif re.search('lib/Python\\d.\\d+\\\\lib$', py_path):
            alias = '<py>'
        elif py_path.startswith(PWD):
            alias = '<pwd>'
            py_path = PWD
        else:
            alias = '<p{0}>'.format(alias_index)
            alias_index += 1
        aliases.append((alias, py_path))
    return aliases


def _iter_entry_rows(aliases, entry_paths, entries):
    for abs_module, entry in zip(entry_paths, entries):
        used_alias = ''
        module_full = abs_module
        module_short = abs_module
        module, call, lineno, context = entry
        if module.startswith('.' + os.sep):
            module = module[2:]
        if abs_module.endswith(module):
            for alias, alias_path in aliases:
                if not abs_module.startswith(alias_path):
                    continue
                new_module_short = abs_module[len(alias_path):]
                new_len = len(new_module_short) + len(alias)
                old_len = len(module_short) + len(used_alias)
                if new_len < old_len:
                    used_alias = alias
                    module_short = new_module_short
        yield Row(used_alias, module_short, module_full, call or '', lineno or
            '', context or '')


def _init_entries_context(entries, term_width=None):
    if term_width is None:
        _term_width = _get_terminal_width()
    else:
        _term_width = term_width
    entry_paths = list(_iter_entry_paths(entries))
    aliases = _init_aliases(entry_paths)
    max_row_width = _term_width - 10
    rows = list(_iter_entry_rows(aliases, entry_paths, entries))
    if rows:
        max_short_module_len = max(len(row.alias) + len(row.short_module) for
            row in rows)
        max_full_module_len = max(len(row.full_module) for row in rows)
        max_lineno_len = max(len(row.lineno) for row in rows)
        max_call_len = max(len(row.call) for row in rows)
        max_context_len = max(len(row.context) for row in rows)
    else:
        max_short_module_len = 0
        max_full_module_len = 0
        max_lineno_len = 0
        max_call_len = 0
        max_context_len = 0
    max_total_len = (max_full_module_len + max_lineno_len + max_call_len +
        max_context_len)
    is_wide_mode = max_total_len < max_row_width
    return Context(rows, aliases, max_row_width, is_wide_mode,
        max_short_module_len, max_full_module_len, max_lineno_len,
        max_call_len, max_context_len)


def _padded_rows(ctx):
    for row in ctx.rows:
        alias, module_short, module_full, call, lineno, context = row
        if ctx.is_wide_mode:
            alias = ''
            padded_module = module_full.ljust(ctx.max_full_module_len)
        else:
            padded_module = module_short.ljust(ctx.max_short_module_len -
                len(alias))
        if ctx.is_wide_mode:
            padded_call = call.ljust(ctx.max_call_len)
        else:
            padded_call = call.ljust(ctx.max_call_len)
        padded_lineno = lineno.rjust(ctx.max_lineno_len)
        yield PaddedRow(alias, padded_module, padded_call, padded_lineno,
            context)


def _aliases_to_lines(ctx, color=False):
    fmt_module = FMT_MODULE if color else '{0}'
    if ctx.aliases:
        alias_padding = max(len(alias) for alias, _ in ctx.aliases)
        for alias, path in ctx.aliases:
            yield '    ' + alias.ljust(alias_padding
                ) + ': ' + fmt_module.format(path)


def _rows_to_lines(rows, color=False):
    fmt_module = FMT_MODULE if color else '{0}'
    fmt_call = FMT_CALL if color else '{0}'
    fmt_lineno = FMT_LINENO if color else '{0}'
    fmt_context = FMT_CONTEXT if color else '{0}'
    for alias, module, call, lineno, context in rows:
        parts = '    ', alias, fmt_module.format(module
            ), '  ', fmt_call.format(call), '  ', fmt_lineno.format(lineno
            ), ': ', fmt_context.format(context)
        line = ''.join(parts)
        if alias:
            if alias == '<pwd>':
                line = line.replace(colorama.Style.NORMAL, colorama.Style.
                    BRIGHT)
        elif module.startswith(PWD):
            line = line.replace(colorama.Style.NORMAL, colorama.Style.BRIGHT)
        yield line


def _traceback_to_entries(traceback):
    summary = tb.extract_tb(traceback)
    for entry in summary:
        module = entry[0]
        call = entry[2]
        lineno = str(entry[1])
        context = entry[3]
        yield com.Entry(module, call, lineno, context)


def _format_traceback(ctx, traceback, color=False):
    padded_rows = list(_padded_rows(ctx))
    lines = []
    if ctx.aliases and not ctx.is_wide_mode:
        lines.append(com.ALIASES_HEAD)
        lines.extend(_aliases_to_lines(ctx, color))
    lines.append(com.TRACEBACK_HEAD)
    lines.extend(_rows_to_lines(padded_rows, color))
    if traceback.exc_name == 'RecursionError' and len(lines) > 100:
        prelude_index = 0
        line_counts = collections.defaultdict(int)
        for i, line in enumerate(lines):
            line_counts[line] += 1
            if line_counts[line] == 3:
                prelude_index = i
                break
        if prelude_index > 0:
            num_omitted = len(lines) - prelude_index - 2
            lines = lines[:prelude_index] + ['    ... {0} omitted lines'.
                format(num_omitted)] + lines[-2:]
    fmt_error_name = FMT_ERROR_NAME if color else '{0}'
    error_line = fmt_error_name.format(traceback.exc_name)
    if traceback.exc_msg:
        fmt_error_msg = FMT_ERROR_MSG if color else '{0}'
        error_line += ': ' + fmt_error_msg.format(traceback.exc_msg)
    lines.append(error_line)
    return os.linesep.join(lines) + os.linesep


def format_traceback(traceback, color=False):
    ctx = _init_entries_context(traceback.entries)
    return _format_traceback(ctx, traceback, color)


def format_tracebacks(tracebacks, color=False):
    traceback_strs = []
    for tb_tup in tracebacks:
        if tb_tup.is_caused:
            traceback_strs.append(com.CAUSE_HEAD + os.linesep)
        elif tb_tup.is_context:
            traceback_strs.append(com.CONTEXT_HEAD + os.linesep)
        traceback_str = format_traceback(tb_tup, color)
        traceback_strs.append(traceback_str)
    return os.linesep.join(traceback_strs).strip()


def exc_to_traceback_str(exc_value, traceback, color=False):
    tracebacks = []
    cur_exc_value = exc_value
    cur_traceback = traceback
    while cur_exc_value:
        next_cause = getattr(cur_exc_value, '__cause__', None)
        next_context = getattr(cur_exc_value, '__context__', None)
        tb_tup = com.Traceback(exc_name=type(cur_exc_value).__name__,
            exc_msg=str(cur_exc_value), entries=list(_traceback_to_entries(
            cur_traceback)), is_caused=bool(next_cause), is_context=bool(
            next_context))
        tracebacks.append(tb_tup)
        if next_cause:
            cur_exc_value = next_cause
            cur_traceback = getattr(next_cause, '__traceback__', None)
        elif next_context:
            cur_exc_value = next_context
            cur_traceback = getattr(next_context, '__traceback__', None)
        else:
            break
    tracebacks = list(reversed(tracebacks))
    return format_tracebacks(tracebacks, color)


class LoggingFormaterMixin(object):

    def formatException(self, ei):
        _, exc_value, traceback = ei
        return exc_to_traceback_str(exc_value, traceback, color=True)


class LoggingFormatter(LoggingFormaterMixin, logging.Formatter):
    pass
