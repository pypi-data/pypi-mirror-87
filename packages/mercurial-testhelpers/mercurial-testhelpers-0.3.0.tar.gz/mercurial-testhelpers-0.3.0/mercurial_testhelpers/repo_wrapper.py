# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
# SPDX-License-Identifier: GPL-2.0-or-later
"""Helpers for automatic tests.

These allow both high level operation on testing repos, and lower level
calls and introspections, making it possible to test more exhaustively inner
code paths that with `.t` tests, which are really functional tests.
"""
import os
from mercurial import (
    cmdutil,
    commands,
    hg,
    node,
    phases,
)
import random
import time

from .util import as_bytes
from .ui import make_ui

# re-exports for stability
NULL_REVISION = node.nullrev  # pragma: no cover
NULL_ID = node.nullid

try:
    phase_names = phases.cmdphasenames
except AttributeError:  # hg<4.8
    phase_names = phases.phasenames[:3]


class RepoWrapper(object):
    """Facilities for handling Mercurial repositories.

    As the name suggests, this is a wrapper class that embeds an
    instance of :class:`mercurial.localrepo.localrepo` as :attr:`repo`.

    It provides helper methods for initialization and content creation or
    mutation, both in the working directory and in changesets.

    For convenience, these high level methods accept both unicode and bytes
    strings. The path objects used by pytest can be used readily where
    a path is expected. There is one notable exception to this principle:
    the generic :meth:`command`, which is designed to forward its arguments
    to the underlying Mercurial command directly.

    All return values that are from Mercurial are untouched, hence strings
    would be bytes.

    All conversions to bytes are done with the UTF-8 codec. If that doesn't
    suit your case, simply encode your strings before hand.

    Running unmodified tests based on this helper on a non UTF-8 filesystem
    is not supported at this point, but it could be done, we are open to
    suggestions.
    """

    def __init__(self, repo):
        self.repo = repo

    @classmethod
    def init(cls, path, base_ui=None, config=None):
        init = cmdutil.findcmd(b'init', commands.table)[1][0]
        ui = make_ui(base_ui, config)

        path = as_bytes(path)
        init(ui, dest=path)
        return cls(hg.repository(ui, path))

    @classmethod
    def load(cls, path, base_ui=None, config=None):
        ui = make_ui(base_ui, config=config)
        return cls(hg.repository(ui, as_bytes(path)))

    @classmethod
    def share_from_path(cls, src_path, dest_path,
                        ui=None, base_ui=None, config=None,
                        **share_opts):
        """Create a new repo as the ``share`` command would do.

        :param ui: if specified, will be copied and used for the new repo
                   creation through ``share``
        :param config: only if ``ui`` is not specified, will be used to
                       create a new ``ui`` instance
        :param base_ui: only if ``ui`` is not specified, will be used to
                       create a new :class:`ui` instance
        :param share_opts: passed directly to :func:`hg.share()`
        :return: wrapper for the new repo
        """
        if ui is None:
            ui = make_ui(base_ui, config=config)
        else:
            # TODO not enough for environ independence
            ui = ui.copy()

        # the 'share' command defined by the 'share' extension, is just a thin
        # wrapper around `hg.share()`, which furthermore returns a repo object.
        repo = hg.share(ui, as_bytes(src_path), dest=as_bytes(dest_path),
                        **share_opts)
        if repo is None:
            return cls.load(dest_path)  # hg<=4.3
        return cls(repo)  # hg>4.3

    def share(self, dest_path, **share_opts):
        return self.share_from_path(self.repo.root, dest_path,
                                    ui=self.repo.ui, **share_opts)

    def command(self, name, *args, **kwargs):
        cmd = cmdutil.findcmd(as_bytes(name), commands.table)[1][0]
        repo = self.repo
        return cmd(repo.ui, repo, *args, **kwargs)

    def random_content(self):
        return "random: {}\n\nparent: {}\n".format(
            random.random(),
            node.hex(self.repo.dirstate.p1()))

    def prepare_wdir(self, parent=None):
        if parent is not None:
            if isinstance(parent, bytes):
                self.update_bin(parent)
            else:
                self.update(parent.hex())

    def set_dirstate_branch(self, branch):
        self.repo.dirstate.setbranch(as_bytes(branch))

    commit_option_handlers = dict(branch='set_dirstate_branch',
                                  )

    @classmethod
    def register_commit_option(cls, name, handler):
        super_registry = super(cls, cls).commit_option_handlers
        registry = cls.commit_option_handlers
        if registry is super_registry:
            registry = cls.commit_option_handlers = super_registry.copy()

        registry[name] = handler

    def commit(self, rel_paths,
               message=None,
               utc_timestamp=None,
               user=None,
               add_remove=False, return_ctx=True, **opts):
        """Commit the current state of working directory.

        This method does not perform any update nor does it change the dirstate
        before committing. See :meth:`prepare_wdir` for helpers about that.

        :param rel_paths: any iterable of relative paths from the repository
           root. Each can be specified as :class:`str` or :class:`bytes`
        :param message: commit message. If not specified, a randomized value
           is used.
        :param user: full user name and email, as in ``ui.username`` config
                     option. Can be :class:`str` or :class:`bytes`
        :param utc_timestamp: seconds since Epoch UTC. Good enough for
                              tests without ambiguity. Can be float (only
                              seconds will be kept). Defaults to
                              ``time.time()``
        :param return_ctx: if ``True``, returns a :class:`changectx` instance
                           and a binary node id otherwise, which can be more
                           straightforward and faster in some cases.
        :returns: :class:`changectx` instance or binary node id for the
                  generated commit, according to ``return_ctx``.
        """
        repo = self.repo

        if utc_timestamp is None:
            utc_timestamp = time.time()

        if user is None:
            user = repo.ui.config(b'ui', b'username')

        if message is None:
            message = self.random_content()

        def commitfun(ui, repo, message, match, opts):
            return repo.commit(message,
                               as_bytes(user),
                               (utc_timestamp, 0),
                               match=match,
                               editor=False,
                               extra=None,
                               )

        for opt, opt_value in opts.items():
            handler = self.commit_option_handlers[opt]
            getattr(self, handler)(opt_value)

        new_node = cmdutil.commit(repo.ui, repo, commitfun,
                                  (os.path.join(repo.root, as_bytes(rel_path))
                                   for rel_path in rel_paths),
                                  {b'addremove': add_remove,
                                   b'message': as_bytes(message),
                                   })
        return repo[new_node] if return_ctx else new_node

    def commit_file(self, relative_path,
                    content=None, message=None,
                    parent=None,
                    **commit_opts):
        """Write content at relative_path and commit in one call.

        This is meant to allow fast and efficient preparation of
        testing repositories. To do so, it goes a bit lower level
        than the actual commit command, so is not suitable to test specific
        commit options, especially if through extensions.

        This leaves the working directoy updated at the new commit.

        :param relative_path: relative path from repository root. If existing,
           will be overwritten by `content`
        :param content: what's to be written in ``relative_path``.
                        If not specified, will be replaced by random content.
        :param parent: binary node id or :class:`changectx` instance.
                       If specified, the repository is
                       updated to it first. Useful to produce branching
                       histories. This is single valued, because the purpose
                       of this method is not to produce merge commits.
        :param commit_opts: additional kwargs as in :meth:`commit`
        :returns: same as :meth:`commit`
        """
        repo = self.repo
        path = os.path.join(repo.root, as_bytes(relative_path))
        self.prepare_wdir(parent=parent)

        if content is None:
            content = self.random_content()
        content = as_bytes(content)

        if message is None:
            message = content

        with open(path, 'wb') as fobj:
            fobj.write(content)

        return self.commit((path, ), message=message, add_remove=True,
                           **commit_opts)

    def commit_removal(self, relative_path, parent=None, message=None,
                       **commit_opts):
        """Make a commit removing the given file.

        :param commit_opts: see :meth:`commit` except for ``add_removed`` which
           is ignored (forced to ``True``).
        """
        commit_opts.pop('add_remove', None)
        if message is None:
            message = b"removing %s" % as_bytes(relative_path)

        self.prepare_wdir(parent=parent)
        os.unlink(os.path.join(self.repo.root, as_bytes(relative_path)))
        return self.commit((relative_path, ),
                           message=as_bytes(message),
                           add_remove=True,
                           **commit_opts)

    def commit_empty(self, parent=None, **commit_opts):
        self.prepare_wdir(parent=parent)
        return self.commit((), **commit_opts)

    def update_bin(self, bin_node, **opts):
        """Update to a revision specified by its node in binary form.

        This is separated in order to avoid ambiguities
        """
        # maybe we'll do something lower level later
        self.update(node.hex(bin_node), **opts)

    def update(self, rev, hidden=False):
        repo = self.repo.unfiltered() if hidden else self.repo
        cmdutil.findcmd(b'update', commands.table)[1][0](repo.ui, repo,
                                                         as_bytes(rev))

    def set_phase(self, phase_name, revs, force=True):
        repo = self.repo
        opts = dict(force=force, rev=[as_bytes(r) for r in revs])
        phase_name_bytes = as_bytes(phase_name)
        opts.update((phn.decode(), phn == phase_name_bytes)
                    for phn in phase_names)
        cmdutil.findcmd(b'phase', commands.table)[1][0](repo.ui, repo, **opts)
