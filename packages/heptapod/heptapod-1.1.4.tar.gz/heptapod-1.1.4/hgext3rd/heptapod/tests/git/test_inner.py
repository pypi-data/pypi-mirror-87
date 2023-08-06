# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Inner tests for the Git subsystem.

These wouldn't really qualify as unit tests, since they exert at least
Mercurial, but they are more unitary and disposable than those of
test_integration, testing the implementation details of the Git subsystem.
"""
from __future__ import absolute_import

from mercurial import (
    error,
)
import pytest
import re

from dulwich.protocol import ZERO_SHA
from heptapod.testhelpers import (
    RepoWrapper,
)
from heptapod.gitlab import prune_reasons
from heptapod.gitlab.tag import gitlab_tag_ref
from ...git import (
    git_branch_ref,
    HeptapodGitHandler,
    GitRefChange as RefChange,  # will probably be renamed
)
from mercurial import pycompat
from ..utils import common_config

# TODO move to helper module
from .test_integration import patch_gitlab_hooks


def bkey(**d):
    """Replacement for `dict(k=v, ...)` that produces bytes keys"""
    return pycompat.byteskwargs(d)


def test_heptapod_gate_bookmarks(tmpdir):
    wrapper = RepoWrapper.init(tmpdir.join('repo'),
                               config=common_config())
    ctx = wrapper.write_commit('foo', content='foo0', message="default0",
                               return_ctx=True)

    repo = wrapper.repo
    handler = HeptapodGitHandler(repo, repo.ui)
    gate = handler.heptapod_gate_bookmarks

    assert len(gate(repo, True, {})) == 0

    def book_changes(**changes):
        """Readability helper because of bytes-everywhere"""
        # keys have to be byteified
        return {pycompat.sysbytes(book): change
                for book, change in changes.items()}

    with pytest.raises(error.Abort) as exc_info:
        gate(repo, False, book_changes(book1=(None, b'\x00\x01')))
    assert b'forbidden' in exc_info.value.args[0]
    assert b'book1' in exc_info.value.args[0]

    handler.map_set(gitsha=b'01ca34fe', hgsha=b'0001')
    deleted = gate(repo, False, book_changes(book1=(b'\x00\x01', None)))
    assert list(deleted) == [(b'book1', b'01ca34fe')]

    deleted = gate(repo, True, book_changes(book1=(None, ctx.node())))
    assert not deleted

    wrapper.command('topics', b'zetop')
    node = wrapper.write_commit('zz', message='topical')
    with pytest.raises(error.Abort) as exc_info:
        gate(repo, True, book_changes(book1=(None, node)))
    assert b'forbidden' in exc_info.value.args[0]
    assert b'topic' in exc_info.value.args[0]


def test_git_branch_for_branchmap_branch(tmpdir):
    wrapper = RepoWrapper.init(tmpdir.join('repo'))
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    gb = handler.git_branch_for_branchmap_branch

    assert gb(b'default') == b'branch/default'
    assert gb(b'default:zztop') == b'topic/default/zztop'

    with pytest.raises(error.Abort) as exc_info:
        assert gb(b'default:zz/top')
    assert b"Invalid character '/'" in exc_info.value.args[0]

    wrapper.repo.ui.setconfig(b'experimental',
                              b'hg-git.accept-slash-in-topic-name', True)

    assert gb(b'default:zz/top') == b'topic/default/zz-top'


def test_multiple_heads_choose_corner_case(tmpdir):
    wrapper = RepoWrapper.init(tmpdir.join('repo'))
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    assert handler.multiple_heads_choose((), 'branch name') is None


def test_multiple_heads_cannot_choose(tmpdir, monkeypatch):
    wrapper = RepoWrapper.init(tmpdir.join('repo'))
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)

    # repo being empty, choosing a head will certainly fail and return None
    gitlab_refs = {}
    handler.branchmap_entry_process_finalize(
        hg_shas=[b'012cafe34', b'663de1928'],
        gitlab_refs=gitlab_refs,
        gitlab_branch=b'branch/some',
        branchmap_branch=b'some',
        allow_multiple=True)

    # data inconsistency not propagated.
    assert not gitlab_refs


def test_notify_gitlab_empty_changes(tmpdir):
    wrapper = RepoWrapper.init(tmpdir.join('repo'))
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    assert handler.heptapod_notify_gitlab('some-hook', {}, {}) is None


def test_native_unknown_git_shas(tmpdir):
    wrapper = RepoWrapper.init(tmpdir.join('repo'),
                               config=dict(heptapod=dict(native="true")))
    wrapper.write_commit('foo', message='foo0')
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    hg_map = {b'known': b'cafe7654'}
    handler.map_hg_get = lambda k: hg_map.get(k)

    records = []

    def hook(*a):
        records.append(a)
        return 0, b'', b''

    ch = RefChange(b'topic/default/zetop', before=b'unknown', after=b'known')
    handler.heptapod_notify_gitlab(hook, {}, {b'topic/default/zetop': ch})

    _prune, changes = records[0][0]
    assert changes == {b'topic/default/zetop': (ZERO_SHA, b'cafe7654')}

    ch = RefChange(b'topic/default/zetop', before=b'known', after=b'unknown')
    with pytest.raises(error.Abort):
        handler.heptapod_notify_gitlab(hook, {}, {b'topic/default/zetop': ch})


def test_analyse_vanished_topic_lookup_error(tmpdir):
    wrapper = RepoWrapper.init(tmpdir.join('repo'))
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    unknown_sha = b'1234beef' * 5
    prune = handler.analyse_vanished_topic(
        b'default', b'zetop', unknown_sha,
        log_info=bkey(ref=b'refs/heads/topic/default/zetop',
                      before_git_sha=b'01234cafe'))
    assert prune == prune_reasons.HeadPruneReason()


def test_analyse_vanished_bogus_topic(tmpdir):
    wrapper = RepoWrapper.init(tmpdir.join('repo'))
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    assert handler.analyze_vanished_refs(
        {b'refs/heads/topic/missing-branch-name': b'ca1234fe',
         b'refs/heads/branch/default': 'will be completely ignored anyway'},
        {b'refs/heads/branch/default': 'will be completely ignored anyway'},
    ) == {}


def test_analyse_vanished_topic_draft_succ_unknown_reason(tmpdir):
    wrapper = RepoWrapper.init(tmpdir.join('repo'),
                               config=common_config())
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    wrapper.write_commit('foo', message='foo0')
    ctx = wrapper.write_commit('foo', message='in topic', topic='zzetop',
                               return_ctx=True)

    # Normally, analyse_vanished_topic works under the assumption that
    # the topic is not visible anymore. Yet feeding a visible topic
    # is the only currently known way of triggering the safety return
    # of before_sha for unknown situations

    prune = handler.analyse_vanished_topic(
        b'default', b'zzetop',
        ctx.hex(),
        log_info=bkey(ref='refs/heads/topic/default/zetop',
                      before_git_sha='01234cafe'))

    # TODO me way use a more precise reason later on
    assert prune == prune_reasons.HeadPruneReason()


def test_analyse_vanished_topic_latest_succ_not_found(tmpdir, monkeypatch):
    wrapper = RepoWrapper.init(tmpdir.join('repo'),
                               config=common_config())
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    wrapper.write_commit('foo', message='foo0')
    ctx = wrapper.write_commit('foo', message='in topic', topic='zzetop',
                               return_ctx=True)
    wrapper.command('amend', message=b'amended')
    wrapper.set_phase('public', ['.'])

    monkeypatch.setattr(handler, 'published_topic_latest_hg_sha',
                        lambda *a, **kw: None)

    prune = handler.analyse_vanished_topic(
        b'default', b'zzetop',
        ctx.hex(),
        log_info=bkey(ref='refs/heads/topic/default/zetop',
                      before_git_sha='01234cafe'))
    # TODO me way use a more precise reason later on
    assert prune == prune_reasons.HeadPruneReason()


def prepare_topic_divergence(tmpdir, additional_config=None):
    config = common_config()
    config['experimental'] = {'evolution.allowdivergence': 'yes'}
    if additional_config is not None:
        config.update(additional_config)
    repo_path = tmpdir.join('repo')
    wrapper = RepoWrapper.init(repo_path, config=config)

    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    wrapper.write_commit('foo', content='foo0', message="default0")
    ctx = wrapper.write_commit('foo', content='obs', message="to obsolete",
                               return_ctx=True)

    # create a content divergence
    repo_path.join('foo').write('amend1')
    wrapper.command('amend', message=b'amend1')

    wrapper.update(ctx.hex(), hidden=True)
    repo_path.join('foo').write('amend2')
    wrapper.command('amend', message=b'amend2')

    return wrapper, ctx, handler


def test_analyse_vanished_topic_divergence_initial_import(tmpdir):
    wrapper, ctx, handler = prepare_topic_divergence(
        tmpdir,
        additional_config=dict(heptapod={'initial-import': True}))

    handler.analyse_vanished_topic(
        'default', 'zetop',
        ctx.hex(),
        log_info=dict(ref='refs/heads/topic/default/zetop',
                      before_git_sha='01234cafe'))


def test_analyse_vanished_topic_divergence_not_initial_import(tmpdir):
    wrapper, ctx, handler = prepare_topic_divergence(tmpdir)

    with pytest.raises(error.Abort) as exc_info:
        handler.analyse_vanished_topic(
            'default', 'zetop',
            ctx.hex(),
            log_info={b'ref': b'refs/heads/topic/default/zetop',
                      b'before_git_sha': b'01234cafe'})

    # TODO UPSTREAM evolve gives a str message instead of the standard
    # bytes for error.Abort
    exc_msg = pycompat.sysbytes(exc_info.value.args[0])
    assert ctx.hex() in exc_msg
    assert b'divergent' in exc_msg


def test_topic_published_multiple_heads(tmpdir):
    wrapper = RepoWrapper.init(tmpdir.join('repo'),
                               config=common_config())
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    wrapper.write_commit('foo', message='foo0')
    before_ctx = wrapper.write_commit('foo', message='in topic',
                                      topic='zzetop', return_ctx=True)

    # let's publish for the sake of consistency, but these inner tests
    # aren't based on the state of a Git repo anyway: previous state is
    # passed explicitely
    wrapper.set_phase('public', ['zzetop'])

    # let's add two public in topic descendants
    ctx1 = wrapper.write_commit('foo', message='this is wild 1',
                                parent=before_ctx.node(), topic='zzetop',
                                return_ctx=True)
    ctx2 = wrapper.write_commit('foo', message='this is wild 2',
                                parent=before_ctx.node(), topic='zzetop',
                                return_ctx=True)
    wrapper.set_phase('public', [ctx1.hex(), ctx2.hex()])

    before_git_sha = b'01234cafe'
    handler.map_set(before_git_sha, before_ctx.hex())
    prune = handler.analyse_vanished_topic(
        b'default', b'zzetop',
        before_ctx.hex(),
        log_info=dict(ref='refs/heads/topic/default/zzetop',
                      before_git_sha=before_git_sha))
    assert prune == prune_reasons.TopicPublished(before_git_sha)


def test_latest_unique_successor_no_descendant(tmpdir):
    wrapper = RepoWrapper.init(tmpdir.join('repo'),
                               config=common_config())
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    ctx = wrapper.write_commit('foo', message='foo0', return_ctx=True)
    assert handler.latest_topic_descendant(b'sometop', ctx) is None


def test_generate_prune_changes_existing_unknown(tmpdir):
    config = common_config()
    config['experimental'] = {'hg-git.prune-previously-closed-branches': 'no'}
    wrapper = RepoWrapper.init(tmpdir.join('repo'), config=config)

    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)

    # let's have a git -> hg map that gives us an unknown hg sha.
    # it still has to be formally valid, though (hex, length 40)
    map_hg = {b'1234': b'cafe' * 10}

    def map_hg_get(git_sha):
        return map_hg.get(git_sha)

    handler.map_hg_get = map_hg_get

    gitlab_branch = b'branch/previously-closed'
    branch_ref = git_branch_ref(gitlab_branch)
    existing = {branch_ref: b'1234'}
    to_prune = {gitlab_branch: 'closed'}
    closed_reason = prune_reasons.BranchClosed()

    reasons, changes = handler.generate_prune_changes(to_prune, existing)
    assert reasons == {gitlab_branch: closed_reason}

    # and now with the previous Git changeset not even known
    existing = {branch_ref: b'unknown'}
    reasons, changes = handler.generate_prune_changes(to_prune, existing)
    assert reasons == {gitlab_branch: closed_reason}


def test_never_prune_default_branch(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)

    config = common_config()
    config['heptapod'] = dict(native=True)
    wrapper = RepoWrapper.init(tmpdir.join('repo'), config=config)

    wrapper.write_commit('foo')
    wrapper.command('gitlab-mirror')
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)

    def no_analyze(existing, exportable):
        # that's just not the point here
        return {}

    handler.analyze_vanished_refs = no_analyze

    with pytest.raises(error.Abort) as exc_info:
        handler.compare_exportable(
            {},
            {ZERO_SHA: {b'branch/default': prune_reasons.HeadPruneReason()}})

    assert re.search(br'prune.*default branch', exc_info.value.args[0])


def test_heptapod_compare_tags_inconsistent(tmpdir):
    wrapper = RepoWrapper.init(tmpdir.join('repo'),
                               config=common_config())
    wrapper.write_commit('foo')
    # yes '..' is a valid tag name in Mercurial, no wonder Git doesn't like it
    wrapper.command('tag', b'0.12.3', rev=b'.')

    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)

    # the handler's hg_sha -> git_sha mapping being empty, it won't find the
    # Git SHA for our changeset, and that's the case we're testing
    changes = handler.heptapod_compare_tags({})
    assert changes == {}


def test_gitlab_tag_ref():
    tag = b'v1.2'
    assert gitlab_tag_ref(tag) == b'refs/tags/v1.2'


def test_heptapod_compare_tags_invalid_git_name(tmpdir):
    wrapper = RepoWrapper.init(tmpdir.join('repo'),
                               config=common_config())
    ctx = wrapper.write_commit('foo', return_ctx=True)
    # yes '..' is a valid tag name in Mercurial, no wonder Git doesn't like it
    wrapper.command('tag', b'..', rev=b'.')

    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    # just enough so that the changeset seems to be known on the Git side
    handler.map_set(b'should be a Git SHA', ctx.hex())
    changes = handler.heptapod_compare_tags({})
    assert changes == {}
