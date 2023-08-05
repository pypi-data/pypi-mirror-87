from __future__ import annotations

import ctypes
import dataclasses
import enum
import functools
import typing as tp

from hsc_instructions.arg_types import (
    Label,
    ModedRegister,
    NonRmRegister,
    PointerDeref,
    Register,
    Shift,
    ShiftPointerDeref,
    Uint16PointerDeref,
    NonRmModedRegister,
)
from hsc_instructions.sized_numbers import Uint8, Uint16


def format_fields(
    **kwargs: int,
) -> tp.List[tp.Tuple[str, tp.Type[ctypes.c_uint], int]]:
    assert sum(kwargs.values()) == 20
    encoding = [
        ("opcode", ctypes.c_uint, 8),
        ("rd", ctypes.c_uint, 4),
        *((name, ctypes.c_uint, value) for name, value in kwargs.items()),
    ]
    return encoding


class EncodingType(enum.Enum):
    I = format_fields(rm=4, imm=16)  # noqa
    R = format_fields(rm=4, rn=4, shift=5, shift_type=2, register_bank=2, _padding=3)
    J = format_fields(address=20)

    # To get around enums not allowing the definition of multiple values
    @functools.cached_property
    def encoding_class(self) -> tp.Type[BinaryInstruction]:
        encodings = {
            self.I: I_BinaryInstruction,
            self.R: R_BinaryInstruction,
            self.J: J_BinaryInstruction,
        }
        return encodings[self]  # type: ignore


class BinaryInstruction(ctypes.BigEndianStructure):
    opcode: int
    rd: int

    def to_bytes(self) -> bytes:
        return bytes(self)


class I_BinaryInstruction(BinaryInstruction):
    rm: int
    imm: int

    _fields_ = EncodingType.I.value


class R_BinaryInstruction(BinaryInstruction):
    rm: int
    rn: int
    shift: int
    shift_type: int
    register_bank: int

    _fields_ = EncodingType.R.value


class J_BinaryInstruction(BinaryInstruction):
    address: int

    _fields_ = EncodingType.J.value


@dataclasses.dataclass(init=False)
class EncodingSlot:
    arg_index: int
    # Allows multiple field accesses
    field: tp.Sequence[str]

    def __init__(self, arg_index: int, *fields: str) -> None:
        self.arg_index = arg_index
        self.field = fields

    def reversed_index(self) -> EncodingSlot:
        return type(self)(-self.arg_index - 1, *self.field)


@dataclasses.dataclass
class InstructionInfo:
    """
    Information about the instruction

    types: The corrosponding types of the instruction arguments
    encoding_slots: Dict of the slot on the encoding name and where to get its
    value in the instruction's args
    value: The argument's value in the encoding
    encoding: The instruction's encoding
    """

    types: tp.Sequence[tp.Type[InstructionArgTypes]]
    encoding_slots: tp.Dict[str, EncodingSlot]
    value: int
    encoding_type: EncodingType

    def __init__(
        self,
        types: tp.Sequence[tp.Type[InstructionArgTypes]],
        encoding_slots: tp.Dict[str, EncodingSlot],
        value: int,
        encoding_type: EncodingType,
    ) -> None:
        self.types = types
        self.encoding_slots = encoding_slots
        self.encoding_type = encoding_type
        self.value = Uint8(value)

    @classmethod
    def nop(cls, nop_value: int) -> MultInstructionInfo:
        return MultInstructionInfo((cls((), {}, nop_value, EncodingType.J),))

    @classmethod
    def register_and_register_or_uint20(
        cls, instruction_value_register: int, instruction_value_imm: int
    ) -> MultInstructionInfo:
        return MultInstructionInfo(
            (
                cls.register_and_uint20(instruction_value_imm)[0],
                cls.two_register(instruction_value_register)[0],
            )
        )

    @classmethod
    def two_register_and_uint20(cls, instruction_value: int) -> MultInstructionInfo:
        return MultInstructionInfo(
            (
                cls(
                    (NonRmRegister, Register, Uint16),
                    {
                        "rd": EncodingSlot(0),
                        "rm": EncodingSlot(1),
                        "imm": EncodingSlot(2),
                    },
                    instruction_value,
                    EncodingType.I,
                ),
            )
        )

    @classmethod
    def two_register_and_shift_or_uint20(
        cls, instruction_value_shift: int, instruction_value_imm: int
    ) -> MultInstructionInfo:
        return MultInstructionInfo(
            (
                cls.two_register_and_shift(instruction_value_shift)[0],
                cls.two_register_and_uint20(instruction_value_imm)[0],
            )
        )

    @classmethod
    def two_register(cls, instruction_value_reg: int) -> MultInstructionInfo:
        return MultInstructionInfo(
            (
                cls(
                    (NonRmRegister, Register),
                    {
                        "rd": EncodingSlot(0),
                        "rm": EncodingSlot(1),
                    },
                    instruction_value_reg,
                    EncodingType.R,
                ),
            )
        )

    @classmethod
    def register_and_pointer_deref_with_imm_or_shift_or_register(
        cls,
        instruction_value_imm: int,
        instruction_value_reg: int,
        instruction_value_shift: int,
    ) -> MultInstructionInfo:
        return MultInstructionInfo(
            (
                cls(
                    (NonRmRegister, Uint16PointerDeref),
                    {
                        "rd": EncodingSlot(0),
                        "rm": EncodingSlot(1, "register"),
                        "imm": EncodingSlot(1, "increment"),
                    },
                    instruction_value_imm,
                    EncodingType.I,
                ),
                cls(
                    (NonRmRegister, ShiftPointerDeref),
                    {
                        "rd": EncodingSlot(0),
                        "rm": EncodingSlot(1, "register"),
                        "rn": EncodingSlot(1, "increment", "register"),
                        "shift_type": EncodingSlot(1, "increment", "type"),
                        "shift": EncodingSlot(1, "increment", "amount"),
                    },
                    instruction_value_shift,
                    EncodingType.R,
                ),
                cls.two_register(instruction_value_reg)[0],
            )
        )

    @classmethod
    def uint8(cls, instruction_value: int) -> MultInstructionInfo:
        return MultInstructionInfo(
            (
                cls(
                    (Uint8,),
                    {"address": EncodingSlot(0)},
                    instruction_value,
                    EncodingType.J,
                ),
            )
        )

    @classmethod
    def two_register_and_shift(cls, instruction_value: int) -> MultInstructionInfo:
        return MultInstructionInfo(
            (
                cls(
                    (NonRmRegister, Register, Shift),
                    {
                        "rd": EncodingSlot(0),
                        "rm": EncodingSlot(1),
                        "rn": EncodingSlot(2, "register"),
                        "shift_type": EncodingSlot(2, "type"),
                        "shift": EncodingSlot(2, "amount"),
                    },
                    instruction_value,
                    EncodingType.R,
                ),
            )
        )

    @classmethod
    def register_and_uint20(cls, instruction_value: int) -> MultInstructionInfo:
        return MultInstructionInfo(
            (
                cls(
                    (NonRmRegister, Uint16),
                    {"rd": EncodingSlot(0), "imm": EncodingSlot(1)},
                    instruction_value,
                    EncodingType.I,
                ),
            )
        )

    @classmethod
    def mov_instruction(
        cls,
        instruction_value_uint20: int,
        instrction_value_shift: int,
        instruction_value_second_moded_reg: int,
        instruction_value_first_moded_reg: int,
    ) -> MultInstructionInfo:
        return MultInstructionInfo(
            (
                cls.register_and_uint20(instruction_value_uint20)[0],
                cls(
                    (NonRmRegister, Shift),
                    {
                        "rd": EncodingSlot(0),
                        "shift_type": EncodingSlot(1, "type"),
                        "shift": EncodingSlot(1, "amount"),
                        "rn": EncodingSlot(1, "register"),
                    },
                    instrction_value_shift,
                    EncodingType.R,
                ),
                cls(
                    (NonRmRegister, ModedRegister),
                    {
                        "rd": EncodingSlot(0),
                        "rm": EncodingSlot(1, "register"),
                        "register_bank": EncodingSlot(1, "mode"),
                    },
                    instruction_value_second_moded_reg,
                    EncodingType.R,
                ),
                cls(
                    (NonRmModedRegister, Register),
                    {
                        "rd": EncodingSlot(0, "register"),
                        "rm": EncodingSlot(1),
                        "register_bank": EncodingSlot(0, "mode"),
                    },
                    instruction_value_first_moded_reg,
                    EncodingType.R,
                ),
            )
        )

    @classmethod
    def label(cls, instruction_value: int) -> MultInstructionInfo:
        return MultInstructionInfo(
            (
                cls(
                    (Label,),
                    {"address": EncodingSlot(0)},
                    instruction_value,
                    EncodingType.J,
                ),
            )
        )

    @classmethod
    def branch(
        cls, branch_type: int
    ) -> tp.Tuple[MultInstructionInfo, MultInstructionInfo]:
        assert branch_type <= 0b1111
        branch_value = 0b01010000 | branch_type
        link_value = 0b01110000 | branch_type
        return (cls.label(branch_value), cls.label(link_value))


class NoEncodingError(Exception):
    pass


class MultInstructionInfo(tp.Tuple[InstructionInfo, ...]):
    def get_encoding(
        self, args: tp.Union[tp.Sequence[InstructionArgTypes], int]
    ) -> InstructionInfo:
        if isinstance(args, int):
            try:
                return next(op for op in self if op.value == args)
            except StopIteration:
                raise NoEncodingError(
                    f"No valid encoding for this instruction with op code {args}"
                ) from None
        for instruction in self:
            if len(instruction.types) == len(args) and all(
                isinstance(arg, arg_type)
                for arg, arg_type in zip(args, instruction.types)
            ):
                return instruction

        raise NoEncodingError("No valid encoding with those args with this instruction")

    def reverse(self) -> MultInstructionInfo:
        return MultInstructionInfo(
            dataclasses.replace(
                instruction,
                types=tuple(reversed(instruction.types)),
                encoding_slots={
                    key: value.reversed_index()
                    for key, value in instruction.encoding_slots.items()
                },
            )
            for instruction in self
        )

    def __repr__(self) -> str:
        return f"{type(self).__name__}({super().__repr__()})"


class Instruction(enum.Enum):
    # The value arg in InstructionInfo is arbritrary right now; The actual value is TBD.
    LDR = InstructionInfo.register_and_pointer_deref_with_imm_or_shift_or_register(
        0b_000_10_100, 0b_000_10_000, 0b_000_10_001
    )
    STR = InstructionInfo.register_and_pointer_deref_with_imm_or_shift_or_register(
        0b_001_10_100, 0b_001_10_000, 0b_001_10_001
    ).reverse()
    MOV = InstructionInfo.mov_instruction(
        0b_001_00_100, 0b_001_00_000, 0b_001_00_001, 0b_001_00_010
    )
    ADD = InstructionInfo.two_register_and_shift_or_uint20(0b_010_00_000, 0b_010_00_100)
    ADDC = InstructionInfo.two_register_and_shift_or_uint20(
        0b_010_00_001, 0b_010_00_101
    )
    SUB = InstructionInfo.two_register_and_shift_or_uint20(0b_011_00_000, 0b_011_00_100)
    RSUB = InstructionInfo.two_register_and_shift_or_uint20(
        0b_011_00_001, 0b_011_00_101
    )
    SUBC = InstructionInfo.two_register_and_shift_or_uint20(
        0b_011_00_010, 0b_011_00_110
    )
    RSUBC = InstructionInfo.two_register_and_shift_or_uint20(
        0b_011_00_011, 0b_011_00_111
    )
    AND = InstructionInfo.two_register_and_shift_or_uint20(0b_100_00_000, 0b_100_00_100)
    OR = InstructionInfo.two_register_and_shift_or_uint20(0b_101_00_000, 0b_101_00_100)
    XOR = InstructionInfo.two_register_and_shift_or_uint20(0b_110_00_000, 0b_110_00_100)
    CMP = InstructionInfo.register_and_register_or_uint20(0b_011_01_000, 0b_011_01_100)
    TST = InstructionInfo.register_and_register_or_uint20(0b_100_01_000, 0b_100_01_100)
    INT = InstructionInfo.uint8(0b_100_10_000)
    BIC = InstructionInfo.two_register_and_shift_or_uint20(0b_100_00_001, 0b_100_00_101)
    NOP = InstructionInfo.nop(0b_010_1_0000)

    BEQ, BEQL = InstructionInfo.branch(0b0001)
    BNE, BNEL = InstructionInfo.branch(0b0010)
    BCS, BCSL = InstructionInfo.branch(0b0011)
    BNC, BNCL = InstructionInfo.branch(0b0100)
    BSS, BSSL = InstructionInfo.branch(0b0101)
    BNS, BNSL = InstructionInfo.branch(0b0110)
    BOV, BOVL = InstructionInfo.branch(0b0111)
    BNV, BNVL = InstructionInfo.branch(0b1000)
    BAB, BABL = InstructionInfo.branch(0b1001)
    BBE, BBEL = InstructionInfo.branch(0b1010)
    BGE, BGEL = InstructionInfo.branch(0b1011)
    BLT, BLTL = InstructionInfo.branch(0b1100)
    BGT, BGTL = InstructionInfo.branch(0b1101)
    BLE, BLEL = InstructionInfo.branch(0b1110)
    B, BL = InstructionInfo.branch(0b1111)

    @classmethod
    def from_int(cls, op: int) -> Instruction:
        try:
            return next(
                mem
                for mem in cls
                if op in {instruction.value for instruction in mem.value}
            )
        except StopIteration:
            raise ValueError(f"There is no instruction with the value {op}") from None

    def is_branch(self) -> bool:
        # I'm assuming that if one version if a instruction is a branch
        # instruction, all versions are
        info: InstructionInfo = self.value[0]
        return (info.value >> 4) in {0b0101, 0b0111}


InstructionArgTypes = tp.Union[
    PointerDeref,
    Uint16,
    Uint8,
    Shift,
    Label,
    Register,
    NonRmRegister,
    ModedRegister,
]
