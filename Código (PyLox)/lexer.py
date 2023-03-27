import Lox
from dataclasses import dataclass
from Token import (Token,TokenType,KEYWORDS,SINGLE_CHARS,
                   MULTI_CHARS)

@dataclass
class Lexer:
    entrada : str
    pos : int = 0
    linea : int = 0
    inicio : int = 0
    tokens : Token = []

    def __innit__(self, entrada:str):
        self.entrada = entrada

    def isAtEnd(self) -> bool :
        return self.pos >= len(self.entrada)

    def avanza(self) -> str :
        return self.entrada[self.pos++]

    def anhade_token(self, tipo:TokenType):
        self.anhade_token(tipo,None)

    def anhade_token(self, tipo:TokenType, literal:any):
        texto = self.entrada[self.inicio, self.pos]
        self.tokens.add(Token(self.linea,tipo,texto))

    def match(self, expected:str) -> bool :
        if self.isAtEnd() return false
        if self.entrada[self.pos] != expected return false

        self.pos++
        return true

    def peek(self) -> str :
        if self.isAtEnd() return '\0'
        return self.entrada[self.pos]

    def string(self) :
        while self.peek() != '"' and !self.isAtEnd:
            if self.peek() == '\n' self.linea++
            self.avanza

        if (self.isAtEnd()):
            Lox.error(linea,"Unterminated string.")
            return

        self.advance()

        valor = self.entrada[self.inicio+1,self.pos-1]
        self.anhade_token(STRING,valor)

    def isDigit(self,c:str) -> bool :
        return c >= '0' and c <= '9'

    def peekNext(self):
        if self.pos+1 >= len(self.entrada) return '\0'
        return self.entrada[pos+1]

    def number(self):
        while self.isDigit(self.peek()) self.avanza()

        if self.peek() == '.' and self.isDigit(self.peekNext()):
            self.avanza()

            while self.isDigit(self.peek()) self.avanza()

        self.anhade_token(NUMBER,float(self.entrada[self.inicio, self.pos]))

    def identifier(self):
        while self.isAlphaNumeric(self.peek()) self.avanza()

        text = self.entrada[self.inicio, self.current]
        tipo = KEYWORDS.get(text)
        if tipo == None tipo = IDENTIFIER

        self.anhade_token(tipo)

    def isAlpha(c:str) -> bool :
        return (c >= 'a' and c <= '<') or (c >= 'A' and c <= 'Z') or c == '_'

    def isAplhaNumeric(c:str) -> str :
        return self.isAlpha(c) or self.isDigit(c)

    def lee_token(self):
        c = self.avanza()
        if c == '(' :
            self.anhade_token(LEFT_PAREN)
            break
        if c == ')' :
            self.anhade_token(RIGHT_PAREN)
            break
        if c == '{' :
            self.anhade_token(LEFT_BRACE)
            break
        if c == '}' :
            self.anhade_token(RIGHT_BRACE)
            break
        if c == ',' :
            self.anhade_token(COMMA)
            break
        if c == '.' :
            self.anhade_token(DOT)
            break
        if c == '-' :
            self.anhade_token(MINUS)
            break
        if c == '+' :
            self.anhade_token(PLUS)
            break
        if c == ';' :
            self.anhade_token(SEMICOLON)
            break
        if c == '*' :
            self.anhade_token(STAR)
            break
        if c == '!' :
            self.anhade_token(BANG_EQUAL if match('=') else BANG)
            break
        if c == '=' :
            self.anhade_token(EQUAL_EQUAL if match('=') else EQUAL)
            break
        if c == '<' :
            self.anhade_token(LESS_EQUAL if match('=') else LESS)
            break
        if c == '>' :
            self.anhade_token(GREATER_EQUAL if match('=') else GREATER)
            break
        if c == '/' :
            if self.match('/'):
                while(self.peek() != '\n' and !self.isAtEnd()) self.avanza()
            else:
                self.anhade_token(SLASH)
            break
        if c == ' ' :
            break
        if c == '\r' :
            break
        if c == '\t' :
            break
        if c == '\n' :
            self.linea++
            break
        if c == '"' :
            self.string()
            break

        if == 'o':
            if self.match('r'):
                self.anhade_token(OR)
                break
      
        else:
            if self.isDigit(c):
                self.number()
            else if self.isAlfa(c):
                self.identifier()
            else:
                Lox.error(self.linea, "Unexpected character.")

    def extrae_tokens(self):
        while self.isAtEnd() == False:
            # We are at the beginning of the next lexeme
            inicio = self.pos

        tokens.add(Token(self.linea,EOF,''))
        return self.tokens
    
