from dataclasses import dataclass
from enum import Enum, unique
from typing import Optional, Union, List, Final


@unique
class TokenTypes(Enum):
    Void = 1
    Char = 2
    Short = 3
    Int = 4
    Long = 5
    Float = 6
    Double = 7
    OpenPar = 8
    ClosePar = 9
    OpenBracket = 10
    CloseBracket = 11
    OpenBrace = 12
    CloseBrace = 13
    Comma = 14
    Period = 15
    SemiColon = 16
    Asterisks = 17
    Return = 18
    IntegerLiteral = 19
    StringLiteral = 20
    FloatLiteral = 21
    Plus = 22
    Minus = 23
    Div = 24
    Mod = 25
    EqualSign = 26
    For = 27
    While = 28
    If = 29
    Else = 30
    Sizeof = 31


class Token:
    pass


@dataclass
class Token:
    def __init__(self, token_type: TokenTypes, index: int, data: Optional[str]):
        self.token_type = token_type
        self.index = index
        self.data = data

    def __str__(self):
        if self.data is None:
            return f"TokenType: {str(self.token_type)}; Index: {self.index}"
        else:
            return f"TokenType: {str(self.token_type)}; Index: {self.index}; Data: {self.data}"

    def __eq__(self, other: Union[Token, TokenTypes]):
        if isinstance(other, TokenTypes):
            return self.token_type == other
        else:
            return super().__eq__(self, other)


class TokenizerException(Exception):
    def __init__(self, message):
        super().__init__(message)


def is_alpha(c: str) -> bool:
    return c.isalpha() or c == "_"


def is_alphanumeric(c: str) -> bool:
    return is_alpha(c) or c.isnumeric()


def tokenize(data: str) -> List[Token]:
    toks: List[Token] = []
    tok = ""
    count = 0

    while count < len(data):
        count += 1

    return toks
