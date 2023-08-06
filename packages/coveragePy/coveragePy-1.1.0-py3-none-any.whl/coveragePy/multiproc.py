# Licensed under the Apache License: http://www.apache.org/licenses/LICENSE-2.0
# For details: https://bitbucket.org/ned/coveragepy/src/default/NOTICE.txt

"""Monkey-patching to add multiprocessing support for coverage.py"""

import multiprocessing
import multiprocessing.process
import os
import sys

from coverage.misc import contract

# An attribute that will be set on the module to indicate that it has been
# monkey-patched.
PATCHED_MARKER = "_coverage$patched2"

# The environment variable that specifies the rcfile for subprocesses.
COVERAGE_RCFILE_ENV = "_COVERAGE_RCFILE"


if sys.version_info >= (3, 4):
    BaseProcess = multiprocessing.process.BaseProcess
else:
    BaseProcess = multiprocessing.Process

original_bootstrap = BaseProcess._bootstrap


class ProcessWithCoverage(BaseProcess):
    """A replacement for multiprocess.Process that starts coverage."""

    def _bootstrap(self):
        """Wrapper around _bootstrap to start coverage."""
        # avoid circular import
        from coveragePy.coverage_logger import CoverageLoggerThread
        thread_cov = CoverageLoggerThread(main=False)
        thread_cov.start()
        try:
            return original_bootstrap(self)
        finally:
            thread_cov.shutdown()
            thread_cov.join()


class Stowaway(object):
    """An object to pickle, so when it is unpickled, it can apply
    the monkey-patch in the newly created process."""
    def __init__(self, rcfile):
        self.rcfile = rcfile

    def __getstate__(self):
        return {'rcfile': self.rcfile}

    def __setstate__(self, state):
        patch_multiprocessing(state['rcfile'])


@contract(rcfile=str)
def patch_multiprocessing(rcfile):
    """Monkey-patch the multiprocessing module.

    This enables coverage measurement of processes started by multiprocessing.
    This involves aggressive monkey-patching.

    `rcfile` is the path to the rcfile being used.

    """

    if hasattr(multiprocessing, PATCHED_MARKER):
        return

    if sys.version_info >= (3, 4):
        BaseProcess._bootstrap = ProcessWithCoverage._bootstrap
    else:
        multiprocessing.Process = ProcessWithCoverage

    # Set the value in ProcessWithCoverage that will be pickled into the child
    # process.
    os.environ[COVERAGE_RCFILE_ENV] = rcfile

    # When spawning processes rather than forking them, we have no state in the
    # new process.  We sneak in there with a Stowaway: we stuff one of our own
    # objects into the data that gets pickled and sent to the sub-process. When
    # the Stowaway is unpickled, it's __setstate__ method is called, which
    # re-applies the monkey-patch.
    # Windows only spawns, so this is needed to keep Windows working.
    try:
        from multiprocessing import spawn
        original_get_preparation_data = spawn.get_preparation_data
    except (ImportError, AttributeError):
        pass
    else:
        def get_preparation_data_with_stowaway(name):
            """Get the original preparation data, and also insert our stowaway.
            """
            d = original_get_preparation_data(name)
            d['stowaway'] = Stowaway(rcfile)
            return d

        spawn.get_preparation_data = get_preparation_data_with_stowaway

    setattr(multiprocessing, PATCHED_MARKER, True)