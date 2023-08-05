from types import TracebackType
from typing import List, Optional, Type

import r2pipe

from .r2seeker import R2Seeker
from .utils import hex_as_string


class R2Reader:
    def __init__(self, r2: r2pipe.open_sync.open) -> None:
        self.r2 = r2

    def __enter__(self) -> "R2Reader":
        self.pos_prev = R2Seeker.get_pos(self.r2)
        return self

    def __exit__(
        self,
        t: Optional[Type[BaseException]],
        v: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        self.r2.cmd(f"s {hex(self.pos_prev)}")

    def read_bytes_at(self, at: int, size: int) -> List[int]:
        self.r2.cmd(f"s {hex(at)}")
        return self.r2.cmdj(f"pxj {hex(size)}")

    def read_bytes_as_hex_str_at(self, at: int, size: int) -> str:
        return hex_as_string(self.read_bytes_at(at, size))
