from expressions import Expr
import expressions
from statements import Stmt, Print
import statements
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
        for tipo in types:
            if type(tipo) is list:
                for i in tipo:
                    if self.check(i):
                        self.advance()
                        return True
            elif self.check(tipo):
                self.advance()
                return True
        return False

    def check(self,tipo:TokenType) -> bool:
        if self.isAtEnd():
            return False
        s = getattr(self.peek(),"tipo") == tipo
        return self.peek().tipo == tipo

    def isAtEnd(self) -> bool:
        return self.peek().tipo == TokenType.EOF
    
    def peek(self) -> Token:
        return self.tokens[self.current]
    
    def previous(self) -> Token:
        return self.tokens[self.current-1]

    def advance(self) -> Token:
        #print("----- ",self.tokens[self.current])
        if self.isAtEnd() == False:
            self.current += 1
        return self.previous()

    def error(self,token:Token,msg:str) -> ParseError:
        return self.ParseError(token,msg)

    def synchronize(self):
        self.advance()

        while self.isAtEnd() == False:
            if self.previous().tipo == TokenType.SEMICOLON:
                return

            if self.peek().tipo in(TokenType.CLASS,TokenType.FUN,
                                   TokenType.VAR,TokenType.FOR,
                                   TokenType.IF,TokenType.WHILE,
                                   TokenType.PRINT,TokenType.RETURN):
                return

            self.advance()

    def consume(self,tipo:TokenType,msg:str) -> Token:
        if self.check(tipo):
            return self.advance()
    
        raise self.error(self.peek(),msg)

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return expressions.Literal(False)
        if self.match(TokenType.TRUE):
            return expressions.Literal(True) # True, true o TRUE ¿?
        if self.match(TokenType.NIL):
            return expressions.Literal(None)
        if self.match(TokenType.NUMBER,TokenType.STRING):
            return expressions.Literal(self.previous().valor)
        if self.match(TokenType.IDENTIFIER):
            return expressions.Variable(self.previous()) # quizás hace falta .valor ¿?
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN,"Expect ')' after expression.")
            return expressions.Grouping(expr)

        self.error(self.peek(),"Expect expression.")
    
    def unary(self) -> Expr:
        if self.match(TokenType.BANG,TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return expressions.Unary(operator,right)
    
        return self.primary()

    def binary_op(self,func,tipos) -> Expr:
        expr = func

        while self.match(tipos):
            operator = self.previous()
            #print("---- operator : ",operator)
            right = self.expression()
            #print("---- right : ",right)
            expr = expressions.Binary(expr,operator,right)

        return expr

    def factor(self) -> Expr:
        tipos = [TokenType.SLASH,TokenType.STAR]
        return self.binary_op(self.unary(),tipos)

    def term(self) -> Expr:
        tipos = [TokenType.MINUS,TokenType.PLUS]
        return self.binary_op(self.factor(),tipos)

    def comparison(self) -> Expr:
        tipos = [TokenType.GREATER,TokenType.GREATER_EQUAL,TokenType.LESS,TokenType.LESS_EQUAL]
        return self.binary_op(self.term(),tipos)

    def equality(self) -> Expr:
        tipos = [TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL]
        return self.binary_op(self.comparison(),tipos)

    def expression(self) -> Expr:
        return self.assignment()

    # Global Vars

    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.VAR):
                return self.varDeclaration()
            return self.statement()
        except self.ParseError as e:
            self.synchronize()
            return None
    
    # Modificación post-Statements
    
    def statement(self) -> Stmt:
        #print("selfffff - ",self)
        if self.match(TokenType.IF):
            return self.ifStatement()
        if self.match(TokenType.PRINT):
            return self.printStatement()
        if self.match(TokenType.LEFT_BRACE):
            #print("Abro scope")
            return statements.Block(self.block())
        
        return self.expressionStatement()

    def ifStatement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN,"Expect '(' after 'if'.")
        condition : Expr = self.expression()
        self.consume(TokenType.RIGHT_PA, "Expect ')' after if condition.")

        thenBranch : Stmt = self.statement()
        elseBranch : Stmt = None
        if self.match(TokenType.ELSE):
            elseBranch = self.statement()

        return statements.If(condition,thenBranch,elseBranch)

    def printStatement(self) -> Stmt:
        #print("PRINT statement")
        value = self.expression()
        self.consume(TokenType.SEMICOLON,"Expect ';' after value.")
        return statements.Print(value)

    def varDeclaration(self) -> Stmt:
        #print(" VAR statement")
        name : Token = self.consume(TokenType.IDENTIFIER,"Expect variable name.")
        #print("name = ",name)
        initializer : Expr = None
        if self.match(TokenType.EQUAL):
            #print("variable inicializada")
            initializer = self.expression()
        #print("inicializacion a ",initializer)
        self.consume(TokenType.SEMICOLON,"Expect ';' after variable declaration.")
        return statements.Var(name,initializer)

    def expressionStatement(self) -> Stmt:
        #print("EXPR statement")
        expr = self.expression()
        self.consume(TokenType.SEMICOLON,"Expect ';' after value.")
        return statements.Expression(expr)

    def block(self) -> List[Stmt]:
        statements : List[Stmt] = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())

        #print("Dentro block statements = ",statements)
        #print("Cierro scope")
        self.consume(TokenType.RIGHT_BRACE,"Expect '}' after block.")
        return statements

    def assignment(self) -> Expr:
        expr : Expr = self.orr()

        if self.match(TokenType.EQUAL):
            equals : Token = self.previous()
            value : Expr = self.assignment()

            if isinstance(expr,expressions.Variable):
                name : Token = expr.name
                #print("Dentro assignment ",name,value)
                return expressions.Assign(name,value)

            self.error(equals,"Invalid assignment target.")

        return expr

    def orr(self) -> Expr:
        expr : Expr = self.andd()

        while self.match(TokenType.OR):
            operator : Token = self.previous()
            right : Expr = self.andd()
            expr = expressions.Logical(expr,operator,right)
        
        return expr

    def andd(self) -> Expr:
        expr : Expr = self.equality()

        while self.match(TokenType.AND):
            operator : Token = self.previous()
            right : Expr = self.equality()
            expr = expressions.Logical(expr, operator, right)

        return expr
    
    '''
    def parse(self) -> expressions.Expr:
        #print(self.tokens)
        try:
            return self.expression()
        except self.ParseError:
            return None
   
    # Parser post-Statements
    '''
    
    def parse(self) -> List[Stmt]:
        stmts : List[statements.Stmt] = []
        while not self.isAtEnd():
            #stmts.append(self.statement())
            stmts.append(self.declaration())

        return stmts
    

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
    #pars = Parser([Token(0,TokenType['STRING'],"'Hola mundo'"), Token(0,TokenType['SEMICOLON'],";"),Token(0,TokenType['EOF'],"")])
    pars = Parser([Token(0,TokenType['NUMBER'],"1"), Token(0,TokenType['STAR'],"*"), Token(0,TokenType['NUMBER'],"2"), Token(0,TokenType['PLUS'],"+"), Token(0,TokenType['NUMBER'],"3"), Token(0,TokenType['SEMICOLON'],";"), Token(0,TokenType.EOF,"")])
    #print("El token 0 es ",pars.tokens[0]," y su tipo es ",TokenType(pars.tokens[0].tipo))
    #print(f"-- tokens in parser : {pars.tokens}")
    expr = pars.parse()
    print(f"-- expr : {expr}")

