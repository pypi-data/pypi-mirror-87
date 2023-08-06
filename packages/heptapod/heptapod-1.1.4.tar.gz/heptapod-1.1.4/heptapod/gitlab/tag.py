# Copyright 2020 Sushil Khanchi <sushilkhanchi97@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Utilities and conventions for GitLab tags.
"""
GITLAB_TAG_REF_PREFIX = b'refs/tags/'


def gitlab_tag_ref(gitlab_tag):
    return GITLAB_TAG_REF_PREFIX + gitlab_tag
