# Crafting Interpreters

#### Mi resumen: por Eduardo del Rio Ruiz

Evaluando Expresiones/Declaraciones y Estados/Control de Flujo  

## 7. Evaluando Expresiones

 Ahora mismo el parser solo soporta las expresiones. Para ejecutar código se evaluará la expresion y se producirá un valor. Por cada exrpesión sintáctica que se puede parsear se necesitará un trozo de código que sepa como evaluar ese arbol produciendo un resultado.

#### 7.1. Representar los valores

Para representar los valores de cada tipo se necesitará una clase correspondiente en python:

| Lox type      | Python representation |
|:-------------:|:---------------------:|
| Any Lox value | Any                   |
| nil           | None                  |
| Boolean       | bool                  |
| number        | float                 |
| string        | str                   |

#### 

#### 7.2. Evaluando expresiones

Para esto se reutilizará el patrón de visitante. Creamos una nueva clase Interpreter que implemente expressions.Visitor. Para los distintos tipos de expresiones devolveremos distintos valores:

- Literales: se devuelve el valor de la expresión.

- Parentesis: se llama a evaluate() que vuelve a mandar la expresión que contiene el paréntesis al intérprete.

- Unarias: se comprueba si es un menos o una exclamación y se devuelve el valor en negativo o llama a isTruthy(). En este método se resuelve el uso de no booleanos en comparaciones lógicas, de manera que si lo que se pasa no es un booleano pero es null devuelve falso.

- Binarias: se devuelven las operaciones aritméticas y comparaciones lógicas correspondientes. Para el más definimos un resultado en caso de que la suma sea de strings. Para las igualdades creamos otra función isEqual() que compare en caso de no ser números que compruebe si ambos son null o no.

#### 7.3. Runtime Errors

Hasta ahora los errores controlados eran estáticos o sintácticos, pero ahora necesitamos controlar los errores en tiempo de ejecución. Estos se dan cuando pasamos tipos de dato no válido a nuestras operaciones. En este momento, el programa se detendría y mostraría un error en pantalla, pero esto no es lo que se quiere.

Para esto en la misma clase Interprete se crean funciones que comprueben el tipo de los datos y en caso de no ser válidos lanzen un LoxRuntimeError, error que creamos también en este fichero.

Hecho esto, se llama a estas funciones en todas nuestras expresiones antes de operar un resultado.

#### 7.4. Conectando el Intérprete

Finalmente se crea una fución interpret y stringify() para evaluar las expresiones y mostrar el resultado por pantalla. Se añade el Interprete y su llamada al programa principal Lox y se prueba su funcionamiento.

## 8. Declaraciones y Estados

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
- Una expresion de una variable, la cual accede a dicha variable.

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
