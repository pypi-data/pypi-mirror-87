from typing import List


def u32_to_u8_array(a: int) -> List[int]:
    return [
        a & 0xFF,
        (a >> 8) & 0xFF,
        (a >> 16) & 0xFF,
        (a >> 24) & 0xFF,
    ]


def hex_as_string(a: List[int]) -> str:
    return "".join(f"{i:02x}" for i in a)


def hex_as_sring_prefix(a: List[int]) -> str:
    return "".join(fr"\x{i:02x}" for i in a)
