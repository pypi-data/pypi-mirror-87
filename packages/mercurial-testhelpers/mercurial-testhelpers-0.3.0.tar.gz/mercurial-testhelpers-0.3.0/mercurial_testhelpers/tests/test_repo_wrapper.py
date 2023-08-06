# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
from __future__ import absolute_import
from mercurial import (
    phases,
)
import pytest

from ..repo_wrapper import (
    RepoWrapper,
    NULL_ID,
    NULL_REVISION,
)

parametrize = pytest.mark.parametrize


def test_init_commit_file(tmpdir):
    wrapper = RepoWrapper.init(tmpdir)
    node = wrapper.commit_file('foo', content='Foo', message='Foo committed')
    ctx = wrapper.repo[node]
    assert ctx.description() == b'Foo committed'
    parents = ctx.parents()
    assert len(parents) == 1
    assert parents[0].rev() == NULL_REVISION
    assert parents[0].node() == NULL_ID

    del wrapper, ctx

    reloaded = RepoWrapper.load(tmpdir)
    rl_ctx = reloaded.repo[node]
    assert rl_ctx.description() == b'Foo committed'


def test_update(tmpdir):
    wrapper = RepoWrapper.init(tmpdir)
    wrapper.commit_file('foo', content='Foo 0')
    node1 = wrapper.commit_file('foo', content='Foo 1', return_ctx=False)
    foo = tmpdir.join('foo')
    assert foo.read() == 'Foo 1'

    wrapper.update('0')
    assert foo.read() == 'Foo 0'

    wrapper.update_bin(NULL_ID)
    assert not foo.isfile()

    wrapper.update_bin(node1)
    assert foo.read() == 'Foo 1'


@parametrize('meth', ['class', 'instance'])
def test_share(tmpdir, meth):
    main_path = tmpdir.join('main')
    dest_path = tmpdir.join('dest')
    main_wrapper = RepoWrapper.init(main_path)
    node0 = main_wrapper.commit_file('foo', message='Done in main')

    if meth == 'class':
        dest_wrapper = RepoWrapper.share_from_path(main_path, dest_path)
    else:
        dest_wrapper = main_wrapper.share(dest_path)

    dest_ctx = dest_wrapper.repo[node0]
    assert dest_ctx.description() == b'Done in main'

    node1 = dest_wrapper.commit_file(
        'foo', message='Done in dest', parent=node0)

    # we need to reload the main repo to see the new changeset
    reloaded = RepoWrapper.load(main_path)
    main_ctx = reloaded.repo[node1]
    assert main_ctx.description() == b'Done in dest'


def test_commit(tmpdir):
    """Demonstrates message auto generation and how to commit several files."""
    wrapper = RepoWrapper.init(tmpdir)
    (tmpdir / 'foo').write('foo')
    (tmpdir / 'bar').write('bar')
    ctx0 = wrapper.commit(('foo', 'bar'), add_remove=True)
    assert set(ctx0.files()) == {b'foo', b'bar'}


def test_commit_file_named_branch(tmpdir):
    """Demonstrate the use of commit_file with parent."""
    wrapper = RepoWrapper.init(tmpdir)
    ctx0 = wrapper.commit_file('foo', content='Foo 0')
    wrapper.commit_file('foo', content='Foo 1')
    ctxbr = wrapper.commit_file('foo', content='Foo branch',
                                parent=ctx0, branch='other')

    assert ctxbr.branch() == b'other'
    assert ctxbr.parents() == [ctx0]


def test_commit_file_parent_nodeid(tmpdir):
    """Demonstrate the use of commit_file with parent given as node id"""
    wrapper = RepoWrapper.init(tmpdir)
    node0 = wrapper.commit_file('foo', content='Foo 0', return_ctx=False)
    assert isinstance(node0, bytes)  # avoid tautologies

    wrapper.commit_file('foo', content='Foo 1')
    ctxbr = wrapper.commit_file('foo', content='Foo branch',
                                parent=node0, branch='other')

    assert ctxbr.branch() == b'other'
    assert [c.node() for c in ctxbr.parents()] == [node0]


def test_commit_file_time(tmpdir):
    """Demonstrate the utc_timestamp optional parameter."""
    wrapper = RepoWrapper.init(tmpdir)
    ctx = wrapper.commit_file('foo', content='Foo', utc_timestamp=123456)
    assert ctx.date() == (123456.0, 0)

    # floats are accepted, but get truncated
    ctx = wrapper.commit_file('foo', content='Foo2', utc_timestamp=12.34)
    assert ctx.date() == (12.0, 0)


def test_commit_file_parent(tmpdir):
    """Demonstrate the use of commit_file with parent"""
    wrapper = RepoWrapper.init(tmpdir)
    ctx0 = wrapper.commit_file('foo', content='Foo 0')
    wrapper.commit_file('foo', content='Foo 1')
    ctxbr = wrapper.commit_file('foo', content='Foo branch',
                                parent=ctx0)

    assert ctxbr.branch() == b'default'
    assert ctxbr.parents() == [ctx0]


def test_commit_file_random(tmpdir):
    """Demonstrate how random content is generated."""

    wrapper = RepoWrapper.init(tmpdir)
    node0 = wrapper.commit_file('foo')
    ctx1 = wrapper.commit_file('foo', parent=node0, return_ctx=True)
    ctx2 = wrapper.commit_file('foo', parent=node0, return_ctx=True)

    assert ctx1.p1() == ctx2.p1()
    assert ctx1 != ctx2


def test_phase(tmpdir):
    wrapper = RepoWrapper.init(tmpdir)
    node = wrapper.commit_file('foo', content='Foo 0')
    ctx = wrapper.repo[node]
    assert ctx.phase() == phases.draft

    wrapper.set_phase('public', ['.'], force=False)
    assert ctx.phase() == phases.public

    wrapper.set_phase('draft', ['.'], force=True)
    assert ctx.phase() == phases.draft


@parametrize('msg_kind', ('no-message', 'explicit-message'))
def test_remove_file(tmpdir, msg_kind):
    wrapper = RepoWrapper.init(tmpdir)
    wrapper.commit_file('foo', content='bar')
    assert tmpdir.join('foo').read() == 'bar'

    if msg_kind == 'no-message':
        passed_msg, expected_msg = (None, b'removing foo')
    else:
        passed_msg, expected_msg = ('explicit', b'explicit')

    ctx = wrapper.commit_removal('foo', message=passed_msg)
    assert ctx.description() == expected_msg
    assert b'foo' not in ctx
    assert b'foo' in ctx.p1()
    assert not tmpdir.join('foo').exists()


def test_empty_changeset(tmpdir):
    wrapper = RepoWrapper.init(tmpdir)
    root_ctx = wrapper.commit_file('foo', content='bar')

    ctx = wrapper.commit_empty(branch='new', message='empty')
    assert ctx.branch() == b'new'
    assert ctx.description() == b'empty'

    ctx = wrapper.commit_empty(branch='other', message='again',
                               parent=root_ctx)
    assert ctx.branch() == b'other'
    assert ctx.description() == b'again'


def test_extensibility_commit(tmpdir):
    class MyWrapper(RepoWrapper):
        def mark_repo(self, marker):
            self.repo.test_marker = marker

    MyWrapper.register_commit_option('mark', 'mark_repo')

    # registration worked, without side effects on the parent class
    assert 'mark' in MyWrapper.commit_option_handlers
    assert 'mark' not in RepoWrapper.commit_option_handlers

    wrapper = MyWrapper.init(tmpdir)
    ctx = wrapper.commit_file('foo', content='bar', mark="extended!")

    # mark_repo() was called as expected
    assert wrapper.repo.test_marker == 'extended!'

    # commit looks normal
    assert (tmpdir / 'foo').read() == 'bar'
    assert ctx.files() == [b'foo']
