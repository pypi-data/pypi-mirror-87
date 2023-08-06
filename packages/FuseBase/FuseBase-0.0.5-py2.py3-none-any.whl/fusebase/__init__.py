from time import time
from typing import NamedTuple, Dict, Union, Optional
# from stat import S_IFDIR, S_IFLNK, S_IFREG
# from pathlib import Path
# from errno import *
import logging
import os


BLK_SIZE = 512  # must be power of two on macos

try:
    UID = os.getuid()
    GID = os.getgid()

except AttributeError:
    logging.debug("Defaulting UID & GID to 0.")
    UID = 0
    GID = 0

ROOT = '/'
DOTS = ['.', '..']


class Stat(NamedTuple):
    st_dev: Optional[int] = None
    st_ino: Optional[int] = None
    st_nlink: Optional[int] = None
    st_mode: Optional[int] = None
    st_uid: Optional[int] = None
    st_gid: Optional[int] = None
    st_rdev: Optional[int] = None
    st_size: Optional[int] = None
    st_blksize: Optional[int] = None
    st_blocks: Optional[int] = None
    st_flags: Optional[int] = None
    st_gen: Optional[int] = None
    st_lspare: Optional[int] = None
    st_qspare: Optional[int] = None
    st_atime: Optional[float] = None
    st_mtime: Optional[float] = None
    st_ctime: Optional[float] = None
    st_birthtime: float = time()

    def with_vals(self, **kwargs) -> 'Stat':
        vals = self.as_dict()
        vals.update(kwargs)
        return Stat(**vals)

    def as_dict(self) -> Dict[str, Union[int, float]]:
        return {
            key: val
            for key, val in self._asdict().items()
            if val is not None
        }


class DirStat(Stat):
    st_nlink: int = 2
    st_blocks: int = 1
    st_size: int = BLK_SIZE


class FileStat(Stat):
    st_nlink: int = 1


class StatVFS(NamedTuple):
    f_bsize: Optional[int] = None
    f_frsize: Optional[int] = None
    f_blocks: Optional[int] = None
    f_bfree: Optional[int] = None
    f_bavail: Optional[int] = None
    f_files: Optional[int] = None
    f_ffree: Optional[int] = None
    f_favail: Optional[int] = None
    f_fsid: Optional[int] = None
    f_flag: Optional[int] = None
    f_namemax: Optional[int] = None

    def as_dict(self) -> Dict[str, int]:
        return {
            key: val
            for key, val in self._asdict().items()
            if val is not None
        }
