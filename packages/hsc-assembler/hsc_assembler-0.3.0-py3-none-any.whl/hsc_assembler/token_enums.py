import enum
import typing

__all__ = ["TokenType", "Syntax", "Token"]

if typing.TYPE_CHECKING:
    from hsc_assembler.scanner import Token


def __getattr__(name: str) -> typing.Any:
    # To prevent a circular import error
    if name == "Token":
        from .scanner import Token

        return Token
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


class TokenType(enum.Enum):
    INSTRUCTION = enum.auto()
    REGISTER = enum.auto()
    MODED_REGISTER = enum.auto()
    SYNTAX = enum.auto()
    LABEL = enum.auto()
    STRING = enum.auto()
    UINT = enum.auto()


# This is defined like this because of the special characters as the enum names
Syntax = enum.Enum("Syntax", [",", "[", "]", "+", ":", "<<", ">>", "ror", "ser"])
