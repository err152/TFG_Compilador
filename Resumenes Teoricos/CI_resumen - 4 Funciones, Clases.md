# Crafting Interpreters

#### Mi resumen: por Eduardo del Rio Ruiz

Funciones/Resolving y Binding/Clases  

## 10. Funciones

#### 10.1. Funciones de llamada

Estas funciones de llamada tienen mayor precedencia que cualquiera de los otros operadores por lo que se modifican las siguientes reglas:

unary          → ( "!" | "-" ) unary | call ;
call           → primary ( "(" arguments? ")" )* ;

arguments      → expression ( "," expression )* ;

Se agrega un nuevo nodo al generador del árbol sintáctico.

Ahora en el parser, el método unary() en vez de llamar a primary() llamará a un nuevo método call(). Este método llama a primary() y entra en un bucle que si lee un paréntesis llama a finishCall(). Este otro método consume las expresiones que serían los argumentos de la función separandolos por las comas que va encontrando.

En el intérprete, se define una función visit_call_expr, que evalúa los argumentos y se los pasa a la función call.

Se crea una nueva interfaz LoxCallable.

Se añade al interprete en el nuevo método anteriormente creado visit_call_expr() una breve gestión de errores.

Para terminar se trata de resolver la aridad de las funciones. Se dice aridad al requerimiento de cierto número de parámetros de la función, si una función en su definición recibe 3 parámetros, se le deberán pasar 3 parámetros a la hora de llamarla. Esto lo solucionamos en la misma función visit_call_expr().



#### 10.2. Funciones nativas

Una vez se tienen las funciones de llamada se necesitarán funciones a las que llamar, a las que se denomina **funciones nativas**. Estas son expuestas por el intérprete al codigo de usuario pero son implementadas en el idioma anfitrión (python) y no en el idioma implementado (Lox).

Algunos lenguajes permiten a los usuarios definir sus propias funciones nativas mediante un mecanismo llamado **FFI** (Foreign Function Interface), **native extension** o **native interface**, pero esto no será implementado en nuestro intérprete.

QUIZÁS NO ME HAGA FALTA (Ahora se tratará de realizar un poco de benchmarking para hacer más sencilla la optimización del interprete en un futuro.

Para ello trataremos de calcular la diferencia entre dos llamadas consecutivas.)



#### 10.3. Declaración de funciones

Se añaden las siguientes reglas a nuestra gramática:

declaration    → funDecl
                       | varDecl
                       | statement ;

funDecl        → "fun" function ;
function       → IDENTIFIER "(" parameters? ")" block ;

parameters     → IDENTIFIER ( "," IDENTIFIER )* ;



Se añade Function a metaExpr y se realizan un par de cambios en el parser:

- Se modifica declaration() para que identifique la definición de funciones al leer el token "fun".

- Se añade la función function() que ya dentro de la declaración de la función consume el identificador de la misma o devuelve un error en caso contrario.

- Ahora dentro de function() gestionamos los parámetros  y llamamos al cuerpo de la función.



#### 10.4. Objetos de las funciones

Falta definir algún tipo de recipiente donde guardar las funciones, esto lo hace statements.Function pero es necesaria una clase LoxFunction que implemente a LoxCallable para poder llamar a las funciones.

Se crea esta clase LoxCallable con sus repsectivos métodos arity, un __str__ para imprimir por pantalla su valor, y call() que será el que ejecute la función.

Se añade al intérprete un vist_function_stmt para procesar estas funciones.



#### 10.5. Declaraciones de retorno

Es el momento de añadir las declaraciones de retorno.

statement      → exprStmt
                   | forStmt
                   | ifStmt
                   | printStmt
                   | returnStmt
                   | whileStmt
                   | block ;

returnStmt     → "return" expression? ";" ;



Un return comienza con el token "return" y puede ir acompañado de una expresión o no, para poder salir de una función que retorna un valor inútil antes.

Toda función debe retornar algo, en su defecto None.

Se añade return a metaExpr y se modifica el parser:

- Se modifica que statement llame a returnStatement() cuando lee el token "return".

- Se crea el método returnStatement() que trata la declaracion de retorno.



Retornar puede ser algo complicado. Se puede retornar desde cualquier parte dentro del cuerpo de una función, incluso desde dentro de multiples declaraciones anidadas. Cuando el retorno es ejecutado, el intérprete tiene que saltar fuera del contexto en el que esté y de alguna manera completar la función.

Se modifica el interprete con un nuevo método visit_return_statement(). En este método tomamos el valor del statement en el que nos encontramos y generamos una excepción Return.

Return será una nueva clase que definiremos y extenderá RuntimeError. Esta llama al constructor de RuntimeError sin parámetros,  y guarda el valor del statement que se le pasa.

A continuación, en LoxFunction en la función call(), rodeamos la ejecución del bloque en un try que en caso de detectar un error de tipo Return retorne el valor del error, que sería el del statement actual.



#### 10.6. Funciones y Cierres locales



 
