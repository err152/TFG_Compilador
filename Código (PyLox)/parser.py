import expressions
from Token import Token, TokenType
import re

tokens = []
current = 0

class ParseError(RuntimeError):
    def __init__(self,token:Token,msg:str):
        super().__init__(msg)
        self.token=token

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

def error(self,token:Token,msg:str) -> ParseError:
    #lexer.error(token,msg) # Mi lexer no tiene
    return ParseError(token,msg)

def synchronize():
    self.advance()

    while self.isAtEnd() == false:
        if self.previous().tipo == TokenType.SEMICOLON:
            return

        if self.peek().tipo in(TokenType.CLASS,TokenType.FUN,
                               TokenType.VAR,TokenType.FOR,
                               TokenType.IF,TokenType.WHILE,
                               TokenType.PRINT,TokenType.RETURN):
            retrun

        self.advance()

def consume(self,tipo:TokenType,msg:str) -> Token:
    if check(tipo):
        return self.advance()
    
    raise self.error(self.peek(),msg)
    
def expression(self) -> expressions.Expr:
    return self.exquality()

def primary(self) -> expressions.Expr:
    if match(TokenType.FALSE):
        return expressions.Literal(false)
    if match(TokenType.TRUE):
        return expressions.Literal(true)
    if match(TokenType.NIL):
        return expressions.Literal(null)

    if match(TokenType.NUMBER,TokenType.STRING):
        return expressions.Literal(previous().literal)

    if match(TokenType.LEFT_PAREN):
        expr = expression()
        consume(RIGHT_PAREN,"Expect ')' after expression.")
        return expressions.Grouping(expr)

    self.error(self.peek(),"Expect expression.")
    
def unary(self) -> expressions.Expr:
    if match(TokenType.BANG,TokenType.MINUS):
        operator = previous()
        right = unary()
        return expressions.Unary(operator,right)
    
    return primary()

def binary_op(self,func,tipos) -> expressions.Expr:
    expr = func

    while self.match(tipos):
        operator = self.previous()
        right = func
        expr = expressions.Binary(expr,operator,right)

    return expr

def factor(self) -> expressions.Expr:
    tipos = [TokenType.SLASH,TokenType.STAR]
    return binary_op(unary(),tipos)

def term(self) -> expressions.Expr:
    tipos = [TokenType.MINUS,TokenType.PLUS]
    return binary_op(factor(),tipos)

def comparison(self) -> expressions.Expr:
    tipos = [TokenType.GREATER,TokenType.GREATER_EQUAL,TokenType.LESS,TokenType.LESS_EQUAL]
    return binary_op(term(),tipos)

def equality(self) -> expressions.Expr:
    tipos = [TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL]
    return binary_op(comparison(),tipos)

def parse(self) -> expressions.Expr:
    try:
        return expression()
    except:
        return None

'''
def comparison(self) -> expressions.Expr:
    expr = self.term()

    while self.match(TokenType.GREATER,GREATER_EQUAL,LESS,LESS_EQUAL):
        operator = self.previous()
        right = self.term()
        expr = expressions.Binary(expr,operator,right)

    return expr

def equality(self) -> expressions.Expr:
    expr = self.comparison()

    while self.match(TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL):
        operator = self.previous()
        right = self.comparison()
        expr = expressions.Binary(expr,operator,right)

    return expr
'''


    
## Implementación Domingo

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
 
