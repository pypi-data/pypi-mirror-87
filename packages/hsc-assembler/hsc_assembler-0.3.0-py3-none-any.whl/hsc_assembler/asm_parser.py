# TODO: Improve error messages
# Replace this with a parsing library (e.g pyparsing)?
from __future__ import annotations

import typing

from hsc_instructions.arg_types import (
    Label,
    ModedRegister,
    NonRmRegister,
    PointerDeref,
    Register,
    Shift,
    ShiftType,
    NonRmModedRegister,
)
from hsc_instructions.errors import ParseError
from hsc_instructions.instruction import Instruction
from hsc_instructions.instruction_info import Instruction as InstructionEnum
from hsc_instructions.sized_numbers import (
    PositiveSizedNumber,
    Uint5,
    Uint8,
    Uint16,
    UintOverflowError,
)

from hsc_assembler.token_enums import Syntax, TokenType

if typing.TYPE_CHECKING:
    from .parseable import Parseable
    from .token_enums import Token

    TPA = typing.TypeVar("TPA", bound=Parseable)


__all__ = ["InstructionsNT", "parse"]


class InstructionsNT(typing.NamedTuple):
    instructions: typing.Sequence[Instruction]
    symbol_table: typing.Dict[str, int]


def comma_split(tokens: typing.Iterable[Token]) -> typing.Iterator[typing.List[Token]]:
    current_tokens: typing.List[Token] = []
    for token in tokens:
        if token.type is TokenType.SYNTAX and token.value is Syntax[","]:
            yield current_tokens
            current_tokens = []
        else:
            current_tokens.append(token)
    if current_tokens:
        yield current_tokens


def empty_token_check(
    tokens: typing.Sequence[Token], line: int
) -> typing.Sequence[Token]:
    if not tokens:
        raise ParseError("Empty operand", line)
    return tokens


def extact_token(one_token: typing.Sequence[Token], line: int) -> Token:
    empty_token_check(one_token, line)
    if len(one_token) > 1:
        raise ParseError(
            f'Extra text "{"".join(token.text for token in one_token[1:])}"',
            line,
        )
    return one_token[0]


def token_type_check(
    token: Token,
    token_types: typing.Union[TokenType, typing.Iterable[TokenType]],
    line: int,
) -> Token:
    if isinstance(token_types, TokenType):
        token_types = (token_types,)
    if token.type not in token_types:
        type_names = " or ".join(token_type.name.lower() for token_type in token_types)
        message = f'Token "{token.text}" instead of {type_names}'
        raise ParseError(message, line)
    return token


TN = typing.TypeVar("TN", bound=PositiveSizedNumber)


def extract_token_num(token: Token, num_type: typing.Type[TN], line: int) -> TN:
    token_type_check(token, (TokenType.UINT, TokenType.STRING), line)
    try:
        return num_type(token.value)
    except UintOverflowError:
        assert isinstance(token.value, int)
        message = (
            f'Number or string "{token.value}" is too large. '  # type: ignore
            f'The max size for this operand is "{num_type.MAX}". '
            f'The orignal text was "{token.text}".'
        )
        raise ParseError(message, line) from None


@Register.make_parse_function
def parse_register(
    cls: typing.Type[Register], tokens: typing.Sequence[Token], line: int
) -> Register:
    token = token_type_check(extact_token(tokens, line), TokenType.REGISTER, line)
    assert isinstance(token.value, cls)
    return token.value


def non_rm_check(register: Register) -> None:
    if Register.r15 is register:
        raise ParseError(
            (
                "Register r15/pc can only take on the role "
                "of Rm (it cannot be shifted)"
            )
        )


@NonRmRegister.make_parse_function
def parse_non_rm_register(tokens: typing.Sequence[Token], line: int) -> Register:
    register = Register.parse(tokens, line)
    non_rm_check(register)
    return register


@PointerDeref.make_parse_function
def parse_pointer_deref(
    cls: typing.Type[PointerDeref],
    tokens: typing.Sequence[Token],
    line: int,
) -> PointerDeref:
    empty_token_check(tokens, line)
    if tokens[0].value is not Syntax["["] or tokens[-1].value is not Syntax["]"]:
        str_tokens = "".join(token.text for token in tokens)
        raise ParseError(f"Invalid pointer dereference {str_tokens}", line)
    register = Register.parse(tokens[1], line)
    if len(tokens) > 3:
        if tokens[2].value is not Syntax["+"]:
            raise ParseError(f'Expected "+" sign, instead got {tokens[2].text}', line)
        increment = cls.increment_parse(tokens[3:-1], line)
    else:
        increment = Uint20(0)
    return cls(register, increment)


@Uint8.make_parse_function
@Uint16.make_parse_function
def parse_number(
    cls: typing.Type[PositiveSizedNumber], tokens: typing.Sequence[Token], line: int
) -> PositiveSizedNumber:
    return extract_token_num(extact_token(tokens, line), cls, line)


@ModedRegister.make_parse_function
def parse_moded_register(
    cls: typing.Type[ModedRegister], tokens: typing.Sequence[Token], line: int
) -> ModedRegister:
    token = extact_token(tokens, line)
    token_type_check(token, TokenType.MODED_REGISTER, line)
    assert isinstance(token.value, ModedRegister)
    return token.value


@NonRmModedRegister.make_parse_function
def parse_non_rm_moded_register(
    cls: typing.Type[ModedRegister], tokens: typing.Sequence[Token], line: int
) -> NonRmModedRegister:
    moded_register = ModedRegister.parse(tokens, line)
    non_rm_check(moded_register.register)
    # Hacky solution
    moded_register.__class__ = NonRmModedRegister  # type: ignore
    return moded_register


@Shift.make_parse_function
def parse_shift(
    cls: typing.Type[Shift], tokens: typing.Sequence[Token], line: int
) -> Shift:
    empty_token_check(tokens, line)
    register = Register.parse(tokens[0], line)
    valid_operators = {
        Syntax[">>"],
        Syntax["<<"],
        Syntax.ror,
        Syntax.ser,
    }
    if len(tokens) == 1:
        shift_type = ShiftType["<<"]
        amount = Uint5(0)
    elif tokens[1].value not in valid_operators:
        raise ParseError(f"Invalid operator {tokens[1].text}", line)
    else:
        assert isinstance(tokens[1].value, Syntax)
        shift_type = ShiftType[tokens[1].value.name]
        amount = extract_token_num(extact_token(tokens[2:], line), Uint5, line)
    return cls(shift_type, register, amount)


@Label.make_parse_function
def parse_label(
    cls: typing.Type[Label], tokens: typing.Sequence[Token], line: int
) -> Label:
    return Label(
        token_type_check(extact_token(tokens, line), TokenType.LABEL, line).value
    )


def parse_args(
    parser_types: typing.Sequence[typing.Collection[typing.Type[TPA]]],
    args: typing.Sequence[typing.Sequence[Token]],
) -> typing.List[TPA]:
    if not args:
        return []
    for ver in parser_types:
        if len(ver) != len(args):
            continue
        try:
            return [
                t.parse(arg, arg[0].line) for t, arg in zip(ver, args)  # type: ignore
            ]
        except ParseError:
            pass
    if all(len(ver) != len(args) for ver in parser_types):
        raise ParseError(
            f"Instruction takes {len(parser_types[0])} arguments", args[0][0].line
        )
    raise ParseError("No valid variant for instruction", args[0][0].line)


def parse(tokens: typing.Iterator[typing.Sequence[Token]]) -> InstructionsNT:
    instructions = []
    symbol_table = {}
    ip = 0
    errors = []
    for line in tokens:
        if line[-1].value is Syntax[":"]:
            assert line[-1].type is TokenType.SYNTAX
            assert len(line) == 2
            assert line[0].type is TokenType.LABEL
            assert isinstance(line[0].value, str)
            symbol_table[line[0].value] = ip
        else:
            ip += 4
            assert line[0].type is TokenType.INSTRUCTION
            instruction = line[0].value
            assert isinstance(instruction, InstructionEnum)
            raw_args = list(comma_split(line[1:]))
            try:
                args = parse_args(
                    list(variant.types for variant in instruction.value), raw_args
                )
            except ParseError as exc:
                breakpoint()
                errors.append(exc.args[0])
                continue

            instructions.append(Instruction(instruction, args))
    if errors:
        raise ParseError.collect_errors(errors)
    return InstructionsNT(instructions, symbol_table)
