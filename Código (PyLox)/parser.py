import expressions
from Token import Token, TokenType
import re

tokens = []
current = 0

def match(self,*types:TokenType) -> bool:
    for tipo in types:
        if self.check(type):
            self.advance()
            return True
    return False

def check(self,tipo:TokenType) -> bool:
    if self.isAtEnd():
        return false
    return self.peek().tipo == tipo

def isAtEnd(self) -> bool:
    return self.peek().tipo == TokenType.EOF # definido?
    
def peek(self) -> Token:
    return self.tokens[self.current]
    
def previous(self) -> Token:
    return self.tokens[self.current-1]

def advance(self) -> Token:
    if self.isAtEnd() == false:
        self.current += 1
    return self.previous()

    
def expression(self) -> expressions.Expr:
    return self.exquality()

def equality(self) -> expressions.Expr:
    expr = self.comparison()

    while self.match(TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL):
        operator = self.previous()
        right = self.comparison()
        expr = expressions.Binary(expr,operator,right)

    return expr


## Implementación Domingo con ¿supertipos?

def arithmetic_func(funcion):
    def func_temp(lista_tokens):
        res = 0
        for i in lista_tokens:
            res = funcion(res,i)
        return res
    return func_temp

def res(x,y):
    return x-y

def sum(x,y):
    return x+y

def mul(x,y):
    return x*y

def pot(x):
    return x*x
        
