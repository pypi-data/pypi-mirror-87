# Copyright 2019 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from __future__ import absolute_import
from mercurial import (
    error,
)
import pytest

from ..testhelpers import RepoWrapper
from ..testhelpers import LocalRepoWrapper  # see test_compat_alis


parametrize = pytest.mark.parametrize


def test_write_commit_topic(tmpdir):
    """Demonstrate the use of write_commit with parent."""
    # it is essential to activate the rebase extension, even though
    # we don't use it in this test, because the
    # first loading of topic patches it only if it is present.
    # without this, all subsequent tests expecting rebase to preserve
    # topics would be broken
    wrapper = RepoWrapper.init(tmpdir,
                               config=dict(extensions=dict(rebase='',
                                                           topic='')))

    ctx0 = wrapper.write_commit('foo', content='Foo 0')
    wrapper.write_commit('foo', content='Foo 1')
    ctxbr = wrapper.write_commit('foo', content='Foo branch',
                                 parent=ctx0, topic='sometop')

    assert ctxbr.topic() == b'sometop'
    assert ctxbr.parents() == [ctx0]


def test_prune_update_hidden(tmpdir):
    wrapper = RepoWrapper.init(tmpdir,
                               config=dict(extensions=dict(evolve='')))
    wrapper.write_commit('foo', content='Foo 0')
    ctx = wrapper.write_commit('foo', content='Foo 1', return_ctx=True)
    wrapper.prune('.')
    assert ctx.obsolete()

    wrapper.update(0)
    assert tmpdir.join('foo').read() == 'Foo 0'

    with pytest.raises(error.FilteredRepoLookupError):
        wrapper.update(ctx.hex())

    wrapper.update_bin(ctx.node(), hidden=True)
    assert tmpdir.join('foo').read() == 'Foo 1'


def test_compat_alias(tmpdir):
    # that's enough to make flake8 happy and provides a strong
    # guarantee.
    assert RepoWrapper is LocalRepoWrapper
