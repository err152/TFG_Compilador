# Crafting Interpreters

#### Mi resumen: por Eduardo del Rio Ruiz

## 1. Introducción

Se va a crear un interprete de un lenguaje de programación llamado Lox, un "lenguaje de dominio específico". A priori, programar un idioma es un tarea muy compleja que iremos resolviendo poco a poco.

El libro se divide en 3 secciones:

- Sección de introducción al lenguaje Lox y la terminología utilizada en la programación de lenguajes.
- Otras dos secciones que implementan ambas un interprete distinto del lenguaje Lox.

Tras cada capítulo tendremos un programa funcional que, con el paso de los capítulos, crecerá hasta cubrir por completo un lenguaje.

Al final de cada capítulo tendremos ejercicios presentados como retos para ampliar nuestro conocimiento.

A diferencia del libro, yo implementaré el interprete plox en python, en vez de en java o en C.

------

## 2. Mapa de del Territorio

"You must have a map, no matter how rough.
Otherwise you wander all over the place. In “The
Lord of the Rings” I never made anyone go
farther than he could on a given day." - J.R.R. Tolkien

Nuestro programa comenzará siendo un código fuente crudo compuesto por cadenas de caracteres. Cada fase analiza el programa y lo transforma en una representación de una capa superior donde la semántica irá tomando forma.

Llegados a la cima, tenemos ya un programa de usuario con un código ya comprensible. Ahora, mientras bajamos, transformaremos el codigo ya de alto nivel en uno más de bajo nivel hasta que llegar a algo que sepamos como ejecuta la CPU.

![image-20220403201402745](C:\Users\Eduardo\AppData\Roaming\Typora\typora-user-images\image-20220403201402745.png)

#### 

#### Scanning (Lexing/Lexical Analysis)

Un '**lexer**' toma un flujo de caracteres y lo transforma en una serie de '**tokens**' (palabras). Estos tokens pueden ser uno o varios caracteres, ya sean literales, numeros, palabras, etc... Se ignoraran los comentarios y los espacios entre palabras.

![image-20220403202134336](C:\Users\Eduardo\AppData\Roaming\Typora\typora-user-images\image-20220403202134336.png)

#### Parsing

Aquí nuestra sintaxis toma una gramática. Un '**parser**' toma una secuencia de tokens y crea una estructura en árbol (parse tree/abstract syntax tree) que imita la naturaleza anidada de una gramática. En esta parte se reportan los '**syntax errors**' o errores de sintaxis.

![image-20220403202143315](C:\Users\Eduardo\AppData\Roaming\Typora\typora-user-images\image-20220403202143315.png)

#### Análisis Estático¿?

El primer análisis que suele realiza un lenguaje se denomina '**binding**' (vinculación) o **resolución**. Para cada **identificador** buscamos donde está definido ese nombre y lo enlazamos.

Aquí se lleva a cabo el '**scope**', donde dentro de una región en el código fuente un cierto nombre puede usarse para hacer referencia a una declaración específica.

Aquí también generaremos los '**type errors**' cuando se realice una operación entre variables de un tipo que no aguantan dicha operación.

La información se puede almacenar como **atributo** en el arbol sintáctico; en una **tabla de símbolos**; o en una estructura de datos completamente nueva.

Hasta aquí el *front end* del interprete.

#### Representación Intermedia

Representación de nuestro interprete entre el front end y back end, que nos permite el soporte de multiples lenguajes fuente, creando un front end para cada lenguaje, un back end para cada lenguaje y luego conectandolos a gusto.

#### Optimization

Optimizar el código. Ejemplo '**constant folding**': remplazar la inicialización de una variable como operación de constantes por el valor de la operación.

#### Generación de Código

Comienza el *back end*. Transformamos el código fuente en código máquina poco a poco, teniendo en dónde deseamos ejecutar nuestro programa. El código generado para correr en una VM se denomina '**bytecode**'.

#### Máquina Virtual

Todavía falta generar desde el bytecode el código máquina para que sea ejecutado por el chipset específico de la máquina en cuestión.

#### Runtime

Hora de ejecutar el programa y ver el resultado final!

Tenemos 3 rutas alternativas:

- Single-pass compilers: entrelaza parsing, analisis y generación de código generando código ejecutable directamente desde el parser.
- Tree-walk interpreters: ejecuta codigo justo despues del parsing, recorriendo el árbol sintáctico rama por rama y hoja por hoja linealmente.
- Transpilers: a la hora de 'bajar de nivel' a nuestro código podemos tratar de generar un código homólogo en otro idioma de alto lenguaje distinto, y utilizar las herramientas de compilación ya existentes de este para generar el código máquina.
- JIT:

#### Compiladores e Interpretes

Compilar es una técnica de implementación que trata de traducir un lenguaje fuente a otra forma, normalmente a nivel inferior. 

Un intérprete además de traducir el lenguaje lo ejecuta.

------

## 3. El lenguaje Lox

```c
// Your first Lox program!
print "Hello, world!";
```

Lox se escribe dinámicamente. Las variables pueden almacenar valores de cualquier tipo, o incluso una variable puede almacenar varios datos de distinto tipo.

A la hora de gestionar la memoria de forma automática tenemos dos opciones: '**reference counting**' o **tracing garbage collection**'. En nuestro caso utilizaremos el garbage collection ya que reference counting tiene varias limitaciones.

Como tipos de datos tenemos:

- **Booleans**: 'true' y 'false'.
- **Números**: flotantes de doble precision. '1234' o '12.34'.
- **Strings**: "I am a string".
- **Nil**: representa un valor nulo. 'nil'.

Expresiones:

- **Aritméticas**: sólo aplicables a números
  
  - Operaciones binarias: x+y, x-y, x*y, x/y
  - Operaciones no binarias: -x

- **Comparación e igualdad**:
  
  - Comparación: x<y, x<=y, x>y, x>=y (solo números) 
  
  - Igualdad: x == y, "x" != "y", x == "y"

- **Operadores Lógicos**: ! , and, or+

- **Precedencia y agrupación**: la precedencia es la misma a lenguajes como C o Java, si se quiere modificar se puede utilizar () .

Sentencias:

Terminadas en ; tienen como objetivo devolver un valor.

Si se desea empaquetar una serie de sentencias en una sola se pueden rodear de {} afectando al scoping.

```c
{
print "One statement.";
print "Two statements.";
}
```

Variables:

Las variables se declaran utilizando sentencias var, si no se inicializan de forma predeterminada valen nil.

```c++
var imAVariable = "here is my value";
var iAmNil;
var breakfast = "bagels";
print breakfast; // "bagels".
breakfast = "beignets";
print breakfast; // "beignets".
```

Control de Flujo:

```c
if (condition) {
print "yes";
} else {
print "no";
}
```

```c
var a = 1;
while (a < 10) {
print a;
a = a + 1;
}
```

```c
for (var a = 1; a < 10; a = a + 1) {
print a;
}
```

Funciones:

Se definen funciones con fun

```c++
makeBreakfast(bacon, eggs, toast);
makeBreakfast();

fun printSum(a, b) {
print a + b;
}
```

Clausuras:

```c++
fun identity(a) {
return a;
}
print identity(addPair)(1, 2); // Prints "3".
```

Clases:

Por que un lenguaje orientado a objetos? La mayoría del código que circula por internet actualmente es en algún lenguaje orientado a objetos y esto se debe a que puede ser bastante útil a la hora de definir tipos de datos complejos. Además de esta forma nuestro intérprete se podría considerar 'más completo'.

```c++
class Breakfast {
    cook() {
        print "Eggs a-fryin'!";
    }
    serve(who) {
        print "Enjoy your breakfast, " + who + ".";
    }
}
```

Instancias e inicialización:

Lox permite añadir propiedades a los objetos de forma libre:

```c++
breakfast.meat = "sausage";
breakfast.bread = "sourdough";
```

Y para acceder a estas propiedades desde dentro de un método utiliza el *this* de toda la vida:

```c++
class Breakfast {
    serve(who) {
        print "Enjoy your " + this.meat + " and " +
        this.bread + ", " + who + ".";
    }
    // ...
}
```

Herencia:

Herencia singular mediante el operador '<'

```c++
class Brunch < Breakfast {
    drink() {
        print "How about a Bloody Mary?";
    }
}

var benedict = Brunch("ham", "English muffin");
benedict.serve("Noble Reader");
```

Al igual que en java para el método init utilizamos super :

```c++
class Brunch < Breakfast {
    init(meat, bread, drink) {
        super.init(meat, bread);
        this.drink = drink;
    }
}
```

------

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

## 8. Declaraciones y estados

### 8.1 Declaraciones

Se añadirán 'declaraciones' a la gramática de Lox, comenzando por las dos más simples:

- La declaración de una expresión, que permite utilizar una expresión dónde se esperaría una declaración, y nos permite evaluar expresiones con efectos secundarios.
- Print, que evalua una expresión y la muestra al usuario.

La nueva sintaxis conlleva nuevas reglas gramáticas:
_program → statement* EOF ;

statement → exprStmt
                | printStmt ;

exprStmt →  expression ";" ;
printStmt → "print" expression ";" ;_

Ahora la primera regla es 'programa' que abarca un script de lox completo terminando en 'EOF'.

Se modifica GenerateAst / metaExpr para que metaprograme en un nuevo fichero 'statements.py' las distintas declaraciones al igual que lo hacía con las expresiones.

Ahora se modifica el método 'parse' del parser, y creamos uno nuevo llamado 'statement', que devuelve una declaracion print si coincide con lo que lee o una declaración de una expresion en su defecto.

Al contrario de la expresiones, las declaracions no producen valores si no vacío. Se añaden en el intérprete las clases visitantes para estas declaraciones que se han creado. Se modifica el método 'interpret' para que interprete declaraciones y se crea el método 'execute' para validar a estas.
Por último, se modifica la clase Lox, más específicamente el 'run' para que parsee declaraciones en vez de una sola expresion.

### 8.2 Variables globales

Crearemos dos nuevos contructos:

- Una declaracion de una variable, lo que crea la variable.
- Una expression variable, la cual accede a dicha variable.

Se modifica una vez más la gramática

_program → declaration* EOF ;

declaration → varDecl
                | statement ;

varDecl → "var" IDENTIFIER ( "=" expression )? ";" ;

statement → exprStmt
                | printStmt ;

primary → "true" | "false" | "nil"
                | NUMBER | STRING
                | "(" expression ")"
                | IDENTIFIER ;_

Se modifica el fichero metaExpr para que agregue estas variables tanto a expressions como a statements.
