# -*- coding: utf-8 -*-
import fnmatch
import os
import time
from collections import defaultdict
from typing import List, Optional, Sequence, Union

from zuper_commons.types import check_isinstance

from . import logger
from .types import DirPath, FilePath

__all__ = ["locate_files"]


# @contract(returns='list(str)', directory='str',
#           pattern='str|seq(str)', followlinks='bool')
def locate_files(
    directory: DirPath,
    pattern: Union[str, Sequence[str]],
    followlinks: bool = True,
    include_directories: bool = False,
    include_files: bool = True,
    normalize: bool = True,
    ignore_patterns: Optional[Sequence[str]] = None,
) -> List[FilePath]:
    if not os.path.exists(directory):
        msg = f'Root directory does not exist: {directory}'
        logger.warning(msg)
        return []
        # raise ValueError(msg)
    """
        pattern is either a string or a sequence of strings

        NOTE: if you do not pass ignore_patterns, it will use  MCDPConstants.locate_files_ignore_patterns

        ignore_patterns = ['*.bak']

        normalize = uses realpath
    """
    t0 = time.time()

    if ignore_patterns is None:
        ignore_patterns = []

    if isinstance(pattern, str):
        patterns = [pattern]
    else:
        patterns = list(pattern)
        for p in patterns:
            check_isinstance(p, str)

    # directories visited
    # visited = set()
    # visited_basename = set()
    # print('locate_files %r %r' % (directory, pattern))
    filenames = []

    def matches_pattern(x):
        return any(fnmatch.fnmatch(x, _) or (x == _) for _ in patterns)

    def should_ignore_resource(x):
        return any(fnmatch.fnmatch(x, _) or (x == _) for _ in ignore_patterns)

    def accept_dirname_to_go_inside(_root_, d_):
        if should_ignore_resource(d_):
            return False
        # XXX
        # dd = os.path.realpath(os.path.join(root_, d_))
        # if dd in visited:
        #     return False
        # visited.add(dd)
        return True

    def accept_dirname_as_match(_):
        return include_directories and not should_ignore_resource(_) and matches_pattern(_)

    def accept_filename_as_match(_):
        return include_files and not should_ignore_resource(_) and matches_pattern(_)

    ntraversed = 0
    for root, dirnames, files in os.walk(directory, followlinks=followlinks):
        ntraversed += 1
        dirnames[:] = [_ for _ in dirnames if accept_dirname_to_go_inside(root, _)]
        for f in files:
            # logger.info('look ' + root + '/' + f)
            if accept_filename_as_match(f):
                filename = os.path.join(root, f)
                filenames.append(filename)
        for d in dirnames:
            if accept_dirname_as_match(d):
                filename = os.path.join(root, d)
                filenames.append(filename)

    if normalize:
        real2norm = defaultdict(lambda: [])
        for norm in filenames:
            real = os.path.realpath(norm)
            real2norm[real].append(norm)
            # print('%s -> %s' % (real, norm))

        for k, v in real2norm.items():
            if len(v) > 1:
                msg = f"In directory:\n\t{directory}\n"
                msg += f"I found {len(v)} paths that refer to the same file:\n"
                for n in v:
                    msg += f"\t{n}\n"
                msg += f"refer to the same file:\n\t{k}\n"
                msg += "I will silently eliminate redundancies."
                # logger.warning(msg) # XXX

        filenames = list(real2norm.keys())

    seconds = time.time() - t0
    if seconds > 5:
        n = len(filenames)
        nuniques = len(set(filenames))
        msg = (
            f"{seconds:.1f} s for locate_files({directory},{pattern}): {ntraversed} traversed, "
            f"found {n} filenames ({nuniques} uniques)")

        logger.debug(msg)
    return filenames
