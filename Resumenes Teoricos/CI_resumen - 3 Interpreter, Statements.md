# Crafting Interpreters

#### Mi resumen: por Eduardo del Rio Ruiz

Evaluando Expresiones/Declaraciones y Estados/Control de Flujo  

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
