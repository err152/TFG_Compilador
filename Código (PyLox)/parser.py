import expressions
from typing import List
from Token import Token, TokenType
import re

class Parser:
    tokens: List[Token] = []
    current = 0

    def __init__(self,tokens:List[Token]):
        self.tokens = tokens
        
    class ParseError(RuntimeError):
        def __init__(self,token:Token,msg:str):
            super().__init__(msg)
            self.token=token

    def match(self,*types:TokenType) -> bool:
        print("--- Dentro match:")
        for tipo in types:
            if type(tipo) is list:
                for i in tipo:
                    if self.check(i):
                        print(f"----- tip : {i}")
                        self.advance()
                        return True
            elif self.check(tipo):
                print(f"----- tipo : {tipo}")
                self.advance()
                return True
        return False

    def check(self,tipo:TokenType) -> bool:
        if self.isAtEnd():
            return False
        print("----- tipo ::: ",type(self.peek().tipo))
        print(":::::::: tipo = ", getattr(self.peek(),"tipo"))
        s = getattr(self.peek(),"tipo") == tipo
        print(f"----- actual : {self.peek().tipo} =? {tipo} --> {s}")
        return self.peek().tipo == tipo

    def isAtEnd(self) -> bool:
        return self.peek().tipo == TokenType.EOF
    
    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current-1]

    def advance(self) -> Token:
        if self.isAtEnd() == False:
            self.current += 1
        return self.previous()

    def error(self,token:Token,msg:str) -> ParseError:
        lox.error(token,msg)
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
        if self.match(TokenType.FALSE):
            return expressions.Literal(false)
        if self.match(TokenType.TRUE):
            return expressions.Literal(true)
        if self.match(TokenType.NIL):
            return expressions.Literal(null)

        if self.match(TokenType.NUMBER,TokenType.STRING):
            return expressions.Literal(self.previous().valor)

        if self.match(TokenType.LEFT_PAREN):
            expr = expression()
            consume(TokenType.RIGHT_PAREN,"Expect ')' after expression.")
            return expressions.Grouping(expr)

        self.error(self.peek(),"Expect expression.")
    
    def unary(self) -> expressions.Expr:
        if self.match(TokenType.BANG,TokenType.MINUS):
            operator = previous()
            right = unary()
            return expressions.Unary(operator,right)
    
        return self.primary()

    def binary_op(self,func,tipos) -> expressions.Expr:
        expr = func

        while self.match(tipos):
            a = self.peek()
            operator = self.previous()
            b = self.peek()
            right = self.expression()
            expr = expressions.Binary(expr,operator,right)

        print(f"BINARYOP : {expr}")
        return expr

    def factor(self) -> expressions.Expr:
        tipos = [TokenType.SLASH,TokenType.STAR]
        return self.binary_op(self.unary(),tipos)

    def term(self) -> expressions.Expr:
        tipos = [TokenType.MINUS,TokenType.PLUS]
        return self.binary_op(self.factor(),tipos)

    def comparison(self) -> expressions.Expr:
        tipos = [TokenType.GREATER,TokenType.GREATER_EQUAL,TokenType.LESS,TokenType.LESS_EQUAL]
        return self.binary_op(self.term(),tipos)

    def equality(self) -> expressions.Expr:
        tipos = [TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL]
        return self.binary_op(self.comparison(),tipos)

    def expression(self) -> expressions.Expr:
        return self.equality()
    
    # Modificación post-Statements
    '''
    def statement(self) -> statements.Stmt:
        if match(PRINT):
            return self.printStatement()
        
        return self.expressionStatement()

    def printStatement(self) -> statements.Stmt:
        value = self.expression()
        consume(TokenType.SEMICOLON,"Expect ';' after value.")
        return statements.Stmt.Print(value)

    def expressionStatement(self) -> statements.Stmt:
        expr = self.expression()
        consume(TokenType.SEMICOLON,"Expect ';' after value.")
        return statements.Stmt.Expression(expr)
    '''
    
    def parse(self) -> expressions.Expr:
        print(self.tokens)
        try:
            return self.expression()
        except self.ParseError:
            return None
   
    # Parser post-Statements
    '''
    def parse(self) -> *statements.Stmt:
        statements = []
        while not isAtEnd():
            statements.append(self.statement())

        return statements
    '''

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

if __name__ == '__main__':
    #pars = Parser([Token(0,TokenType.STRING,"'Hola mundo'"),Token(0,TokenType.EOF,"")])
    pars = Parser([Token(0,TokenType['STRING'],"'Hola mundo'"),Token(0,TokenType['EOF'],"")])
    #pars = Parser([Token(0,TokenType.NUMBER,"1"), Token(0,TokenType.PLUS,"+"), Token(0,TokenType.NUMBER,"2"), Token(0,TokenType.EOF,"")])
    print("El token 0 es ",pars.tokens[0]," y su tipo es ",TokenType(pars.tokens[0].tipo))
    #print(f"-- tokens in parser : {pars.tokens}")
    expr = pars.parse()
    print(f"-- expr : {expr}")
