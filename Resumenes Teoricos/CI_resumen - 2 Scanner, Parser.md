# Crafting Interpreters

#### Mi resumen: por Eduardo del Rio Ruiz

Scanning/Representando el Codigo/Parsing Expressions

## 4. Scanning

Este es el primer paso de cualquier intérprete. El scanner toma un código fuente como una serie de caracteres y los agrupa en lo que llamamos **lexemas**, los cuales tratados como información de un tipo concreto y en un contexto se convierten en **tokens**.

Se definen 3 tipos de token: IDENTIFICADOR, NUMERO, STRING

Además de palabras clave como operadores lógicos, funciones internas, o caracteres especiales.

Todos ellos son definidos en el fichero de nombre 'TokenType.py' de la siguiente manera:

```python
class Token:
    def __init__(self, linea, tipo, valor):
        self.linea = linea
        self.tipo = tipo
        self.valor = valor

    def __repr__(self):
        return f'[{self.linea},"{self.tipo}",{self.valor}]'

class TokenType(Enum):
    # Single-character tokens
    LEFT_PAREN = '('
    RIGHT_PAREN = ')'
    LEFT_BRACE = '{'
    RIGHT_BRACE = '}'
    COMMA = ','
    DOT = '.'
    MINUS = '-'
    PLUS = '+'
    SEMICOLON = ';'
    SLASH = '/'
    STAR = '*'

    # One or two+ character tokens
    BANG = '!'
    BANG_EQUAL = '!='
    EQUAL = '='
    EQUAL_EQUAL = '=='
    GREATER = '>'
    GREATER_EQUAL = '>='
    LESS = '<'
    LESS_EQUAL = '<='

    # Literales
    IDENTIFIER = 'identifier'
    NUMBER = 'num'
    STRING = 'str'

    # Keywords
    AND = 'and'
    CLASS = 'class'
    ELSE = 'else'
    FALSE = 'false'
    FUN = 'fun'
    FOR = 'for'
    IF = 'if'
    NIL = 'nil'
    OR = 'or'
    PRINT = 'print'
    RETURN = 'return'
    SUPER = 'super'
    THIS = 'this'
    TRUE = 'true'
    VAR = 'var'
    WHILE = 'while'

    # end-of-file
    EOF = ''

_keywords: Tuple[str] = (
    'true','false','nil','and','or','if','else','fun','return','for','class',
    'super','this','while','print'
    )

KEYWORDS: Dict[str,TokenType] = {key: TokenType(key) for key in _keywords}

SINGLE_CHARS: Tuple[str] = (
    '(', ')', '{', '}', ',', '.', '-', '+', ';', '*',
)

MULTI_CHARS: Tuple[str] = ('!', '!=', '=', '==', '>', '>=', '<', '<=')
```

Los tokens son tuplas compuestas de un número de línea, el tipo al que pertenecen y un valor dentro del tipo. Se definen todos los caracteres posibles bajo su nombre de tipo para poder utilizarlos a gusto en le resto del código.

Una vez definidos, ahora dada una cadena de caracteres debemos desarrollar un programa **lexer.py** que lea caracter a caracter y vaya identificando los distintos tipos de tokens según avance.

```python
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
                if estado not in ('ESPACIO','NUMERO_'):
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
```

Este programa cuenta con unos atributos llamados pos, inicio y linea que respectivamente indican la posición actual dentro de la cadena de caracteres, el inicio del token actualmente en proceso, y el número de línea actual.

En la función devuelve_token se avanza caracter a caracter aumentando pos hasta reconocer que ha terminado el token llamando a la funcion transición en cada iteración, devolviendo los caracteres del inicio hasta la posicion actual, junto a la linea (que también irá aumentando según se lea el caracter \n).

La función transición es la que se encarga de ir reconociendo los caracteres e interpretarlos como los distintos tipos de tokens que tenemos, comprobando el caracter actual o los leídos desde el inicio hasta la posición actual, y devolviendo el tipo de Token en forma de string.

## 5. Representando el código

A la hora de definir el lenguaje de forma sintáctica tendremos que crear una gramática libre de contexto o **CFG**, mediante la cual definiendo reglas o **producciones** se abarcará todo el lenguaje sin definir implícitamente cada punto y coma.

Estas producciones tiene la forma:

A → Bc ;

Donde A es la **cabeza** y esta se transforma en el **cuerpo** Bc siendo B una **variable** y c un **terminal**. Los terminales serán tokens que vienen del lexer, y se llaman así porque son un punto final, estos no pueden derivar mediante producciones. Por otro lado, las variables o no-terminales hacen referencia a otras producciones de la gramática.

En nuestra notación también se utilizarán los siguientes simbolos:

- A → b | c | d ;    Funcionando el símbolo '|' como un OR.
- A → (b | c) d ;    Los paréntesis dan prioridad de elección al grupo que rodean.
- A → B B* ;    El símbolo '*' indica que la variable a la que sigue se puede repetir entre 0 e infinitas veces. De esta forma logramos recursión.
- A → B+ ;    El símbolo '*' indica que la variable a la que sigue se puede repetir entre 1 e infinitas veces. De esta forma logramos recursión.
- A → b (C d E)? ;    Indicando '?' que el grupo o variable al que acompaña aparece una o ninguna vez, es opcional.

En nuestra gramática para el lenguaje Lox se definen de comienzo las siguientes expresiones:

- Literales: numeros, strings, booleanos, nil.
- Expresiones Unarias: el prefijo "!" para realizar un NOT lógico o "-" para negar un número.
- Expresiones Binarias: los operadores aritméticos y lógicos que conocemos.
- Paréntesis: Un par de "(" y ")" que envuelven una expresión.

Esta sería nuestra gramática resultante:

expression → literal
                    | unary
                    | binary
                    | grouping ;
literal → NUMBER | STRING | "true" | "false" | "nil" ;
grouping → "(" expression ")" ;
unary → ( "-" | "!" ) expression ;
binary → expression operator expression ;
operator → "==" | "!=" | "<" | "<=" | ">" | ">="
                | "+" | "-" | "*" | "/" ;

## El patrón Visitante

Este patrón funciona de manera que teniendo dos subclases 'B' y 'C' que extienden a otra clase principal 'A', se crea una interfaz 'visitaBC' con un nuevo método para cada una de las subclases llamado 'visitaB' y 'visitaC', en la clase 'A' se agrega un método llamado 'acepta', y por último en cada una de las subclases se define este método 'acepta' de forma que se le pase la interfaz 'visitaBC' como parámetro y ahí se elija si 'visitaB' o 'visitaC'. Ahora cuando se desee realizar una operación se llama al método 'acepta' y se le pasa como parámetro el visitante (la interfaz) que se quiera ejecutar.

Esto se conoce como polimorfismo, definido como la capacidad de llamar a objetos de distintos tipos con la misma sintaxis.

...........…
.............

# 
