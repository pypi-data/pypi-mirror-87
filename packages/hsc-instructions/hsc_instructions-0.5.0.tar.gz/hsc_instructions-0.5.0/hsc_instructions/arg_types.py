"""Enums for Tokens."""
from __future__ import annotations

import dataclasses
import enum
import typing as tp

from hsc_instructions.errors import DecodeKeyError
from hsc_instructions.parsable import FakeParsable, Parsable, ParseMethod
from hsc_instructions.sized_numbers import Uint5, Uint16

__all__ = [
    "Register",
    "Shift",
    "ShiftType",
    "PointerDeref",
    "Label",
    "DecodeEnumFromValueMixin",
    "ShiftPointerDeref",
    "Uint16PointerDeref",
]

TC = tp.TypeVar("TC", bound="DecodeEnumFromValueMixin")


class DecodeEnumFromValueMixin:
    @classmethod
    def from_int(cls: tp.Type[TC], value: int) -> TC:
        try:
            return next(
                enum_mem for enum_mem in cls if enum_mem.value == value  # type: ignore
            )
        except StopIteration:
            raise DecodeKeyError(
                f"No {cls.__name__} with encoding {value}", None
            ) from None


class ParsableDecodeEnumFromValue(Parsable, DecodeEnumFromValueMixin):
    pass


class Register(ParsableDecodeEnumFromValue, enum.IntEnum):
    """
    Enum of the registers
    """

    r0 = 0
    r1 = 1
    r2 = 2
    r3 = 3
    r4 = 4
    r5 = 5
    r6 = 6
    r7 = 7
    r8 = 8
    r9 = 9
    r10 = 10
    r11 = 11
    r12 = 12
    r13 = 13
    r14 = 14
    r15 = 15

    # These have to be accessed using their prefix to require the programmer
    # to acknowledge they're in the right mode.
    mcr_s = 12
    ivt_i = 12

    sp = 13
    lr = 14
    pc = 15

    @classmethod
    def from_fields(cls, fields: tp.Dict[tp.Tuple[str, ...], int]) -> Register:
        return cls.from_int(fields[()])

    def asm_code(self) -> str:
        return self.name


class NonRmRegister(FakeParsable[Register]):
    """Hacky solution to get around the inability to subclass Register"""

    real_class = Register

    @classmethod
    def from_int(cls, value: int) -> Register:
        reg = cls.real_class.from_int(value)
        if cls.real_class.pc is reg:
            raise DecodeKeyError(
                "register pc (r15) can only take on the role of Rm", None
            ) from None
        return reg

    from_fields = Register.from_fields


class Mode(DecodeEnumFromValueMixin, enum.IntEnum):
    USER = 0
    SUPERVISOR = 1
    IRQ = 2
    FLAGS = 3

    def internal(self) -> int:
        """ Returns the internal (CPU) representation of the mode """
        if self is Mode.FLAGS:
            raise ValueError(
                "Mode FLAGS is not a real mode; only exists in the encoding"
            )
        return {self.SUPERVISOR: 0, self.IRQ: 1, self.USER: 2}[self]

    @classmethod
    def from_internal_int(cls, value: int) -> Mode:
        """ Returns mode from the internal (CPU) representation of the mode"""
        try:
            return next(mem for mem in cls if mem.internal() == value)
        except (ValueError, StopIteration):
            raise DecodeKeyError(
                f"No valid mode with internal value {value}", None
            ) from None


@dataclasses.dataclass
class ModedRegister(Parsable):
    mode: Mode
    register: Register
    mode_suffixes: tp.ClassVar[tp.Dict[Mode, str]] = {
        Mode.USER: "_u",
        Mode.IRQ: "_i",
        Mode.SUPERVISOR: "_s",
    }
    str_suffixes: tp.ClassVar[tp.Dict[str, Mode]] = {
        value: key for key, value in mode_suffixes.items()
    }
    reg_from_int: tp.ClassVar[tp.Callable[[int], Register]] = Register.from_int

    @classmethod
    def flag(cls) -> ModedRegister:
        # Register doesn't matter
        return cls(Mode.FLAGS, Register.r0)

    def asm_code(self) -> str:
        if self.mode is Mode.FLAGS:
            return "flags"
        return self.register.asm_code() + self.mode_suffixes[self.mode]

    __str__ = asm_code

    @classmethod
    def from_fields(cls, fields: tp.Dict[tp.Tuple[str, ...], int]) -> ModedRegister:
        mode = Mode.from_int(fields[("mode",)])
        register = cls.reg_from_int(fields[("register",)])
        return cls(mode, register)


class NonRmModedRegister(ModedRegister):
    reg_from_int: tp.ClassVar[tp.Callable[[int], Register]] = NonRmRegister.from_int


ShiftType = enum.IntEnum(
    "ShiftType",
    {"<<": 0, ">>": 1, "ser": 2, "ror": 3},
    type=ParsableDecodeEnumFromValue,
)


@dataclasses.dataclass(init=False)
class Label(Parsable):
    name: tp.Optional[str]
    address: tp.Optional[Uint16]

    def __init__(
        self, name: tp.Optional[str] = None, address: tp.Optional[int] = None
    ) -> None:
        if name is None and address is None:
            raise ValueError("Either the name or address must be specified")
        self.name = name
        self.address = Uint16(address) if address is not None else address

    @classmethod
    def from_fields(cls, fields: tp.Dict[tp.Tuple[str, ...], int]) -> Label:
        return cls(address=fields[()])

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name}, address={self.address})"

    def __str__(self) -> str:
        return self.name if self.name is not None else str(self.address)

    asm_code = __str__


@dataclasses.dataclass
class Shift(Parsable):
    type: ShiftType
    register: Register
    amount: Uint5

    @classmethod
    def from_fields(cls, fields: tp.Dict[tp.Tuple[str, ...], int]) -> Shift:
        shift_type = ShiftType.from_int(fields[("type",)])  # type: ignore
        shift_register = Register(Register.from_int(fields[("register",)]))
        shift_amount = Uint5(fields[("amount",)])
        return cls(shift_type, shift_register, shift_amount)

    def asm_code(self) -> str:
        shift = f"{self.type.name} {self.amount.asm_code()}" if self.amount else ""
        return f"{self.register.asm_code()} {shift}"


TI = tp.TypeVar("TI", Uint16, Shift)


@dataclasses.dataclass
class PointerDeref(Parsable, tp.Generic[TI]):
    register: Register
    increment: TI
    increment_parse: tp.ClassVar[ParseMethod]

    def asm_code(self) -> str:
        return f"[{self.register.asm_code()} + {self.increment.asm_code()}]"


# These are seperate because they have different binary encodings
class Uint16PointerDeref(PointerDeref[Uint16]):
    increment_parse = Uint16.parse

    @classmethod
    def from_fields(
        cls, fields: tp.Dict[tp.Tuple[str, ...], int]
    ) -> Uint16PointerDeref:
        register = Register.from_int(fields[("register",)])
        increment = Uint16(fields[("increment",)])
        return cls(register, increment)


class ShiftPointerDeref(PointerDeref[Shift]):
    increment_parse = Shift.parse

    @classmethod
    def from_fields(cls, fields: tp.Dict[tp.Tuple[str, ...], int]) -> ShiftPointerDeref:
        register = Register(Register.from_int(fields[("register",)]))
        shift = Shift.from_fields(
            {
                name[1:]: value
                for name, value in fields.items()
                if name[0] == "increment"
            }
        )
        return cls(register, shift)
