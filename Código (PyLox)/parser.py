import expressions
from Token import Token, TokenType
import re

class Parser:
    tokens = []
    current = 0

    def __init__(self,tokens:[]):
        self.tokens = tokens
        
    class ParseError(RuntimeError):
        def __init__(self,token:Token,msg:str):
            super().__init__(msg)
            self.token=token

    def match(self,*types:TokenType) -> bool:
        print(f"--------- INSIDE: MATCH {types}")
        for tipo in types:
            if self.check(tipo):
                self.advance()
                return True
        return False

    def check(self,tipo:TokenType) -> bool:
        print(f"---------- INSIDE: CHECK {tipo}")
        if self.isAtEnd():
            return false
        s = self.peek().tipo == tipo
        print(f"---------- INSIDE: CHECK {self.peek().tipo}")
        print(f"---------- INSIDE: CHECK {s}")
        return self.peek().tipo == tipo

    def isAtEnd(self) -> bool:
        #print(f"----------- INSIDE: END?")
        return self.peek().tipo == TokenType.EOF # definido?
    
    def peek(self) -> Token:
        #print(f"------------ INSIDE: PEEK {self.tokens[self.current]}")
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current-1]

    def advance(self) -> Token:
        print(f"---------- INSIDE: AVANZ")
        if self.isAtEnd() == False:
            self.current += 1
        return self.previous()

    def error(self,token:Token,msg:str) -> ParseError:
        print(f"------------- INSIDE: ERROR")
        #lexer.error(token,msg) # Mi lexer no tiene
        return self.ParseError(token,msg)

    def synchronize():
        self.advance()

        while self.isAtEnd() == false:
            if self.previous().tipo == TokenType.SEMICOLON:
                return

            if self.peek().tipo in(TokenType.CLASS,TokenType.FUN,
                                   TokenType.VAR,TokenType.FOR,
                                   TokenType.IF,TokenType.WHILE,
                                   TokenType.PRINT,TokenType.RETURN):
                return

            self.advance()

    def consume(self,tipo:TokenType,msg:str) -> Token:
        if check(tipo):
            return self.advance()
    
        raise self.error(self.peek(),msg)

    def primary(self) -> expressions.Expr:
        print("---------- INSIDE: PRIMA")
        if self.match(TokenType.FALSE):
            return expressions.Literal(false)
        if self.match(TokenType.TRUE):
            return expressions.Literal(true)
        if self.match(TokenType.NIL):
            return expressions.Literal(null)

        if self.match(TokenType.NUMBER,TokenType.STRING):
            return expressions.Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expr = expression()
            consume(RIGHT_PAREN,"Expect ')' after expression.")
            return expressions.Grouping(expr)

        self.error(self.peek(),"Expect expression.")
    
    def unary(self) -> expressions.Expr:
        print("--------- INSIDE: UNA")
        if self.match(TokenType.BANG,TokenType.MINUS):
            print("--------- INSIDE: UNA if")
            operator = previous()
            right = unary()
            return expressions.Unary(operator,right)
    
        return self.primary()

    def binary_op(self,func,tipos) -> expressions.Expr:
        print("-------- INSIDE: BINOP")
        expr = func
        print(f"------- func = {expr}")

        while self.match(tipos):
            operator = self.previous()
            right = func
            expr = expressions.Binary(expr,operator,right)

        return expr

    def factor(self) -> expressions.Expr:
        print("------- INSIDE: FAC")
        tipos = [TokenType.SLASH,TokenType.STAR]
        return self.binary_op(self.unary(),tipos)

    def term(self) -> expressions.Expr:
        print("------ INSIDE: TER")
        tipos = [TokenType.MINUS,TokenType.PLUS]
        return self.binary_op(self.factor(),tipos)

    def comparison(self) -> expressions.Expr:
        print("----- INSIDE: COM")
        tipos = [TokenType.GREATER,TokenType.GREATER_EQUAL,TokenType.LESS,TokenType.LESS_EQUAL]
        return self.binary_op(self.term(),tipos)

    def equality(self) -> expressions.Expr:
        print("---- INSIDE: EQU")
        tipos = [TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL]
        return self.binary_op(self.comparison(),tipos)

    def expression(self) -> expressions.Expr:
        print("--- INSIDE: EXP")
        return self.equality()

    def parse(self) -> expressions.Expr:
        print("-- INSIDE: PARSE")
        try:
            print("-- INSIDE: PARSE try")
            return self.expression()
        except self.ParseError:
            print("-- INSIDE: PARSE except")
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
 
