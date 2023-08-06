# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from os.path import dirname
import hgext3rd.heptapod
HGEXT_HEPTA_SOURCE = dirname(hgext3rd.heptapod.__file__)


def common_config():
    """Return a configuration dict, prefilled with what we almost always need.

    Notably, it activates the present extension.
    """
    return dict(extensions=dict(heptapod=HGEXT_HEPTA_SOURCE,
                                topic='',
                                evolve='',
                                rebase='',
                                ))
