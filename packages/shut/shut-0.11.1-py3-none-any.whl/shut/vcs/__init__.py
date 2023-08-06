
"""
Abstraction of a version control system for the purpose of the interaction by Shut.
"""

import abc
import typing as t
from pathlib import Path


class AbstractVCS(metaclass=abc.ABCMeta):

  def __init__(self, root: Path) -> None:
    self._root = root

  def __repr__(self) -> str:
    return f'{type(self).__name__}(root={self.root!r})'

  def root(self) -> Path:
    return self._root


def detect_vcs(directory: Path) -> t.Optional[AbstractVCS]:
  """
  Detects a VCS in the specified *directory*, or any of it's parent directories. Currently
  supports Git only.
  """

  from .git import GitVCS

  while directory != Path(directory.root):
    if directory.joinpath('.git').exists():
      return GitVCS(directory)
    directory = directory.parent

  return None
