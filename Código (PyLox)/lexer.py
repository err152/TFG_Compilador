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
            #print("----- ",self.inicio," : ",estado," : ",caracter," : ",mid," : ",self.pos)
            nuevo_estado = self.transicion(estado,caracter,mid)
            if nuevo_estado == 'ERROR':
                if estado not in ('ESPACIO','NUMBER_','COMMENT_'):
                    yield Token(self.linea,TokenType[estado],self.token_actual())
                self.inicio = self.pos
                estado = 'inicial'
                
            elif nuevo_estado == 'ESPACIO':
                if estado not in ('inicial','ERROR','ESPACIO'):
                    #print(":::::: caracter = ",caracter," estado = ",estado)
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
        #print(" :: transicion :: estado ",estado," caracter ",caracter," mid ",mid)
        #print(" :://:://:: ",TokenType(caracter).name)
        if estado == 'inicial' and caracter in SINGLE_CHARS:
            #print(":::::: single char : ",caracter," es tokenType : ",TokenType(caracter).name)
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
    #a = Lexer('"espacio " 32 \ne2p4c10 ')
    #l = []
    #for i in a.devolver_tokens():
    #    l.append(i)
    #print(l)
    #analizador = Lexer("AAAAAA  A")
    #analizador = Lexer("> == *- 34")
    #analizador = Lexer("string 'Hola mundo' Sinbad el 'marino' soy")
    #analizador = Lexer(" '' ' ' ")
    #analizador = Lexer(" 2 2345 2.356 2. ")
    #analizador = Lexer('''class Brunch < Breakfast {
    #   init(meat, bread, drink) {
    #       super.init(meat, bread);
    #       this.drink = drink;
    #       }
    #   }''')
    #analizador = Lexer(" true false and adn burrito")
    #analizador = Lexer(" a si //Esto es un comentario \n Holaa")
    #analizador = Lexer('"string _ 34 */' ' " check')
    
    #for i in analizador.devolver_tokens():
    #    print(i)
        
