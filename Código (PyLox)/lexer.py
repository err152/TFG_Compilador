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
            print("----- ",self.inicio," : ",estado," : ",caracter," : ",mid," : ",self.pos)
            nuevo_estado = self.transicion(estado,caracter,mid)
            if nuevo_estado == 'ERROR':
                if estado != 'ESPACIO':
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
                
        if estado not in ('inicial','ERROR','ESPACIO'):
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

        elif estado not in ('STRING') and (caracter.isspace()
                                           or caracter == '\n'): # BIEN
            if caracter == '\n':
                self.linea += 1
            return 'ESPACIO'

        elif estado == 'inicial' and (caracter == '"' or caracter == "'"):
            print("Entro STRING")
            self.consume_str(caracter)

        elif estado in ('NUMERO','inicial') and caracter.isdigit():
            #self.consume_num()
            return 'NUMERO'

        elif estado in  ('IDENTIFICADOR','inicial') and caracter.isalnum() or caracter == '_':
            #self.consume_id()
            return 'IDENTIFICADOR'

        else:
            return 'ERROR'

    def consume_str(self,caracter):
        while self.entrada[pos] != caracter and self.pos < len(self.entrada):
            if self.entrada[pos] == '\n':
                self.linea += 1
            self.pos += 1
            print("----- ",self.pos)
            
        self.pos +=1
        texto = self.entrada[(self.inicio+1):(self.pos-1)]
        print(texto)
        yield Token(self.linea,TokenType.STRING,texto)
            
if __name__ == '__main__':
    #analizador = Lexer("aAA  \n ass 34")
    #analizador= Lexer("> == *- 34")
    analizador= Lexer("string 'Hola mundo'")
    for i in analizador.devolver_tokens():
        print(i)
        
