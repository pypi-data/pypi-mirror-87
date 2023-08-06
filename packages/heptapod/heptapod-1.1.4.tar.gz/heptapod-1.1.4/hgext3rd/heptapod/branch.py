# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Heptapod specific branch facilities.

Default GitLab branch:
  This a GitLab branch, e.g., ``branch/default`` rather than a Mercurial
  branch, e.g., ``default``.

  It is stored inside the repository directory, but not in the main store.
  In principle, different shares could have different default GitLab branches,
  if that were to be useful.

  For comparison, GitLab uses the value of `HEAD` on Git repositories for
  this.
"""
from mercurial.i18n import _
from mercurial import (
    hg,
    error,
)

DEFAULT_GITLAB_BRANCH_FILE_NAME = b'default_gitlab_branch'


def get_default_gitlab_branch(repo):
    """Return the default GitLab branch name, or ``None`` if not set."""
    branch = repo.vfs.tryread(DEFAULT_GITLAB_BRANCH_FILE_NAME)
    # (hg 5.4) tryread returns empty strings for missing files
    if not branch:
        return None
    return branch


def set_default_gitlab_branch(repo, target):
    if not target:
        raise error.Abort(_("The default GitLab branch cannot be an "
                            "empty string."))
    shared_from = hg.sharedreposource(repo)
    if shared_from is not None:
        repo = shared_from

    with repo.wlock():
        repo.vfs.write(DEFAULT_GITLAB_BRANCH_FILE_NAME, target)
