from Token import (Token,TokenType,KEYWORDS,SINGLE_CHARS,
                   MULTI_CHARS)

class Lexer:
    def __init__(self, entrada):
        self.entrada = entrada
        self.pos = 0
        self.linea = 0
        self.inicio = 0

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
                if estado not in ('ESPACIO','NUMERO_','COMMENT_'):
                    yield Token(self.linea,estado,self.token_actual())
                self.inicio = self.pos
                estado = 'inicial'
                
            elif nuevo_estado == 'ESPACIO':
                if estado not in ('inicial','ERROR','ESPACIO'):
                    yield Token(self.linea,estado,self.token_actual())
                self.inicio = self.pos
                self.pos += 1
                estado = nuevo_estado
                
            else:
                self.pos += 1
                estado = nuevo_estado
                
        if estado not in ('inicial','ERROR','ESPACIO','COMMENT_'):
            yield Token(self.linea,estado,self.token_actual())

    def transicion(self,estado,caracter,mid):
        if estado == 'inicial' and caracter in SINGLE_CHARS: # BIEN
            return TokenType(caracter).name

        elif estado == 'inicial' and caracter in MULTI_CHARS: # BIEN
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
            self.pos -= 1

        elif estado == 'COMMENT_':
            if caracter == '\n':
                self.linea += 1
                return 'inicial'
            else:
                return 'COMMENT_'

        elif estado not in ('STRING_','NUMERO_','IDENTIFICADOR') and (caracter.isspace()
                                           or caracter == '\n'): # BIEN
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
            return 'NUMERO'

        elif estado == 'NUMERO':
            if caracter.isdigit():
                return 'NUMERO'
            elif caracter == '.':
                return 'NUMERO_'
            
        elif estado == 'NUMERO_':
            if caracter.isdigit():
                return 'NUMERO'
            else:
                return 'ERROR'

        elif estado in  ('IDENTIFICADOR','inicial') and caracter.isalnum() or caracter == '_':
            midd = self.entrada[self.inicio:self.pos+1]
            if midd in KEYWORDS:
                return TokenType(midd).name
            
            return 'IDENTIFICADOR'

        else:
            return 'ERROR'

            
#if __name__ == '__main__':
    #analizador = Lexer("aAA  \n ass 34")
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
        #print(i)
        
