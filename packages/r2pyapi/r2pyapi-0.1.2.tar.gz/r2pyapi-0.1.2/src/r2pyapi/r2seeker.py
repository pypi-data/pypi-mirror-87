from dataclasses import dataclass
from types import TracebackType
from typing import Generator, List, Optional, Type

import r2pipe

from .r2types import R2ByteSearchResult, R2Instruction
from .utils import hex_as_sring_prefix


@dataclass()
class R2SearchRegion:
    start_addr: int
    end_addr: int


class R2Seeker:
    def __init__(
        self, r2: r2pipe.open_sync.open, region: Optional[R2SearchRegion] = None
    ) -> None:
        self.r2 = r2
        self.region = region

    def __enter__(self) -> "R2Seeker":
        self.search_region_prev = self.get_search_region(self.r2)
        if self.region:
            self.set_search_region(self.r2, self.region)
        return self

    def __exit__(
        self,
        t: Optional[Type[BaseException]],
        v: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        self.set_search_region(self.r2, self.search_region_prev)

    def seek_instructions(
        self, asm_str: str
    ) -> Generator[Optional[R2Instruction], None, None]:
        raw_results = self.r2.cmdj(f"/aaj {asm_str}")
        if not raw_results:
            yield None
        for raw_result in raw_results:
            yield R2Instruction(**raw_result)

    def seek_byte_sequences(
        self, hex_array: List[int]
    ) -> Generator[Optional[R2ByteSearchResult], None, None]:
        raw_results = self.r2.cmdj(f"/j {hex_as_sring_prefix(hex_array)}")
        if not raw_results:
            yield None
        for raw_result in raw_results:
            yield R2ByteSearchResult(**raw_result)

    @staticmethod
    def get_pos(r2: r2pipe.open_sync.open) -> int:
        return int(r2.cmd("s").strip(), 16)

    @staticmethod
    def get_search_region(r2: r2pipe.open_sync.open) -> R2SearchRegion:
        return R2SearchRegion(
            int(r2.cmd("e search.from").strip(), 16),
            int(r2.cmd("e search.to").strip(), 16),
        )

    @staticmethod
    def set_search_region(r2: r2pipe.open_sync.open, region: R2SearchRegion) -> None:
        r2.cmd(f"e search.from = {hex(region.start_addr)}")
        r2.cmd(f"e search.to = {hex(region.end_addr)}")

    @staticmethod
    def clear_search_region(r2: r2pipe.open_sync.open) -> None:
        R2Seeker.set_search_region(
            r2, R2SearchRegion(0xFFFFFFFFFFFFFFFF, 0xFFFFFFFFFFFFFFFF)
        )
