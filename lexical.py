from dataclasses import dataclass
from enum import Enum, unique
from typing import Optional, Union, List, Tuple, Final


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
    UserDefined = 32
    LessThanSign = 33
    GreaterThanSign = 34


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


# returns is_number, is_float
def is_string_number(s: str) -> Tuple[bool, bool]:
    if s == "":
        return False, False
    if len(s) == 1:
        if s.isnumeric():
            return True, False
        else:
            return False, False
    if not s[0].isnumeric() and s[0] != "-":
        return False, False
    is_float = False
    for c in s[1:]:
        if not c.isnumeric() and c != ".":
            return False, False
        elif c == ".":
            if is_float:
                raise TokenizerException(f"Not a valid float: {s}")
            else:
                is_float = True
    return True, is_float


# [(String of token), (TokenType), (Needs space (isn't symbol))]
TOKENS: Final[List[Tuple[str, TokenTypes, bool]]] = [
    ("void", TokenTypes.Void, True),
    ("char", TokenTypes.Char, True),
    ("short", TokenTypes.Short, True),
    ("int", TokenTypes.Int, True),
    ("long", TokenTypes.Long, True),
    ("sizeof", TokenTypes.Sizeof, True),
    ("(", TokenTypes.OpenPar, False),
    (")", TokenTypes.ClosePar, False),
    ("[", TokenTypes.OpenBrace, False),
    ("]", TokenTypes.CloseBrace, False),
    ("{", TokenTypes.OpenBracket, False),
    ("}", TokenTypes.CloseBracket, False),
    (",", TokenTypes.Comma, False),
    (".", TokenTypes.Period, False),
    (";", TokenTypes.SemiColon, False),
    ("*", TokenTypes.Asterisks, False),
    ("+", TokenTypes.Plus, False),
    ("-", TokenTypes.Minus, False),
    ("%", TokenTypes.Mod, False),
    ("/", TokenTypes.Div, False),
    ("<", TokenTypes.LessThanSign, False),
    (">", TokenTypes.GreaterThanSign, False),
    ("return", TokenTypes.Return, True),
    ("for", TokenTypes.For, True),
    ("if", TokenTypes.If, True),
    ("else", TokenTypes.Else, True),
    ("while", TokenTypes.While, True),
    ("=", TokenTypes.EqualSign, False)
]


def is_token(tok: str) -> bool:
    for t in TOKENS:
        if tok == t[0]:
            return True
    return False


def is_valid_typename(tok: str) -> bool:
    if len(tok) == 0:
        return False
    if len(tok) == 1:
        if is_alpha(tok):
            return True
        else:
            return False
    for t in tok[1:]:
        if not is_alphanumeric(t):
            return False
    return True


def tokenize(data: str) -> List[Token]:
    toks: List[Token] = []
    tok = ""
    count = 0

    while count < len(data):
        if tok == "":
            try:
                while data[count].isspace():
                    count += 1
            except IndexError:
                return toks
        tok += data[count]

        if is_string_number(tok)[0]:
            while is_string_number(tok)[0]:
                count += 1
                tok += data[count]
            tok = tok[:len(tok) - 1]
            toks.append(Token(
                TokenTypes.FloatLiteral if is_string_number(tok)[1] else TokenTypes.IntegerLiteral,
                count - len(tok),
                tok
            ))
            tok = ""
        elif is_token(tok):
            after = data[count + 1]

            for t in TOKENS:
                if t[0] == tok:
                    if t[2] and is_alphanumeric(after):
                        break
                    toks.append(Token(t[1], count - len(tok) + 1, None))
                    tok = ""
        elif is_valid_typename(tok) and not is_alphanumeric(data[count + 1]):
            toks.append(Token(TokenTypes.UserDefined, count - len(tok) + 1, tok))
            tok = ""

        count += 1

    return toks
