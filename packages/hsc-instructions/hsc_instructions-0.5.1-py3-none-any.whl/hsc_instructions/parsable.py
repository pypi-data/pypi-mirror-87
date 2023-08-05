from __future__ import annotations

import abc
import dataclasses
import typing as tp

T = tp.TypeVar("T")
PT = tp.TypeVar("PT", bound="Parsable")

# cls: tp.Type[PT]
# tokens: tp.Union[tp.Sequence[tp.Any], tp.Any]
# line: int
# returns: PT
ParseFunction = tp.Callable[
    [tp.Type[PT], tp.Union[tp.Sequence[tp.Any], tp.Any], int], PT
]
ParseMethod = tp.Callable[[tp.Union[tp.Sequence[tp.Any], tp.Any], int], PT]
TPF = tp.TypeVar("TPF", bound=ParseFunction)


class Parsable:
    parse_function: tp.ClassVar[tp.Optional[ParseFunction]] = None

    @classmethod
    def make_parse_function(cls, function: TPF) -> TPF:
        cls.parse_function = function
        return function

    @classmethod
    def parse(
        cls: tp.Type[PT],
        tokens: tp.Union[tp.Sequence[tp.Any], tp.Any],
        line: int,
    ) -> PT:
        if cls.parse_function is None:
            decorator = cls.make_parse_function.__qualname__
            msg = (
                "parse method not implemented; "
                f"specify parse function using {decorator} decorator"
            )
            raise NotImplementedError(msg)
        if not isinstance(tokens, tp.Sequence):
            tokens = [tokens]
        return cls.parse_function(cls, tokens, line)


@dataclasses.dataclass
class FakeParsable(abc.ABC, tp.Generic[T]):
    """
    Same as Parsable except it returns an object with a different type than its type

    Avoid using this when possible
    """

    parse_function: tp.ClassVar[
        tp.Optional[tp.Callable[[tp.Union[tp.Sequence[tp.Any], tp.Any], int], T]]
    ]
    real_class: tp.ClassVar[tp.Type[T]]

    def __new__(cls, *args: object, **kwargs: object) -> tp.Any:
        return cls.real_class(*args, **kwargs)

    @classmethod
    def __subclasshook__(cls, other: type) -> tp.Any:
        return issubclass(other, cls.real_class) or NotImplemented

    @classmethod
    def make_parse_function(
        cls, function: tp.Callable[[tp.Union[tp.Sequence[tp.Any], tp.Any], int], T]
    ) -> tp.Callable[[tp.Union[tp.Sequence[tp.Any], tp.Any], int], T]:
        cls.parse_function = function
        return function

    @classmethod
    def parse(
        cls,
        tokens: tp.Union[tp.Sequence[tp.Any], tp.Any],
        line: int,
    ) -> T:
        if cls.parse_function is None:
            decorator = cls.make_parse_function.__qualname__
            msg = (
                "parse method not implemented; "
                f"specify parse function using {decorator} decorator"
            )
            raise NotImplementedError(msg)
        if not isinstance(tokens, tp.Sequence):
            tokens = [tokens]
        return cls.parse_function(tokens, line)
