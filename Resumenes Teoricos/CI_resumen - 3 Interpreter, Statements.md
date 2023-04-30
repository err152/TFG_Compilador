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

#### 8.1 Declaraciones

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

#### 8.2 Variables globales

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

La método de entrada al parser cambia, ya que el nivel superior del programa ahora es una lista de declaraciones y no expresiones.

Para ello se crea un nuevo método declaration() que conecta con la recuperación de errores realizada anteriormente que no se llegó a utilizar. Este método es un buen punto para sincronizar el parser cuando entre en modo pánico ya que se le llama repetidas veces según se parsea.

Ahora definimos la función varDeclaration() que crea las variables de forma que inicializa la variable como null si no se detecta un token '='.

Finalmente se añade el caso del indentificador al la función primary().

#### 8.3. Entornos

Las asignaciones que asocian las variables con sus valores deben estar almacenadas en algún sitio. Este sitio se llama entorno (Enviroment).

Se crea una nueva clase Entorno que tendrá como atributo un diccionario con las variables y sus respectivos valores. Se definen las siguientes funciones:

- define(name,value) para añadir las nuevas variables a esta lista.

- get(name) para comprobar si ya existe una variable.

Volviendo al Interprete, ahora se crea un entorno como atributo de manera que guarde los valores hasta que este termine de ejecutar. 

Dado que se tienen dos nuevos arboles sintacticos se deberán crear dos nuevas funciones visit, una para cada una.

#### 8.4. Asignación

En Lox se permite la reasignación de las variables. Aquí se presenta un problema y es que la comparación de igualdad está a uno de los niveles más bajos en nuestra gramática. Se tendrá que modificar el parser y añadir una nueva expresión.

Se añade a parser la función assignment() para solucionar este problema.

Ahora se tiene un nuevo nodo en nuestro árbol semántico que se define en el intérprete como visit_assign_expr(expr).

En Entorno se añade assign(name,value).

#### 8.5. Scope

Un scope define la region donde los nombre se mapea a una cierta entidad. Multiples scopes permiten al mismo nombre referirse a diferentes cosas en diferentes contextos.

Lexical Scope es un tipo específico de scoping donde el texto de un programa se muestra donde empieza y termina un scope. Por otro lado tenemos Scope Dinámico en donde no se sabe a que se refiere un nombre hasta que se ejecuta el código. Lox no tiene variables scopeadas dinámicamente, pero si métodos y campos en objetos.

Una primera aproximación a implementar el scoping podría funcionar así:

1. Según se visita cada declaración dentro de un bloque, se realiza un seguimiento de cualquier variable declarada.

2. Cuando la última declaración se ejecuta, se le pide al entorno que borre todas esas variables.

Esto no funciona del todo bien. Cuando una variable local tiene el mismo nombre que una variable en dentro de un scope, esta hace sombra a la exterior de manera que ya no puede acceder a esta otra, pero sigue estando ahí y volverá una vez se ejecute el scope.

Se añade a la clase Entorno un atributo de su mismo tipo y se crean constructores para inicializarlo. También se modifican los métodos get() y assign() de manera que busquen las variables en el entorno y si no las encuentran comprueben el entorno exterior de forma recursiva.

## 9. Control de Flujo

"Logic, like whiskey, loses its beneficial effect when taken in too large quantities" - Edward John Moreton Drax Plunkett, Lord Dunsany

El siguiente paso para nuestro intérprete será lograr que sea Turing-completo.

#### 9.1. Máquinas de Turing

Las máquinas de Turing son un pequeño sistema que con la mínima maquinaria es capaz de calcular cualquiera de una clase (muy) grande de funciones.

Cualquier lenguaje de programación con un mínimo nivel de expresividad es suficientemente potente como para calcular cualquier función computable.

Esto se puede probar escribiendo un simulador de maquinas de Turing en tu lenguaje. Ya que Turing lo demostró para su máquina, eso significaría que tu lenguaje tambíen. Solo hay que traducir la función en una máquina de Turing, y luego probarlo en tu simulador.

Si tu lenguaje puede hacerlo, se le considera Turing-completo. Las máquinas de Turing son muy simples, solamente se necesita aritmética, un poco de control de flujo y la habilidad de asignar y utilizar cantidades arbitrarias de memoria. Se tiene lo primero, ahora iremos a por lo segundo.

## 9.2. Ejecución Condicional

Podemos dividir el control de flujo en dos tipos:

- Condicional o control de flujo en ramas (**Branching**), es utilizado para no ejecutar ciertos trozos del código. Saltar por encima de partes del código.

- Control de flujo en bucles (**Looping**), ejecuta cierta parte del código más de una vez. Salta hacia atrás para voler a hacer algo, y para no entrar en bucles infinitos se tiene alguna condición lógica para salir de este.

El branching es más simple así que se empezará por ahí. Lox no tiene operadores condicionales, así que se implementará la declaración **if** lo primero de todo. Nuestra gramática de statements gana una nueva producción:

statement      → exprStmt
                   | ifStmt
                   | printStmt
                   | block ;

ifStmt         → "if" "(" expression ")" statement
                   ( "else" statement )? ;

Un statement if tiene una expresion para la condición, y un statement que ejecutar si la condición es cierta. Opcionalmente, puede tener un else y otro statement que ejecutar si la condición es falsa. Agregamos If al árbol sintáctico.

Se añade también que el parser reconozca estos statements cuando lee el Token IF y llame al método ifStatement que parsee el resto. Si encuentra un Token else crea el statement y si no lo deja a None.

Este statement else genera un problema de ambigüedad. Considera:

```
if (first) if (second) whenTrue(); else whenFalse();
```

¿A qué if pertenece el else? Tenemos que solucionar esto. En nuestro caso el else pertenecerá al if más cercano a este mismo, ya que if busca un else antes de retornar. De momento esto nos sirve y podemos pasar al intérprete, donde se añade un método visit_if_stmt que procese los ifs.

#### 9.3. Operadores Lógicos

Ahora se implementarán los operadores lógicos **and** y **or**. Estos funcionan de distinta manera ya que dependen del resultado de uno de los dos lados de la operación para producir su resultado. Es por esto que van separados del resto de operadores binarios.

expression     → assignment ;
assignment     → IDENTIFIER "=" assignment
                       | logic_or ;
logic_or       → logic_and ( "or" logic_and )* ;
logic_and      → equality ( "and" equality )* ;



Se añade al generador y en el parser ahora assignment() en vez de llamar a equality() llamará a orr(). Se definen los métodos orr() y andd(). Y en el intérprete se añade el método visit_logical_expr() después de visit_literal_expr().



#### 9.4. Bucles While

Lox cuenta con dos tipos de control de flujo por bucles, **while** y **for**. Se empieza por el bucle while al ser este más sencillo.

statement      → exprStmt
                       | ifStmt
                       | printStmt
                       | whileStmt
                       | block ;

whileStmt      → "while" "(" expression ")" statement ;

Se añade While al generador,al parser con su método whileStatement(), y al intérprete con el método visit_while_stmt().
