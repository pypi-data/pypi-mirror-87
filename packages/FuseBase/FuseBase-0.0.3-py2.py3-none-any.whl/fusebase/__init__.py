from time import time
from typing import NamedTuple, List, Iterable, Dict, Tuple, Union, Optional, Callable, Any
from stat import S_IFDIR, S_IFLNK, S_IFREG
from pathlib import Path
from errno import *
import os


BLK_SIZE = 512  # must be power of two on macos

try:
    UID = os.getuid()
    GID = os.getgid()

except:
    UID = 0
    GID = 0

ROOT = '/'
DOTS = ['.', '..']


class Stat(NamedTuple):
    st_dev: int = None
    st_ino: int = None
    st_nlink: int = None
    st_mode: int = None
    st_uid: int = None
    st_gid: int = None
    st_rdev: int = None
    st_size: int = None
    st_blksize: int = None
    st_blocks: int = None
    st_flags: int = None
    st_gen: int = None
    st_lspare: int = None
    st_qspare: int = None
    st_atime: float = None
    st_mtime: float = None
    st_ctime: float = None
    st_birthtime: float = time()

    def with_vals(self, **kwargs) -> 'Stat':
        vals = self.as_dict()
        vals.update(kwargs)
        return Stat(**vals)

    def as_dict(self) -> Dict[str, Union[int, float]]:
        return {
            k: v
            for k, v in self._asdict().items()
            if v is not None
        }
    
    
class DirStat(Stat):
    st_nlink: int = 2
    st_blocks: int = 1
    st_size: int = BLK_SIZE

        
class FileStat(Stat):
    st_nlink: int = 1

        
class StatVFS(NamedTuple):
    f_bsize: int = None
    f_frsize: int = None
    f_blocks: int = None
    f_bfree: int = None
    f_bavail: int = None
    f_files: int = None
    f_ffree: int = None
    f_favail: int = None
    f_fsid: int = None
    f_flag: int = None
    f_namemax: int = None

    def as_dict(self) -> dict:
        return {
            k: v
            for k, v in self._asdict().items()
            if v is not None
        }
