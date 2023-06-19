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

Hasta ahora, siempre han sido globals, el entorno global superior al actual. De esta manera cuando no se encuentra un identificador en un entorno local se busca en el inmediatamente superior.

Pero en Lox las declaraciones de funciones son permitidas en cualquier lugar dónde se pueda vincular un nombre.

Denominamos **cierre** (closure) a una combinación de una función y el entorno léxico dentro del cual se define esa función. Es un concepto poderoso que permite a las funciones "recordar" y acceder a variables de su ámbito externo incluso después de que ese ámbito haya terminado de ejecutarse.

En este apartado, nuevamente, se realiza una implementación distinta a la del libro.

Se añade en LoxFunction un nuevo entorno de cierre "closure" que funciona como copia del entorno en el momento de definición de la función. Esto se guarda en su constructor el cual llamamos dentro del Interprete en la función visit_function_stmt.

Hasta aquí todo está como en el libro, pero ahora en la clase Entorno añadimos también un atributo "closure_function" el cual se utiliza para guardar el entorno capturado en el momento de la definición en el caso de las funciones que hemos mencionado anteriormente. Al hacer esto, modificando las funciones get y assign, se pueden buscar las variables tanto en values, como en el stack, como en este nuevo entorno. Hecho esto solo falta asignar este closure_function. Esto se hace en el momento de la llamada a la función, en el call(). Cuando se lleva a cabo la llamada se asigna el entorno que tenemos copiado en la LoxFunction al closure_function del entorno actual, para después operar la función como ya se había definido anteriormente.



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

Se crea una nueva clase Resolver. Ala hora de resolver variables solo interesan un par de nodos:

- La declaración de un bloque introduce un nuevo scope para las declaraciones que contiene.

- La declaración de una función introduce un nuevo scope para su cuerpoy vincula sus parámetros a este scope.

- La declaración de una variable añade la variable al scope actual.

- Las expresiones de variables y asignaciones necesitan tener sus variables resueltas.

El resto de nodos no hacen nada especial, aunque se tendrán que visitar de todas formas para recorrer el árbol.

Empezando por los bloques se crea un método resolve() que pasada una lista de declaraciones llama a resolve() para cada una de ellas. A su vez si esta recibe una declaracion o una expresion llama a sus métodos acepta() para ser resueltas.

Se crea ahora un método visit_block_stmt() en el que se llama a beginScope(), función que guarda un diccionario vacío en una lista scopes que tiene la clase Revolver() como atributo. Seguido, llama a resolve para la lista de declaraciones, y luego llama a endScope(), función que extrae un diccionario de la lista scopes.

Para la declaracion de variables se diferencia entre la declaración y la definición. Se añade un nuevo método visit_var_stmt() que llama a declare(), resuelve la variable y llama a define().

¿Qué ocurre cuando el inicializador de una variable local hace referencia a una 
variable con el mismo nombre que la variable que se está declarando? Se tienen diferentes formas de actuar:

1. Inicializar y luego añadir la nueva variable en el scope.

2. Añadir la nueva variable al scope y luego inicializarla.

3. Que esto devuelva un error.

Como las priemras tienden a producir errores de usuario, se implementará la tercera.

Primero se define la declaración que agrega la variable al scope más interno, de manera que  oculta cualquier scope externo y así sabemos que la variable existe.  La marcamos como "no lista todavía" al vincular su nombre a `False` en el diccionario scope.

Se crea ahora el método visit_var_expr(), en el que primero se comprueba si la variable está siendo accedida desde dentro de su inicialización. Si la variable existe en actual scope pero tiene valor False, se retorna un error. Si no, se llama a resolveLocal(), función que de manera similar al Entorno busca desde el scope actual hacia arriba en busqueda de la variable, si se encuentra se resuelve pasandole el número de saltos entre scopes que se han realizado.

Para las asignaciones, tan solo se resuelve la expresion en visit_assign_expr.

Para las funciones, se declara y define la declaración y se llama a la funcion resolveFunction(), la cual abre un scope, declara y define los parámetros de la función, resuelve el cuerpo de esta y cierra el scope.

Finalmente, se añaden los demás nodos en los que no se hace nada especial más allá de resolver sus diferentes componentes.

#### 11.4. Interpretando Variables Resueltas

Veamos de que sirve el Resolver. Cada vez que se visita una variable, comunica al interprete el número de scopes que hay entre el actual y donde está definida la variable. Creamos un método resolve() que guarde en una lista *locals* las expresiones y el numero de salto para acceder a ellas.

Se modifica visit_var_expr() para que llame a una nueva función lookUpVariable() que comprueba en *locals* la distancia de la expresion que se va a tratar. Si la distancia no es nula llama a getAt() de lo contrario toma el valor de *globals*. La función getAt() devuelve el valor de la variable que le retorna ancestor(), función que devuelve el entorno a x saltos, pasandose x como parámetro.

De igual manera hacemos con visit_assign_expr(), en este caso llamando a assignAt() que también llamará a ancestor().

Finalmente, se añade al programa principal la definición del resolver y llamamos a resolve() antes que al interpret().

#### 11.5. Errores de Resolución

Se añade control de erores al Resolver para los casos en los que en un scope local se crean dos variables con un mismo nombre, y para prevenir llamadas return fuera de ningún scope.
