class Token:
    def __init__(self, linea, tipo, valor):
        self.linea = linea
        self.tipo = tipo
        self.valor = valor
        
    def __repr__(self):
        return f'[{self.linea},"{self.tipo}",{self.valor}]'
    
class Lexer:
    def __init__(self, entrada):
        self.entrada = entrada
        self.pos = 0
        self.linea = 0
        self.inicio = 0

    def devolver_tokens(self):
        estado = "inicial"
        while self.pos < len(self.entrada):
            caracter = self.entrada[self.pos]
            print("----- ",self.inicio," : ",estado," : ",caracter," : ",self.pos)
            nuevo_estado = self.transicion(estado,caracter)
            if nuevo_estado == 'ERROR':
                if estado != 'ESPACIO':
                    yield Token(self.linea,estado,self.entrada[self.inicio:self.pos])
                self.inicio = self.pos
                estado = 'inicial'
                
            elif nuevo_estado == 'ESPACIO':
                if estado not in ('inicial','ERROR','ESPACIO'):
                    yield Token(self.linea,estado,self.entrada[self.inicio:self.pos])
                self.inicio = self.pos
                self.pos += 1
                estado = nuevo_estado
                
            else:
                self.pos += 1
                estado = nuevo_estado
                
        if estado not in ('inicial','ERROR','ESPACIO'):
            yield Token(self.linea,estado,self.entrada[self.inicio:self.pos])

    def transicion(self,estado,caracter):
        if estado in ('NUMERO','inicial') and caracter.isdigit():
            return 'NUMERO'

        elif estado in  ('IDENTIFICADOR','inicial') and caracter.isalnum() or caracter == '_':
            return 'IDENTIFICADOR'

        elif estado not in ('STRING') and (caracter.isspace() or caracter == '\n'):
            if caracter == '\n':
                self.linea += 1
            return 'ESPACIO'

        else:
            return 'ERROR'

if __name__ == '__main__':
    analizador= Lexer("aAA  \n aas 34")
    for i in analizador.devolver_tokens():
        print(i)
        
