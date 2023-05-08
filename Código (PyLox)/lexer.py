from dataclasses import dataclass
from Token import (Token,TokenType,KEYWORDS,SINGLE_CHARS,
                   MULTI_CHARS)

@dataclass
class Lexer:
    entrada : str
    pos : int = 0
    linea : int = 0
    inicio : int = 0

    def __init__(self,source:str):
        self.entrada=source

    def token_actual(self):
        return self.entrada[self.inicio:self.pos]

    def devolver_tokens(self):
        estado = "inicial"
        while self.pos < len(self.entrada):
            caracter = self.entrada[self.pos]
            mid = self.token_actual()
            nuevo_estado = self.transicion(estado,caracter,mid)
            if nuevo_estado == 'ERROR':
                if estado not in ('ESPACIO','NUMBER_','COMMENT_'):
                    yield Token(self.linea,TokenType[estado],self.token_actual())
                self.inicio = self.pos
                estado = 'inicial'
                
            elif nuevo_estado == 'ESPACIO':
                if estado not in ('inicial','ERROR','ESPACIO'):
                    yield Token(self.linea,TokenType[estado],self.token_actual())
                self.inicio = self.pos
                self.pos += 1
                estado = nuevo_estado
                
            else:
                self.pos += 1
                estado = nuevo_estado
                
        if estado not in ('inicial','ERROR','ESPACIO','COMMENT_'):
            yield Token(self.linea,TokenType[estado],self.token_actual())

    
    def transicion(self,estado,caracter,mid):
        if estado == 'inicial' and caracter in SINGLE_CHARS:
            return TokenType(caracter).name

        elif estado == 'inicial' and caracter in MULTI_CHARS: 
            self.pos += 1
            mid = self.entrada[self.inicio:self.pos+1]
            if mid in MULTI_CHARS:
                return TokenType(mid).name
            self.pos -= 1
            mid = self.token_actual()
            return TokenType(caracter).name

        elif estado == 'inicial' and caracter == '/':
            self.pos += 1
            midd = self.entrada[self.inicio:self.pos+1]
            if midd == '//':
                return 'COMMENT_'
            else:
                self.pos -=1
                midd = self.entrada[self.inicio:self.pos+1]
                return 'SLASH'
            self.pos -= 1

        elif estado == 'COMMENT_':
            if caracter == '\n':
                self.linea += 1
                return 'inicial'
            else:
                return 'COMMENT_'

        elif estado not in ('STRING_','NUMBER_','IDENTIFIER') and (caracter.isspace()
                                           or caracter == '\n'): 
            if caracter == '\n':
                self.linea += 1
            return 'ESPACIO'

        elif estado == 'inicial' and (caracter == '"' or caracter == "'"):
            return 'STRING_'
            
        elif estado == 'STRING_':
            if caracter == '"' or caracter == "'":
                return 'STRING'
            elif caracter != '"' or caracter != "'":
                return 'STRING_'

        elif estado == 'inicial' and caracter.isdigit():
            return 'NUMBER'

        elif estado == 'NUMBER':
            if caracter.isdigit():
                return 'NUMBER'
            elif caracter == '.':
                return 'NUMBER_'
            else:
                return 'ERROR'
            
        elif estado == 'NUMBER_':
            if caracter.isdigit():
                return 'NUMBER'
            else:
                return 'ERROR'

        elif estado in  ('IDENTIFIER','inicial') and caracter.isalnum() or caracter == '_':
            midd = self.entrada[self.inicio:self.pos+1]
            if midd in KEYWORDS:
                return TokenType(midd).name
            
            return 'IDENTIFIER'

        else:
            return 'ERROR'

    def extrae_tokens(self):
        l = []
        for i in self.devolver_tokens():
            l.append(i)
        l.append(Token(self.linea,TokenType['EOF'],""))
        return l

            
if __name__ == '__main__':
    a = Lexer('''true''')
    b = str(a.extrae_tokens())
    print(b)
        
