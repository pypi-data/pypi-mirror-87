# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
import os
from mercurial import (
    ui as uimod,
)

from .util import as_bytes


def make_ui(base_ui, config=None):
    # let's make sure we aren't polluted by surrounding settings
    os.environ['HGRCPATH'] = ''
    if base_ui is None:
        ui = uimod.ui.load()
    else:
        ui = base_ui.copy()

    # with load(), ui.environ is encoding.environ, with copy() it's not copied
    # we need the environ to be unique for each test to avoid side effects.
    # Also, on Python 2, encoding.environ is os.environ, leading to even
    # worse side effects.
    ui.environ = dict(ui.environ)

    # we want the most obscure calls to ui output methods to be executed
    # in tests. With the default settings, ui.note() early returns for example
    # meaning that only its arguments are tested, not what it does of them.
    ui.setconfig(b'ui', b'debug', b'yes')

    if config is not None:
        for section_name, section in config.items():
            for item_name, item_value in section.items():
                ui.setconfig(as_bytes(section_name),
                             as_bytes(item_name),
                             as_bytes(item_value),
                             source=b'tests')
    return ui
