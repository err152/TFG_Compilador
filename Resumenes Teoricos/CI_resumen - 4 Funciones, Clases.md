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

Nuestra implementación de call() crea un nuevo entorno al que vincula los parámetros de las funciones. Pero, ¿quién es el *padre* de este entorno?

Hasta ahora, siempre han sido globals, el entorno global superior al actual. De esta manera cuando no se encuentra un identificador en un entorno local se busca en el inmediatamente superior. (Checkear ejemplo Fibonacci)

Pero en Lox las declaraciones de funciones son permitidas en cualquier lugar dónde se pueda vincular un nombre.

Denominamos **cierre** (closure) a una combinación de una función y el entorno léxico dentro del cual se define esa función. Es un concepto poderoso que permite a las funciones "recordar" y acceder a variables de su ámbito externo incluso después de que ese ámbito haya terminado de ejecutarse.



Se añade en LoxFunction un nuevo entorno de cierre "closure". En el intérprete cuando se crea una función, se captura el entorno actual. Finalmente, cuando se llama a la funión call(), se utiliza este entorno de cierre como padre en vez de ir directamente al entorno global.



## 11. Resolución y vinculación

Un brecha se ha producido en nuestro barco al implementar los cierres.



#### 11.1. Static Scope

El uso de una variable se refiere a la declaración previa con el mismo nombre en el ámbito más interno que engloba la expresión en la que se utiliza la variable.

Analicemos esta frase:

- Se dice "uso de una variable" en vez de "expresión de una variable" para abarcar expresiones y asignaciones.

- "Previa" significa que aparece antes en el texto del programa.

- "Más interno" se utiliza por el shadowing. Puede haber más de una variable con el mismo nombre en un entorno circundante.

Dado el siguiente código:

```Lox
var a = "global";
{
  fun showA() {
    print a;
  }

  showA();
  var a = "block";
  showA();
}
```

Si estas familiarizado con scopes y closures el resultado debería ser "global" dos veces. Ya que la misma función debería acceder siempre a la misma variable.

Pero en este caso se devuelve "global" "block".



#### 11.2. Análisis Semántico

Nuestro intérprete resuelve una variable cada vez que la expresión variable es evaluada. Si esta variable está dentro de un bucle que se ejecuta 100 veces, la variable será resuelta 100 veces.

La solución es escribir un programa que investigue todo el código, encuentre cada variable mencionada, y encuentre a que declaración se refiere cada una. Este proceso es un ejemplo de **análisis semántico**. Mientras que el parser solo comprueba si el programa es gramáticamente correcto, el análisis semántico va un paso más allá y averigua lo que significa en realidad cada pieza del código.

La clave para solucionar nuestro error será medir los saltos entre entornos que se realizan para buscar las referencias a las variables. De manera que estos saltos se almacenen y siempre se realice el mismo número de saltos, accediendo siempre al mismo resultado.

Después de que el parser produzca el árbol sintáctico, pero antes de que el intérprete comience a ejecutarlo, se realizará un paseo por el árbol para resolver todas las variables que contenga.

En este paseo se visitan todos los nodos, pero un análisis estático es diferente de una ejecución dinámica:

- No tiene efectos secundarios. No ejecuta nada por lo que no tiene efecto.

- No tiene control de flujo. Los bucles son visitados una única vez. Ambas ramas son visitadas en los bucles if. Los operadores lógicos no son cortocircuitados.



#### 11.3. Una clase Resolver

Se crea una nueva clase Resolver.
