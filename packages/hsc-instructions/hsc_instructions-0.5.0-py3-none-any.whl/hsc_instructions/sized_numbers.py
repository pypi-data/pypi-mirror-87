from __future__ import annotations

import typing

from hsc_instructions.parsable import Parsable


class UintOverflowError(OverflowError):
    def __init__(self, number: int, max_size: int, type_name: str) -> None:
        message = (
            f"Number {number} is too large for type {type_name}. "
            f"Its max size is {max_size}."
        )
        super().__init__(message)


class UnderflowError(Exception):
    def __init__(self, number: int, type_name: str) -> None:
        super().__init__(
            f"Number {number} is too small (below zero) for type {type_name}."
        )


UintUnderflowError = UnderflowError

TP = typing.TypeVar(
    "TP",
    bound="PositiveSizedNumber",
)


class PositiveSizedNumber(int):
    MAX: typing.ClassVar[int]

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls, *args, **kwargs)
        if self > self.MAX:
            raise UintOverflowError(self, self.MAX, cls.__name__)
        if self < 0:
            raise UnderflowError(self, cls.__name__)
        return self

    def __repr__(self) -> str:
        return f"{type(self).__name__}({super().__repr__()})"

    def __str__(self) -> str:
        return super().__repr__()

    @classmethod
    def from_int(cls, value: int) -> PositiveSizedNumber:
        return cls(value)

    @classmethod
    def from_fields(
        cls, fields: typing.Dict[typing.Tuple[str, ...], int]
    ) -> PositiveSizedNumber:
        return cls(fields[()])

    asm_code = __str__


class Uint5(PositiveSizedNumber):
    MAX = 0b11111


class Uint8(Parsable, PositiveSizedNumber):
    MAX = 0xFF


class Uint16(Parsable, PositiveSizedNumber):
    MAX = 0xFFFF


class Uint20(PositiveSizedNumber):
    MAX = 0xFFFFF
