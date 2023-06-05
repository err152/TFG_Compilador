from enum import Enum
from typing import Dict,Tuple

class TokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    COMMA = ','
    DOT = '.'
    MINUS = '-'
    PLUS = '+'
    SEMICOLON = ';'
    SLASH = '/'
    STAR = '*'

    # One or two+ character tokens
    BANG = '!'
    BANG_EQUAL = '!='
    EQUAL = '='
    EQUAL_EQUAL = '=='
    GREATER = '>'
    GREATER_EQUAL = '>='
    LESS = '<'
    LESS_EQUAL = '<='
    COMMENT = '//'

    # Literales
    IDENTIFIER = 'identifier'
    NUMBER = 'num'
    STRING = 'str'

    # Keywords
    AND = 'and'
    CLASS = 'class'
    ELSE = 'else'
    FALSE = 'false'
    FUN = 'fun'
    FOR = 'for'
    IF = 'if'
    NIL = 'nil'
    OR = 'or'
    PRINT = 'print'
    RETURN = 'return'
    SUPER = 'super'
    THIS = 'this'
    TRUE = 'true'
    VAR = 'var'
    WHILE = 'while'

    # end-of-file
    EOF = ''

    def __repr__(self):
        
        return "TokenType."+self.__class__.__name__

class Token:
    def __init__(self, linea:int, tipo:TokenType, valor:any):
        self.linea = linea
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f'''Token({self.linea},{self.tipo},"{self.valor}")'''

    def tipo(self) -> TokenType:
        return self.tipo

_keywords: Tuple[str] = (
    'true','false','nil','and','or','if','else','fun','return','for','class',
    'super','this','while','print','var'
    )

KEYWORDS: Dict[str,TokenType] = {key: TokenType(key) for key in _keywords}

SINGLE_CHARS: Tuple[str] = (
    '(', ')', '{', '}', ',', '.', '-', '+', ';', '*',
)

MULTI_CHARS: Tuple[str] = ('!', '!=', '=', '==', '>', '>=', '<', '<=')

'''if __name__ == '__main__':
    tokk = Token(0,'num',3)
    print(tokk)'''

if __name__ == '__main__':
    t = TokenType.VAR
