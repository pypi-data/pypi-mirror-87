# Copyright 2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Integration tests for the Git subsystem

In this case, "integration" means that we're testing the main methods,
using true Git repos, and the whole Hook logic. We may also need to create
complex transactions, with several commits, rebases, phase changes etc.
"""
from __future__ import absolute_import

from dulwich.protocol import ZERO_SHA
import pytest
import re
import subprocess

from heptapod.gitlab import hooks
from heptapod.gitlab.prune_reasons import (
    HeadPruneReason,
    BookmarkRemoved,
    BranchClosed,
    TopicPublished,
)
from heptapod.testhelpers import (
    RepoWrapper,
)
from hgext3rd.heptapod.branch import get_default_gitlab_branch
from mercurial import (
    encoding,
    error,
    pycompat,
    ui as uimod,
)
from ...git import (
    GitRefChange,
    HeptapodGitHandler,
)
from ..utils import common_config


parametrize = pytest.mark.parametrize


def patch_gitlab_hooks(monkeypatch, records, action=None):

    def call(self, changes):
        records.append((self.name, changes))
        if action is not None:
            return action(self.name, changes)
        else:
            return 0, ("hook %r ok" % self.name).encode(), 'no error'

    def init(self, repo, encoding='utf-8'):
        self.repo = repo
        self.encoding = encoding

    monkeypatch.setattr(hooks.Hook, '__init__', init)
    monkeypatch.setattr(hooks.PreReceive, '__call__', call)
    monkeypatch.setattr(hooks.PostReceive, '__call__', call)


def patch_ui_warnings(monkeypatch, records):

    def warn(self, *a):
        records.append(a)

    monkeypatch.setattr(uimod.ui, 'warn', warn)


def extract_git_branch_titles(branches):
    return {ref: info['title'] for ref, info in branches.items()}


class GitRepo(object):

    def __init__(self, path):
        self.path = path

    @classmethod
    def init(cls, path):
        subprocess.call(('git', 'init', '--bare', str(path)))
        return cls(path)

    def branch_titles(self):
        return extract_git_branch_titles(self.branches())

    def branches(self):
        out = subprocess.check_output(('git', 'branch', '-v', '--no-abbrev'),
                                      cwd=str(self.path))
        split_lines = (l.lstrip(b'*').strip().split(None, 2)
                       for l in out.splitlines())
        return {sp[0]: dict(sha=sp[1], title=sp[2]) for sp in split_lines}

    def tags(self):
        out = subprocess.check_output(('git', 'tag'), cwd=str(self.path))
        return set(l.strip() for l in out.splitlines())

    def commit_hash_title(self, revspec):
        out = subprocess.check_output(
            ('git', 'log', '-n1', revspec, r'--pretty=format:%H|%s'),
            cwd=str(self.path))
        return out.strip().split(b'|')

    def get_symref(self, name):
        return self.path.join(name).read().strip().split(':', 1)[1].strip()

    def set_symref(self, name, target_ref):
        self.path.join(name).write('ref: %s\n' % target_ref)

    def set_branch(self, name, sha):
        sha = pycompat.sysstr(sha)
        self.path.join('refs', 'heads', name).ensure().write(sha + '\n')

    def get_branch_sha(self, name):
        if isinstance(name, bytes):
            name = name.decode()
        return self.path.join('refs', 'heads', name).read().strip()


def make_main_repo(path):
    """Make repo with 2 public revs; return wrapper, ctx of rev 0

    The returned ctx is for the first changeset because we'll use it as
    a branching point, hence more often than the second.
    """
    config = common_config()
    config['extensions']['hggit'] = ''
    config['phases'] = dict(publish=False)

    wrapper = RepoWrapper.init(path, config=config)
    ctx = wrapper.write_commit('foo', content='foo0', message="default0",
                               return_ctx=True)
    wrapper.write_commit('foo', content='foo1', message="default1")
    wrapper.set_phase('public', ['.'])
    return wrapper, ctx


def set_allow_bookmarks(repo_wrapper, value):
    repo_wrapper.repo.ui.setconfig(
        b'experimental', b'hg-git.bookmarks-on-named-branches', value)


def set_prune_closed_branches(repo_wrapper, value):
    repo_wrapper.repo.ui.setconfig(
        b'experimental', b'hg-git.prune-newly-closed-branches', value)


def activate_mirror(repo_wrapper):
    """Activate the mirrorring hook for given repo.

    Using the hook is a simple way to get in-transaction, while still within
    a repo fully controlled by these tests (configuration, notably).
    """
    repo_wrapper.repo.ui.setconfig(
        b'hooks', b'pretxnclose.testcase',
        b'python:heptapod.hooks.gitlab_mirror.mirror')


def test_basic(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    repo_path = tmpdir.join('repo.hg')
    repo, base_ctx = make_main_repo(repo_path)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    repo.command('gitlab-mirror')

    assert git_repo.branch_titles() == {b'branch/default': b'default1'}
    sha = git_repo.branches()[b'branch/default']['sha']
    assert notifs == [
        ('pre-receive', ({}, {b'refs/heads/branch/default': (ZERO_SHA, sha)})),
        ('post-receive', ({},
                          {b'refs/heads/branch/default': (ZERO_SHA, sha)})),
    ]


def test_alternate_encoding(tmpdir, monkeypatch):
    """Round trip with branch name not in UTF-8.

    It's not clear whether this is valid on the GitLab side, but it should
    be transparent in here: what comes in comes out.
    """
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    repo_path = tmpdir.join('repo.hg')
    wrapper, base_ctx = make_main_repo(repo_path)
    wrapper.command('gitlab-mirror')
    notifs[:] = []

    git_repo = GitRepo.init(tmpdir.join('repo.git'))

    # Even though it's been initialized from the `HGENCODING` environment
    # variable, the encoding is a global.
    monkeypatch.setattr(encoding, 'encoding', b'latin-1')

    wrapper.write_commit('encoded', branch=b'pr\xe9parations')
    wrapper.command('gitlab-mirror')

    # not using existing helpers to avoid making the test tautological
    git_branch = b'branch/pr\xe9parations'
    git_ref = b'refs/heads/' + git_branch

    # both in Git repo and in notifs, we have the exact same bytes as provided
    assert set(git_repo.branch_titles()) == {b'branch/default', git_branch}
    sha = git_repo.branches()[git_branch]['sha']
    assert notifs == [
        ('pre-receive', ({}, {git_ref: (ZERO_SHA, sha)})),
        ('post-receive', ({}, {git_ref: (ZERO_SHA, sha)})),
    ]


def test_wiki(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    repo_path = tmpdir.join('repo.hg')
    wrapper, base_ctx = make_main_repo(repo_path)
    wrapper.repo.ui.environ[b'GL_REPOSITORY'] = b'wiki-251'
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.command('gitlab-mirror')

    # for wikis, we duplicate `branch/default` as `master`
    assert git_repo.branch_titles() == {b'branch/default': b'default1',
                                        b'master': b'default1',
                                        }
    sha = git_repo.branches()[b'branch/default']['sha']
    changes = {}, {b'refs/heads/branch/default': (ZERO_SHA, sha),
                   b'refs/heads/master': (ZERO_SHA, sha),
                   }
    assert notifs == [
        ('pre-receive', changes),
        ('post-receive', changes),
    ]


def test_tags(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    repo_path = tmpdir.join('repo.hg')
    repo, base_ctx = make_main_repo(repo_path)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))

    # Creation
    repo.command('tag', b'v1.2.3', rev=base_ctx.hex())
    repo.command('gitlab-mirror')

    branches = git_repo.branches()
    assert list(branches) == [b'branch/default']
    branch = branches[b'branch/default']

    assert b'v1.2.3' in branch['title']
    assert git_repo.tags() == {b'v1.2.3', }
    tagged_git_sha_0, tagged_git_title = git_repo.commit_hash_title('v1.2.3')
    assert tagged_git_title == b'default0'

    first_default_branch_sha = branch['sha']
    changes = {}, {
        b'refs/heads/branch/default': (ZERO_SHA, first_default_branch_sha),
        b'refs/tags/v1.2.3': (ZERO_SHA, tagged_git_sha_0),
    }
    assert notifs == [('pre-receive', changes), ('post-receive', changes)]
    del notifs[:]

    # Modification
    repo.command('tag', b'v1.2.3', rev=b'1', force=True)
    repo.command('gitlab-mirror')

    assert git_repo.tags() == {b'v1.2.3', }
    tagged_git_sha_1, tagged_git_title = git_repo.commit_hash_title('v1.2.3')
    assert tagged_git_title == b'default1'

    new_default_branch_sha = git_repo.branches()[b'branch/default']['sha']
    changes = {}, {
        b'refs/heads/branch/default': (first_default_branch_sha,
                                       new_default_branch_sha),
        b'refs/tags/v1.2.3': (tagged_git_sha_0, tagged_git_sha_1),
    }
    assert notifs == [('pre-receive', changes), ('post-receive', changes)]

    # Removal not supported in Heptapod 0.8. TODO later


def test_share(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    main_path = tmpdir.join('main.hg')
    main_wrapper, base_ctx = make_main_repo(main_path)
    git_repo = GitRepo.init(tmpdir.join('main.git'))

    # let's start with some commits in the Git repo
    main_wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {b'branch/default': b'default1'}

    # now let's make a share
    dest_wrapper = main_wrapper.share(tmpdir.join('share.hg'))
    dest_wrapper.write_commit('bar', message='other0',
                              branch='other', parent=base_ctx.node())
    dest_wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {b'branch/default': b'default1',
                                        b'branch/other': b'other0'}


def test_bookmarks_prune(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    server_path = tmpdir.join('repo.hg')
    server, base_ctx = make_main_repo(server_path)
    server.command('bookmark', b'zebook', rev=base_ctx.hex())
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    # not being in a transaction accepts the bookmark immediately
    server.command('gitlab-mirror')
    assert git_repo.branch_titles() == {
        b'branch/default': b'default1',
        b'zebook': b'default0'
    }

    activate_mirror(server)
    server.command('bookmark', b'zebook', delete=True)

    assert server.repo.nodebookmarks(base_ctx.node()) == []
    assert git_repo.branch_titles() == {
        b'branch/default': b'default1',
    }

    # TODO assert notifs


def test_bookmarks_mask_branch_prune(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    server_path = tmpdir.join('repo.hg')
    server, base_ctx = make_main_repo(server_path)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    server.command('gitlab-mirror')
    # just checking our assumptions
    assert git_repo.branch_titles() == {b'branch/default': b'default1'}

    # we need to test the branch masking on a branch
    # that's not the GitLab default (which is protected)
    server.write_commit('foo', branch='other', message='other1')

    activate_mirror(server)
    set_allow_bookmarks(server, True)
    head = server.repo[b'tip']
    server.command('bookmark', b'zebook', rev=head.hex())
    assert git_repo.branch_titles() == {
        b'branch/default': b'default1',
        b'zebook': b'other1'
    }

    server.command('bookmark', b'zebook', delete=True)

    assert server.repo.nodebookmarks(head.node()) == []
    assert git_repo.branch_titles() == {
        b'branch/default': b'default1',
        b'branch/other': b'other1',
    }

    # TODO assert notifs


def test_bookmarks_dont_mask_default_branch(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    server_path = tmpdir.join('repo.hg')
    server, base_ctx = make_main_repo(server_path)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    server.command('gitlab-mirror')
    # just checking our assumptions
    assert git_repo.branch_titles() == {b'branch/default': b'default1'}

    activate_mirror(server)
    set_allow_bookmarks(server, True)
    head = server.repo[b'tip']
    git_sha = git_repo.get_branch_sha('branch/default').encode()

    del notifs[:]
    server.command('bookmark', b'zebook', rev=head.hex())

    # the default branch is not pruned
    assert git_repo.branch_titles() == {
        b'branch/default': b'default1',
        b'zebook': b'default1'
    }

    changes = {b'refs/heads/zebook': (ZERO_SHA, git_sha)}
    assert notifs == [('pre-receive', ({}, changes)),
                      ('post-receive', ({}, changes)),
                      ]

    del notifs[:]
    server.command('bookmark', b'zebook', delete=True)

    assert server.repo.nodebookmarks(head.node()) == []
    assert git_repo.branch_titles() == {b'branch/default': b'default1'}
    changes = {b'refs/heads/zebook': (git_sha, ZERO_SHA)}
    prunes = {b'zebook': BookmarkRemoved(git_sha)}

    assert notifs == [('pre-receive', (prunes, changes)),
                      ('post-receive', (prunes, changes)),
                      ]


@parametrize('branch_name', ('default', 'other'))
def test_change_gitlab_default_branch(tmpdir, monkeypatch, branch_name):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    config = common_config()
    config['extensions']['hggit'] = ''
    config['phases'] = dict(publish=False)

    wrapper = RepoWrapper.init(tmpdir.join('repo.hg'), config=config)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.write_commit('foo', message="other0",
                         branch=branch_name,
                         topic='initial')
    wrapper.command('gitlab-mirror')

    def assert_default_gitlab_branch(gl_branch):
        assert git_repo.get_symref('HEAD') == 'refs/heads/' + gl_branch
        gl_branch_bytes = pycompat.sysbytes(gl_branch)
        assert get_default_gitlab_branch(wrapper.repo) == gl_branch_bytes

    assert_default_gitlab_branch('topic/%s/initial' % branch_name)

    wrapper.set_phase('public', ['.'])
    wrapper.command('gitlab-mirror')

    assert_default_gitlab_branch('branch/' + branch_name)


def test_change_gitlab_default_branch_nothing_new(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    config = common_config()
    config['extensions']['hggit'] = ''
    config['phases'] = dict(publish=False)

    wrapper = RepoWrapper.init(tmpdir.join('repo.hg'), config=config)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.write_commit('foo', message="other0",
                         branch='default',
                         topic='initial')
    wrapper.command('gitlab-mirror')

    def assert_default_gitlab_branch(gl_branch):
        assert git_repo.get_symref('HEAD') == 'refs/heads/' + gl_branch
        gl_branch_bytes = pycompat.sysbytes(gl_branch)
        assert get_default_gitlab_branch(wrapper.repo) == gl_branch_bytes

    assert_default_gitlab_branch('topic/default/initial')

    wrapper.write_commit('foo', message="same gitlab branch")
    wrapper.command('gitlab-mirror')

    assert_default_gitlab_branch('topic/default/initial')


def test_closed_branch(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    wrapper.write_commit('foo', message="other0",
                         branch='other',
                         parent=base_ctx.node(),
                         return_ctx=True)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {b'branch/default': b'default1',
                                        b'branch/other': b'other0'}
    to_close_sha = git_repo.branches()[b'branch/other']['sha']
    set_prune_closed_branches(wrapper, True)
    activate_mirror(wrapper)
    del notifs[:]

    wrapper.command('commit', message=b"closing other",
                    close_branch=True)
    # we'll let GitLab do the pruning so that it can use the closing
    # sha for Merge Request detection.
    assert git_repo.branch_titles() == {b'branch/default': b'default1'}

    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    closing_sha = handler.map_git_get(wrapper.repo[b'tip'].hex())
    prune_reason = {b'branch/other':
                    BranchClosed([(closing_sha, [to_close_sha])])}
    changes = {b'refs/heads/branch/other': (to_close_sha, ZERO_SHA)}

    assert notifs == [('pre-receive', (prune_reason, changes)),
                      ('post-receive', (prune_reason, changes))]


def test_previously_closed_branch_not_pruned(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    wrapper.write_commit('foo', message="other0",
                         branch='other',
                         parent=base_ctx.node(),
                         return_ctx=True)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))

    # let's prepare a closed branch that hasn't been prune
    set_prune_closed_branches(wrapper, False)
    wrapper.command('commit', message=b"closing other", close_branch=True)
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {b'branch/default': b'default1',
                                        b'branch/other': b'closing other'}

    # subsequent calls won't prune it...
    set_prune_closed_branches(wrapper, True)
    wrapper.repo.ui.setconfig(
        b'experimental', b'hg-git.prune-previously-closed-branches', False)
    wrapper.command('gitlab-mirror')

    assert git_repo.branch_titles()[b'branch/other'] == b'closing other'

    # until we flip the right switch
    wrapper.repo.ui.setconfig(
        b'experimental', b'hg-git.prune-previously-closed-branches', True)
    wrapper.command('gitlab-mirror')

    assert b'branch/other' not in git_repo.branch_titles()


def test_closed_branch_not_in_git(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    wrapper.write_commit('foo', message="other0",
                         branch='other',
                         parent=base_ctx.node(),
                         return_ctx=True)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))

    # the `other` branch being mirrored as already closed, will trigger
    # a prune request that should be ignored in order not to fail
    wrapper.command('commit', message=b"closing other", close_branch=True)
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {b'branch/default': b'default1'}


def test_closed_default_branch(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {b'branch/default': b'default1'}
    git_repo.set_symref('HEAD', 'refs/heads/branch/default')

    set_prune_closed_branches(wrapper, True)
    wrapper.command('commit', message=b"closing default!", close_branch=True)

    # On native repos, this is a user error
    wrapper.repo.ui.setconfig(b'heptapod', b'native', True)

    del notifs[:]
    with pytest.raises(error.Abort) as exc_info:
        wrapper.command('gitlab-mirror')

    assert re.search(br'prune.*default branch', exc_info.value.args[0])

    assert not notifs
    assert git_repo.branch_titles() == {b'branch/default': b'default1'}

    # On non-native repos, this is ignored
    wrapper.repo.ui.setconfig(b'heptapod', b'native', False)
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {b'branch/default': b'default1'}


def test_multiple_heads_merge(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    warnings = []
    patch_ui_warnings(monkeypatch, warnings)

    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    first = wrapper.repo[b'tip']
    second = wrapper.write_commit('bar', message="second head",
                                  branch='default',
                                  parent=base_ctx.node(),
                                  return_ctx=True)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {
        b'wild/' + first.hex(): b'default1',
        b'wild/' + second.hex(): b'second head',
        # the most recently added revision always wins
        b'branch/default': b'second head',
    }
    assert any(b'experimental.single-head-per-branch' in part
               for warning in warnings for part in warning)
    wrapper.command('merge')
    wrapper.command('commit', message=b'merging heads')
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {b'branch/default': b'merging heads'}

    # TODO assert notifs


def test_push_multiple_heads_switch_branch(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    # second head on default branch (easy to merge for later test)
    wrapper.write_commit('bar', message="default head 2",
                         parent=base_ctx.node())
    default_heads_titles = {b'default1', b'default head 2'}

    wrapper.command('gitlab-mirror')

    branch_titles = git_repo.branch_titles()
    assert set(branch_titles.values()) == default_heads_titles
    assert len(branch_titles) == 3

    wrapper.write_commit('foo', message="other", branch='other')
    wrapper.command('gitlab-mirror')
    branch_titles = git_repo.branch_titles()
    assert set(branch_titles.values()) == default_heads_titles | {b'other', }
    assert len(branch_titles) == 4

    # now let's add a topic on top of one of those wild 'default' heads
    wrapper.write_commit('foo', message="on topic",
                         topic='zetop',
                         parent=base_ctx.node())

    wrapper.command('gitlab-mirror')
    branch_titles = git_repo.branch_titles()
    assert set(b for b in branch_titles if not b.startswith(b'wild/')) == {
        b'branch/default', b'branch/other', b'topic/default/zetop'}

    assert set(title
               for name, title in branch_titles.items()
               if name.startswith(b'wild/')) == default_heads_titles
    assert branch_titles[b'branch/default'] in default_heads_titles
    assert branch_titles[b'branch/other'] == b'other'
    assert branch_titles[b'topic/default/zetop'] == b'on topic'


def test_push_multiple_heads_refuse(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    # in Heptapod 0.18, this will be entirely controlled by
    # heptapod.allow-multiple-heads
    wrapper.repo.ui.setconfig(b'experimental', b'single-head-per-branch', True)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.write_commit('bar', message="default head 2",
                         parent=base_ctx.node())

    with pytest.raises(error.Abort) as exc_info:
        wrapper.command('gitlab-mirror')

    assert b'multiple heads' in exc_info.value.args[0]
    assert git_repo.branch_titles() == {}


def test_topic_pruned(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    wrapper, _ = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.write_commit('foo', message='in topic', topic='zzetop')
    wrapper.command('gitlab-mirror')
    del notifs[:]

    topic_gl_branch = b'topic/default/zzetop'
    branches_before = git_repo.branches()
    assert extract_git_branch_titles(branches_before) == {
        b'branch/default': b'default1',
        topic_gl_branch: b'in topic'}

    wrapper.prune(b'zzetop')
    wrapper.command('gitlab-mirror')

    topic_ref = b'refs/heads/topic/default/zzetop'
    topic_change = {topic_ref: (
        branches_before[b'topic/default/zzetop']['sha'],
        ZERO_SHA,
    )}
    prune_reason = {topic_gl_branch: HeadPruneReason()}

    assert git_repo.branch_titles() == {
        b'branch/default': b'default1',
    }
    assert notifs == [('pre-receive', (prune_reason, topic_change)),
                      ('post-receive', (prune_reason, topic_change))]


def test_topic_amended(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    repo_path = tmpdir.join('repo.hg')
    wrapper, _ = make_main_repo(repo_path)
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.write_commit('foo', message='in topic', topic='zzetop')
    wrapper.command('gitlab-mirror')
    del notifs[:]

    branches_before = git_repo.branches()
    assert extract_git_branch_titles(branches_before) == {
        b'branch/default': b'default1',
        b'topic/default/zzetop': b'in topic'}

    repo_path.join('foo').write('amend1')
    wrapper.command('amend', message=b'amend1')

    wrapper.command('gitlab-mirror')

    branches = git_repo.branches()
    assert extract_git_branch_titles(branches) == {
        b'branch/default': b'default1',
        b'topic/default/zzetop': b'amend1',
    }

    topic_change = {b'refs/heads/topic/default/zzetop': (
        branches_before[b'topic/default/zzetop']['sha'],
        branches[b'topic/default/zzetop']['sha'],
    )}

    assert notifs == [('pre-receive', ({}, topic_change)),
                      ('post-receive', ({}, topic_change))]


def test_topic_ff_publish(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    wrapper, _ = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.command('topics', b'zzetop')
    wrapper.write_commit('foo', message='in ff topic')
    wrapper.command('gitlab-mirror')
    del notifs[:]

    topic_gl_branch = b'topic/default/zzetop'
    branches_before = git_repo.branches()
    assert extract_git_branch_titles(branches_before) == {
        b'branch/default': b'default1',
        topic_gl_branch: b'in ff topic'}

    wrapper.set_phase('public', ['zzetop'])
    wrapper.command('gitlab-mirror')

    assert git_repo.branch_titles() == {b'branch/default': b'in ff topic'}

    topic_ref = b'refs/heads/topic/default/zzetop'
    topic_before_sha = branches_before[b'topic/default/zzetop']['sha']

    prune_reasons = {topic_gl_branch: TopicPublished(topic_before_sha)}
    changes = {
        b'refs/heads/branch/default': (
            branches_before[b'branch/default']['sha'],
            topic_before_sha,
        ),
        topic_ref: (
            branches_before[b'topic/default/zzetop']['sha'],
            ZERO_SHA,
        )
    }

    assert notifs == [('pre-receive', (prune_reasons, changes)),
                      ('post-receive', (prune_reasons, changes))]


def test_topic_rebase_publish(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    wrapper, _ = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.write_commit('zz', message='in topic', topic='zzetop')
    wrapper.command('gitlab-mirror')
    del notifs[:]

    topic_gl_branch = b'topic/default/zzetop'

    branches_before = git_repo.branches()
    assert extract_git_branch_titles(branches_before) == {
        b'branch/default': b'default1',
        topic_gl_branch: b'in topic'}

    wrapper.command('rebase', rev=[b'zzetop'])
    wrapper.set_phase('public', ['zzetop'])
    wrapper.command('gitlab-mirror')

    branches_after = git_repo.branches()
    assert extract_git_branch_titles(branches_after) == {
        b'branch/default': b'in topic'}

    default_after_sha = branches_after[b'branch/default']['sha']
    prune_reasons = {topic_gl_branch: TopicPublished(default_after_sha)}
    changes = {
        b'refs/heads/branch/default': (
            branches_before[b'branch/default']['sha'],
            default_after_sha),
        b'refs/heads/topic/default/zzetop': (
            branches_before[b'topic/default/zzetop']['sha'],
            ZERO_SHA),
    }
    assert notifs == [('pre-receive', (prune_reasons, changes)),
                      ('post-receive', (prune_reasons, changes))]


def test_topic_git_escape(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    wrapper, _ = make_main_repo(tmpdir.join('repo.hg'))
    del notifs[:]

    # Only test names that are possible with topics in the first place
    invalid_git_ref_names = [
        ".starts-with-dot",
        "..",
        "ends-with.lock",
        "ends-with-dot.",
    ]
    for name in invalid_git_ref_names:
        wrapper.write_commit('zz', message='in topic', topic=name)

    # This fails if topic names that are invalid in Git are not escaped
    wrapper.command('gitlab-mirror')


def test_topic_add_rebase_publish(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.write_commit('zz', message='in topic',
                         parent=base_ctx.node(), topic='zzetop')
    wrapper.command('gitlab-mirror')
    del notifs[:]

    topic_gl_branch = b'topic/default/zzetop'

    branches_before = git_repo.branches()
    assert extract_git_branch_titles(branches_before) == {
        b'branch/default': b'default1',
        topic_gl_branch: b'in topic'}

    wrapper.write_commit('zz', message='topic addition')
    wrapper.command('rebase')
    wrapper.set_phase('public', ['zzetop'])
    wrapper.command('gitlab-mirror')

    branches_after = git_repo.branches()
    assert extract_git_branch_titles(branches_after) == {
        b'branch/default': b'topic addition'}

    changes = {
        b'refs/heads/branch/default': (
            branches_before[b'branch/default']['sha'],
            branches_after[b'branch/default']['sha']),
        b'refs/heads/topic/default/zzetop': (
            branches_before[b'topic/default/zzetop']['sha'],
            ZERO_SHA),
    }
    prune_reasons = {
        topic_gl_branch:
            TopicPublished(branches_after[b'branch/default']['sha'])
    }
    assert notifs == [('pre-receive', (prune_reasons, changes)),
                      ('post-receive', (prune_reasons, changes))]


def test_topic_clear_publish(tmpdir, monkeypatch):
    """The topic head seen from Git is public and has changed topic.

    This is the test for heptapod#265
    The starting point can be considered to be corrupted: any topic change
    should have updated the Git branch for the topic. In this scenario
    the change is a removal, wich should have pruned the Git branch, but
    somehow the Git branch got updated to the new changeset, that doesn't
    have a topic.
    """
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    wrapper.write_commit('zz', message='in topic', topic='zzetop')
    wrapper.command('gitlab-mirror')

    topic_gl_branch = b'topic/default/zzetop'

    branches_before = git_repo.branches()
    assert extract_git_branch_titles(branches_before) == {
        b'branch/default': b'default1',
        topic_gl_branch: b'in topic'}

    wrapper.command('topics', rev=[b'.'], clear=True)
    wrapper.command('gitlab-mirror')
    wrapper.set_phase('public', ['.'])
    forced_topic_before_sha = git_repo.get_branch_sha('branch/default')
    forced_topic_before_sha_bytes = pycompat.sysbytes(forced_topic_before_sha)

    # here's the main point:
    git_repo.set_branch(pycompat.sysstr(topic_gl_branch),
                        forced_topic_before_sha)

    del notifs[:]
    # This used to raise LookupError
    wrapper.command('gitlab-mirror')

    branches_after = git_repo.branches()
    assert extract_git_branch_titles(branches_after) == {
        b'branch/default': b'in topic',
    }
    changes = (
        {topic_gl_branch: TopicPublished(forced_topic_before_sha_bytes)},
        {b'refs/heads/topic/default/zzetop': (
            branches_after[b'branch/default']['sha'],
            ZERO_SHA)},
    )
    assert notifs == [('pre-receive', changes),
                      ('post-receive', changes)]


def test_topic_branch_change(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))

    wrapper.write_commit('bar', message='other0',
                         parent=base_ctx.node(), branch='other')
    wrapper.write_commit('zz', message='in topic',
                         topic='zzetop')
    wrapper.command('gitlab-mirror')

    assert git_repo.branch_titles() == {
        b'branch/default': b'default1',
        b'branch/other': b'other0',
        b'topic/other/zzetop': b'in topic'}

    wrapper.command('rebase', rev=[b'zzetop'], dest=b'default')
    wrapper.command('gitlab-mirror')
    assert git_repo.branch_titles() == {
        b'branch/default': b'default1',
        b'branch/other': b'other0',
        b'topic/default/zzetop': b'in topic',
    }


def test_analyse_vanished_topic_not_in_git(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    repo = wrapper.repo
    git_repo = GitRepo.init(tmpdir.join('repo.git'))

    wrapper.write_commit('zz', message='in topic', topic='zzetop')
    wrapper.command('gitlab-mirror')

    def return_unknown(handler, *a, **kw):
        handler.repo.test_patch_called = True
        return b'unknown-to-git'

    # let's make the published topic analysis return something unknown to Git
    monkeypatch.setattr(HeptapodGitHandler, 'published_topic_latest_hg_sha',
                        return_unknown)

    wrapper.set_phase('public', ['zzetop'])
    # Calling export directly because through the hook, such
    # monkey patching often does not work.
    HeptapodGitHandler(repo, repo.ui).export_commits()

    # we didn't fail and have been conservative with the topic GitLab branch
    assert git_repo.branch_titles() == {
        b'branch/default': b'in topic',
        b'topic/default/zzetop': b'in topic'
    }

    # note that coverage would notice if the test harness didn't work
    assert wrapper.repo.test_patch_called


def test_heptapod_notify_gitlab(tmpdir, monkeypatch):
    wrapper = RepoWrapper.init(tmpdir.join('repo'))
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)

    notifs = []

    def trigger_failures(name, changes):
        if b'exc' in changes[1]:
            raise RuntimeError('trigger_failures: ' + name)
        if b'code_one' in changes[1]:
            return 1, b'', 'hook refusal'
        return 0, b'Consider a MR for ' + name.encode(), ''

    patch_gitlab_hooks(monkeypatch, notifs, action=trigger_failures)

    # minimal valid change
    change = GitRefChange(b'master', b'before', b'after')
    hook = hooks.PreReceive(wrapper.repo)
    handler.heptapod_notify_gitlab(hook, [], {b'master': change},
                                   allow_error=False)
    assert notifs == [('pre-receive',
                       ([], {b'master': (b'before', b'after')})
                       )]
    del notifs[:]

    with pytest.raises(error.Abort) as exc_info:
        handler.heptapod_notify_gitlab(hook, [], {b'code_one': change},
                                       allow_error=False)
    assert b"hook refusal" in exc_info.value.args[0]

    with pytest.raises(RuntimeError) as exc_info:
        handler.heptapod_notify_gitlab(hook, [], {b'exc': change},
                                       allow_error=False)
    assert "trigger_failures" in exc_info.value.args[0]

    # case where exception is triggered yet is accepted
    errors = []

    def record_ui_error(*args):
        errors.append(args)
    monkeypatch.setattr(handler.repo.ui, 'error', record_ui_error)
    handler.heptapod_notify_gitlab(hook, [], {b'exc': change},
                                   allow_error=True)
    assert errors[0][0].splitlines()[:2] == [
        (b"GitLab update error (GitLab 'pre-receive' hook): "
         + pycompat.sysbytes(
             # this repr() differs between py2 and py3
             repr(RuntimeError('trigger_failures: pre-receive')))),
        b"Traceback (most recent call last):"
    ]


def test_heptapod_notify_gitlab_native(tmpdir, monkeypatch):
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)

    # setup a repo pair, with two commits
    wrapper, base_ctx = make_main_repo(tmpdir.join('repo.hg'))
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    topic_ctx = wrapper.write_commit('zz', message='in topic', topic='zzetop')
    wrapper.command('gitlab-mirror')
    del notifs[:]  # start over on notifs for actual testing

    gl_branch_default = b'branch/default'
    default_hg_sha = wrapper.repo[1].hex()
    default_git_sha = git_repo.get_branch_sha(gl_branch_default).encode()

    gl_branch_topic = b'topic/default/zzetop'
    topic_hg_sha = topic_ctx.hex()
    topic_git_sha = git_repo.get_branch_sha(gl_branch_topic).encode()

    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)

    hook1 = hooks.PreReceive(wrapper.repo)
    hook2 = hooks.PostReceive(wrapper.repo)

    wrapper.repo.ui.setconfig(b'heptapod', b'native', b'yes')

    # branch creation, interesting because ZERO_SHA isn't in the mappings
    change = GitRefChange(b'something', ZERO_SHA, topic_git_sha)
    handler.heptapod_notify_gitlab(hook1, [], {b'something': change})
    assert notifs == [
        ('pre-receive', ([], {b'something': (ZERO_SHA, topic_hg_sha)}))
    ]

    # branch change
    # second hook call to check for side effects in pre/post-receive succession
    change = GitRefChange(b'branch/default', default_git_sha, topic_git_sha)
    del notifs[:]
    handler.heptapod_notify_gitlab(hook1, [], {b'branch/default': change})
    assert notifs == [
        ('pre-receive', ([],
                         {b'branch/default': (default_hg_sha, topic_hg_sha)}))
    ]
    del notifs[:]
    handler.heptapod_notify_gitlab(hook2, [], {b'branch/default': change})
    assert notifs == [
        ('post-receive', ([],
                          {b'branch/default': (default_hg_sha, topic_hg_sha)}))
    ]

    # Topic published (making this realistic, but consistency shouldn't matter)
    # this tests most of the PruneReasons. If a new one not subclassing
    # HeadPruneReasonWithSha would appear, coverage drop would warn us.
    del notifs[:]
    prune_change = GitRefChange(gl_branch_topic, topic_git_sha, ZERO_SHA)
    prune_reasons = {gl_branch_topic: TopicPublished(topic_git_sha)}
    changes = {gl_branch_default: change, gl_branch_topic: prune_change}
    expected = ({gl_branch_topic: TopicPublished(topic_hg_sha)},
                {gl_branch_default: (default_hg_sha, topic_hg_sha),
                 gl_branch_topic: (topic_hg_sha, ZERO_SHA),
                 })
    handler.heptapod_notify_gitlab(hook1, prune_reasons, changes)
    assert notifs[-1] == ('pre-receive', expected)
    handler.heptapod_notify_gitlab(hook2, prune_reasons, changes)
    assert notifs[-1] == ('post-receive', expected)

    # BranchClosed.
    # This example is less realistic, we pretend the topic changeset
    # actually closes the default branch. At this low level, it doesn't matter.
    del notifs[:]
    prune_change = GitRefChange(gl_branch_default, default_git_sha, ZERO_SHA)
    changes = {gl_branch_default: prune_change}
    prune_reasons = {
        gl_branch_default: BranchClosed([(topic_git_sha, [default_git_sha])]),
    }
    expected = (
        {gl_branch_default: BranchClosed([[topic_hg_sha, [default_hg_sha]]])},
        {gl_branch_default: (default_hg_sha, ZERO_SHA)},
    )
    handler.heptapod_notify_gitlab(hook1, prune_reasons, changes)
    assert notifs[-1] == ('pre-receive', expected)
    handler.heptapod_notify_gitlab(hook2, prune_reasons, changes)
    assert notifs[-1] == ('post-receive', expected)

    # HeadPruneReason with no info to convert
    prune_reasons = {gl_branch_default: HeadPruneReason()}
    expected = (
        {gl_branch_default: HeadPruneReason()},
        {gl_branch_default: (default_hg_sha, ZERO_SHA)},
    )
    handler.heptapod_notify_gitlab(hook1, prune_reasons, changes)
    assert notifs[-1] == ('pre-receive', expected)

    # Corner case: BranchClosed without info to convert
    prune_reasons = {gl_branch_default: BranchClosed()}
    expected = (
        {gl_branch_default: BranchClosed()},
        {gl_branch_default: (default_hg_sha, ZERO_SHA)},
    )
    handler.heptapod_notify_gitlab(hook1, prune_reasons, changes)
    assert notifs[-1] == ('pre-receive', expected)


def test_subrepos(tmpdir, monkeypatch):
    """See heptapod#310 and heptapod#311."""
    notifs = []
    patch_gitlab_hooks(monkeypatch, notifs)
    main_path = tmpdir.join('repo.hg')
    GitRepo.init(tmpdir.join('repo.git'))
    wrapper, base_ctx = make_main_repo(main_path)

    nested_path = main_path.join('nested')
    nested = RepoWrapper.init(nested_path)
    nested.write_commit("bar", content="in nested")
    main_path.join('.hgsub').write("\n".join((
        "nested = ../bar",
        "[subpaths]",  # reproduction of heptapod#310
        "foo2=bar2",
    )))

    wrapper.command(b'add', subrepos=True)
    wrapper.command(b'commit', subrepos=True, message=b"invalid")
    wrapper.command('gitlab-mirror')

    wrapper.repo.ui.setconfig(b'hooks', b'precommit',
                              b'python:heptapod.hooks.subrepos.forbid_commit')
    with pytest.raises(error.Abort) as exc_info:
        wrapper.write_commit("foo")
    assert re.search(b'cannot commit.*there are subrepos',
                     exc_info.value.args[0])

    # Now let's simulate update from NULL revision, as Heptapod's
    # use of shares would do
    wrapper.command(b'update', b'0000000000000000000000', clean=True)
    nested_path.remove()

    with pytest.raises(error.Abort) as exc_info:
        wrapper.command(b'update', b'default')
    assert b'not supported' in exc_info.value.args[0]


def test_default_git_ref(tmpdir):
    wrapper = RepoWrapper.init(tmpdir.join('repo'),
                               config=common_config())
    git_repo = GitRepo.init(tmpdir.join('repo.git'))
    handler = HeptapodGitHandler(wrapper.repo, wrapper.repo.ui)
    # default Git value
    assert handler.get_default_git_ref() == b'refs/heads/master'
    other_ref = b'refs/heads/something'
    handler.set_default_gitlab_ref(other_ref)

    assert git_repo.get_symref('HEAD') == other_ref.decode()

    # instance level cache got invalidated
    assert handler.get_default_git_ref() == other_ref
