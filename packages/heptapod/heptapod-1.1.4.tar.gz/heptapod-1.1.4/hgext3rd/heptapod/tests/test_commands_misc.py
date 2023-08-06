# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from __future__ import absolute_import

import json
from mercurial import (
    error,
    scmutil,
)
import pytest
import re

from heptapod.testhelpers import (
    RepoWrapper,
)
from .utils import common_config

from .. import (
    versions as hpd_versions,
)


def test_hpd_unique_successor(tmpdir, monkeypatch):
    repo_path = tmpdir.join('repo')
    wrapper = RepoWrapper.init(repo_path, config=common_config())
    ctx = wrapper.write_commit('foo', message="default0",
                               return_ctx=True)
    repo_path.join('foo').write('amend 1')
    wrapper.command('amend', message=b'amend1')
    repo_path.join('foo').write('amend 2')
    wrapper.command('amend', message=b'amend2')

    records = []

    def write(*args, **opts):
        records.append((args, opts))

    wrapper.repo.ui.write = write
    wrapper.command('hpd-unique-successor', rev=ctx.hex())
    out = records[0][0][0]

    succ_ctx = scmutil.revsingle(wrapper.repo, out)
    assert succ_ctx.description() == b'amend2'


def test_hpd_unique_successor_divergence(tmpdir, monkeypatch):
    repo_path = tmpdir.join('repo')
    config = common_config()
    config.setdefault('experimental', {})['evolution.allowdivergence'] = 'yes'
    wrapper = RepoWrapper.init(repo_path, config=config)
    ctx = wrapper.write_commit('foo', message="default0",
                               return_ctx=True)
    repo_path.join('foo').write('amend 1')
    wrapper.command('amend', message=b'amend1')

    # let's create the divergence
    wrapper.update(ctx.hex(), hidden=True)
    repo_path.join('foo').write('amend 2')
    wrapper.command('amend', message=b'amend2')

    with pytest.raises(error.Abort) as exc_info:
        wrapper.command('hpd-unique-successor', rev=ctx.hex())
    assert 'divergent' in exc_info.value.args[0]


def test_hpd_unique_successor_missing_rev(tmpdir, monkeypatch):
    repo_path = tmpdir.join('repo')
    wrapper = RepoWrapper.init(repo_path, config=common_config())

    with pytest.raises(error.Abort) as exc_info:
        wrapper.command('hpd-unique-successor')
    assert b'specify a revision' in exc_info.value.args[0]


def test_hpd_versions_with_hg_git(tmpdir, monkeypatch):
    # using RepoWrapper is pure lazyness on our part: they  give us the easiest
    # access to fully set up `ui` objects, with activated extensions
    config = common_config()
    config['extensions']['hggit'] = ''
    ui = RepoWrapper.init(tmpdir, config=config).repo.ui
    records = []

    def write(*args, **opts):
        assert all(isinstance(a, bytes) for a in args)
        records.append((args, opts))

    monkeypatch.setattr(ui, 'write', write)
    hpd_versions(ui)
    out = json.loads(records[0][0][0].decode())
    assert set(out.keys()) == {'python', 'mercurial',
                               'topic', 'hggit', 'evolve'}
    # for hggit it looks like: x.y.z (dulwich a.b.c)
    # for Mercurial, it can be just x.y
    version_re = re.compile(r'\d+[.]\d+([.]\d+)?')
    assert all(v is None or version_re.match(v) is not None
               for v in out.values())
    out.pop('hggit', None)  # hggit won't be shipped in some future
    assert all(v is not None for v in out.values())
