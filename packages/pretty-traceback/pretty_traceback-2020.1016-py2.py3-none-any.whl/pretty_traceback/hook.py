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
import sys
import types
import typing as typ
import colorama
from pretty_traceback import formatting


def init_excepthook(color):

    def excepthook(exc_type, exc_value, traceback):
        tb_str = formatting.exc_to_traceback_str(exc_value, traceback, color)
        if color:
            colorama.init()
            try:
                sys.stderr.write(tb_str)
            finally:
                colorama.deinit()
        else:
            sys.stderr.write(tb_str)
    return excepthook


def install(envvar=None, color=True, only_tty=True,
    only_hook_if_default_excepthook=True):
    """Hook the current excepthook to the pretty_traceback.

    If you set `only_tty=False`, pretty_traceback will always
    be active even when stdout is piped or redirected.
    """
    if envvar and os.environ.get(envvar, '0') == '0':
        return
    isatty = getattr(sys.stderr, 'isatty', lambda : False)
    if only_tty and not isatty():
        return
    if not isatty():
        color = False
    is_default_exepthook = sys.excepthook == sys.__excepthook__
    if only_hook_if_default_excepthook and not is_default_exepthook:
        return
    sys.excepthook = init_excepthook(color=color)


def uninstall():
    """Restore the default excepthook."""
    sys.excepthook = sys.__excepthook__
