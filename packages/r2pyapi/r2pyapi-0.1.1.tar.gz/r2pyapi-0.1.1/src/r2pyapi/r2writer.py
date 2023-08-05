import sys
from types import TracebackType
from typing import List, Optional, Type

import r2pipe

from .r2seeker import R2Seeker
from .utils import hex_as_string


class R2Writer:
    block_size: int = 0x500

    @staticmethod
    def r2_is_write_mode(r2: r2pipe.open_sync.open) -> bool:
        return r2.cmdj("ij")["core"]["mode"][1] == "w"

    def __init__(self, r2: r2pipe.open_sync.open) -> None:
        if not self.r2_is_write_mode(r2):
            print("NOTE: reopening r2pipe with write mode", file=sys.stderr)
            r2.cmd("oo+")
        self.r2 = r2

    def __enter__(self) -> "R2Writer":
        self.pos_prev = R2Seeker.get_pos(self.r2)
        return self

    def __exit__(
        self,
        t: Optional[Type[BaseException]],
        v: Optional[BaseException],
        tb: Optional[TracebackType],
    ):
        self.r2.cmd(f"s {hex(self.pos_prev)}")

    def _write_bytes_at(
        self, payload: List[int], address_at: int, write_cmd: str
    ) -> None:
        self.r2.cmd(f"s {hex(address_at)}")
        for i in range(int(len(payload) / self.block_size)):
            hex_as_string(payload[self.block_size * i: self.block_size * (i + 1)])
            self.r2.cmd(
                f"{write_cmd} {hex_as_string(payload[self.block_size * i:self.block_size * (i + 1)])}; s+{hex(self.block_size)};"
            )

    def overwrite_bytes(self, payload: List[int], address_at: int) -> None:
        self._write_bytes_at(payload, address_at, "wx")

    def insert_bytes(self, payload: List[int], address_at: int) -> None:
        self._write_bytes_at(payload, address_at, "wex")
