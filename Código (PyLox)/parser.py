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
        if self.match(TokenType.NUMBER):
            return expressions.Literal(float(self.previous().valor))
        if self.match(TokenType.STRING):
            return expressions.Literal(self.previous().valor)
        if self.match(TokenType.THIS):
            return expressions.This(self.previous())
        if self.match(TokenType.IDENTIFIER):
            return expressions.Variable(self.previous())
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
    
        return self.call()


    def finishCall(self,callee: Expr) -> Expr:
        arguments : List[Expr] = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                arguments.append(self.expression())
                if not self.match(TokenType.COMMA):
                    break

        paren : Token = self.consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return expressions.Call(callee,paren,arguments)
         

    def call(self) -> Expr:
        expr : Expr = self.primary()

        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finishCall(expr)
            elif self.match(TokenType.DOT):
                name : Token = self.consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
                expr = expressions.Get(expr,name)
            else:
                break
        
        return expr


    def binary_op(self,func,tipos) -> Expr:
        expr = func()

        while self.match(tipos):
            operator = self.previous()
            right = func() #self.expression()
            expr = expressions.Binary(expr,operator,right)

        return expr


    def factor(self) -> Expr:
        tipos = [TokenType.SLASH,TokenType.STAR]
        return self.binary_op(self.unary,tipos)


    def term(self) -> Expr:
        tipos = [TokenType.MINUS,TokenType.PLUS]
        return self.binary_op(self.factor,tipos)


    def comparison(self) -> Expr:
        tipos = [TokenType.GREATER,TokenType.GREATER_EQUAL,TokenType.LESS,TokenType.LESS_EQUAL]
        return self.binary_op(self.term,tipos)


    def equality(self) -> Expr:
        tipos = [TokenType.BANG_EQUAL,TokenType.EQUAL_EQUAL]
        return self.binary_op(self.comparison,tipos)


    def expression(self) -> Expr:
        return self.assignment()


    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.CLASS):
                return self.classDeclaration()
            if self.match(TokenType.FUN):
                return self.function("function")
            if self.match(TokenType.VAR):
                return self.varDeclaration()
            return self.statement()
        except self.ParseError as e:
            self.synchronize()
            return None
        
<<<<<<< HEAD
    def classDeclaration(self) -> Stmt:
        name : Token = self.consume(TokenType.IDENTIFIER,"Expect class name.")
        self.consume(TokenType.LEFT_BRACE,"Expect '{' before class body.")
        
        methods : List[statements.Function] = []
        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            methods.add(self.function("method"))
            
        self.consume(TokenType.RIGHT_BRACE,"Expect '}' before class body.")
        return statements.Class(name,methods)  
=======
        
    def classDeclaration(self) -> Stmt:
        name : Token = self.consume(TokenType.IDENTIFIER,"Expect class name.")
        self.consume(TokenType.LEFT_BRACE,"Expect '{' before class body.")
    
        methods : List[statements.Function]= []
        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            methods.append(self.function("method"))
            
        self.consume(TokenType.RIGHT_BRACE,"Expect '}' before class body.")
        return statements.Class(name,methods)
    
>>>>>>> clases
        
    def statement(self) -> Stmt:
        if self.match(TokenType.FOR):
            return self.forStatement()
        if self.match(TokenType.IF):
            return self.ifStatement()
        if self.match(TokenType.PRINT):
            return self.printStatement()
        if self.match(TokenType.RETURN):
            return self.returnStatement()
        if self.match(TokenType.WHILE):
            return self.whileStatement()
        if self.match(TokenType.LEFT_BRACE):
            return statements.Block(self.block())
        
        return self.expressionStatement()


    def forStatement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN,"Expect '(' after 'for'.")

        initializer : Stmt = None  # initializer
        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.varDeclaration()
        else:
            initializer = self.expressionStatement()
        
        condition : Expr = None # condition
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression() 
            self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment : Expr = None # incremento
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body : Stmt = self.statement()
        if increment is not None:
            body = statements.Block([body,statements.Expression(increment)])

        if condition is None:
            condition = expressions.Literal(True)
        body = statements.While(condition,body)

        if initializer is not None:
            body = statements.Block([initializer,body])

        return body


    def ifStatement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN,"Expect '(' after 'if'.")
        condition : Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        thenBranch : Stmt = self.statement()
        elseBranch : Stmt = None
        if self.match(TokenType.ELSE):
            elseBranch = self.statement()

        return statements.If(condition,thenBranch,elseBranch)


    def printStatement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON,"Expect ';' after value.")
        return statements.Print(value)
    
    
    def returnStatement(self):
        key : Token = self.previous()
        value : Expr = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return statements.Return(key, value)


    def varDeclaration(self) -> Stmt:
        name : Token = self.consume(TokenType.IDENTIFIER,"Expect variable name.")
        initializer : Expr = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON,"Expect ';' after variable declaration.")
        return statements.Var(name,initializer)


    def whileStatement(self) -> Stmt : 
        self.consume(TokenType.LEFT_PAREN,"Expect '(' after 'while'.")
        condition : Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body : Stmt = self.statement()

        return statements.While(condition, body)


    def expressionStatement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON,"Expect ';' after value.")
        return statements.Expression(expr)
    
    
    def function(self, kind : str) -> statements.Function:
        name : Token = self.consume(TokenType.IDENTIFIER,"Expect "+kind+" name.")
        
        # Gestión de los parámetros
        self.consume(TokenType.LEFT_PAREN,"Expect '(' after "+kind+" name.")
        params : List[Token] = []
        if not self.check(TokenType.RIGHT_PAREN):
            while True:
                if len(params) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters.")
                params.append(self.consume(TokenType.IDENTIFIER,"Expect parameter name."))
                if not self.match(TokenType.COMMA):
                    break
        self.consume(TokenType.RIGHT_PAREN,"Expect ')' after parameters.")
        
        # Gestión del cuerpo
        self.consume(TokenType.LEFT_BRACE, "Expect '{' before "+kind+" body.")
        body : List[Stmt] = self.block()
        return statements.Function(name,params,body)


    def block(self) -> List[Stmt]:
        statements : List[Stmt] = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE,"Expect '}' after block.")
        return statements
    
    
    def block_bucle(self) -> List[Stmt]:
        statements : List[Stmt] = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE,"Expect '}' after block.")
        return statements


    def assignment(self) -> Expr:
        expr : Expr = self.orr()

        if self.match(TokenType.EQUAL):
            equals : Token = self.previous()
            value : Expr = self.assignment()

            if isinstance(expr,expressions.Variable):
                name : Token = expr.name
                return expressions.Assign(name,value)
            elif isinstance(expr,expressions.Get):
                get : expressions.Get = expr
                return expressions.Set(get.object, get.name, value)

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
    
    
    def parse(self) -> List[Stmt]:
        stmts : List[statements.Stmt] = []
        while not self.isAtEnd():
            #stmts.append(self.statement())
            stmts.append(self.declaration())

        return stmts
<<<<<<< HEAD
=======
    
>>>>>>> clases

if __name__ == '__main__':
    #pars = Parser([Token(0,TokenType.STRING,"'Hola mundo'"),Token(0,TokenType.EOF,"")])
    #pars = Parser([Token(0,TokenType['STRING'],"'Hola mundo'"), Token(0,TokenType['SEMICOLON'],";"),Token(0,TokenType['EOF'],"")])
    pars = Parser([Token(0,TokenType['NUMBER'],"1"), Token(0,TokenType['STAR'],"*"), Token(0,TokenType['NUMBER'],"2"), Token(0,TokenType['PLUS'],"+"), Token(0,TokenType['NUMBER'],"3"), Token(0,TokenType['SEMICOLON'],";"), Token(0,TokenType.EOF,"")])
    #print("El token 0 es ",pars.tokens[0]," y su tipo es ",TokenType(pars.tokens[0].tipo))
    #print(f"-- tokens in parser : {pars.tokens}")
    expr = pars.parse()
    #print(f"-- expr : {expr}")

