import sys
import typing

from hsc_instructions.errors import error_print

__all__ = [
    "chunk",
    "getattributes",
    "exit_open",
    "twos_complement",
    "bit_twos_complement",
]

T = typing.TypeVar("T")


def chunk(iterable: typing.Iterable[T], size: int) -> typing.Iterator[typing.List[T]]:
    group = []
    for item in iterable:
        group.append(item)
        if len(group) == size:
            yield group
            group = []
    if group:
        message = (
            "Extra data in iterable; Iterable cannot split into "
            f"chunks of size {size} without extra data."
        )
        raise ValueError(message)


def exit_open(*args, **kwargs) -> typing.IO:
    try:
        return open(*args, **kwargs)
    except OSError as exc:
        error_print(exc.strerror)
        sys.exit(exc.errno)


def getattributes(obj: object, *fields: str) -> object:
    for field in fields:
        obj = getattr(obj, field)
    return obj


def twos_complement(num: int, byte_count: int) -> int:
    return bit_twos_complement(num, byte_count * 8)


# Modified from https://stackoverflow.com/a/37075643
def bit_twos_complement(val: int, nbits: int) -> int:
    """Compute the 2's complement of int value val"""
    if val < 0:
        val = (1 << nbits) + val
    else:
        if (val & (1 << (nbits - 1))) != 0:
            # If sign bit is set.
            # compute negative value.
            val = val - (1 << nbits)
    if val > (2 ** nbits):
        raise ValueError(f"nbits <{nbits}> to few to represent val")
    return val
