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

Se crea una nueva clase Resolver. A la hora de resolver variables solo interesan un par de nodos:

- La declaración de un bloque introduce un nuevo scope para las declaraciones que contiene.

- La declaración de una función introduce un nuevo scope para su cuerpoy vincula sus parámetros a este scope.

- La declaración de una variable añade la variable al scope actual.

- Las expresiones de variables y asignaciones necesitan tener sus variables resueltas.

El resto de nodos no hacen nada especial, aunque se tendrán que visitar de todas formas para recorrer el árbol.

Esta clase tiene como atributos: un intérprete, en el que se guardanlos resultados; una lista de diccionarios 'scopes' en la que se van simulando la creación de entornos y guardando el estado (inicializadas o no) de las variables que se necesiten resolver; y un entorno 'currentFunction'  mediante el que se resuelven las clausuras.

Empezando por los bloques se crea un método resolve() que pasada una lista de declaraciones llama a resolve() para cada una de ellas. A su vez si esta recibe una sentencia o una expresion llama a sus métodos acepta() para ser resueltas.

Se crea ahora un método visit_block_stmt() en el que se llama a beginScope(), función que guarda un diccionario vacío en una lista scopes que tiene la clase Revolver() como atributo. Seguido, llama a resolve para la lista de declaraciones, y luego llama a endScope(), función que extrae un diccionario de la lista scopes.

Para la declaracion de variables se diferencia entre la declaración y la definición. Se añade un nuevo método visit_var_stmt() que llama a declare(), resuelve la variable y llama a define().

¿Qué ocurre cuando el inicializador de una variable local hace referencia a una variable con el mismo nombre que la variable que se está declarando? Se tienen diferentes formas de actuar:

1. Inicializar y luego añadir la nueva variable en el scope.

2. Añadir la nueva variable al scope y luego inicializarla.

3. Que esto devuelva un error.

Como las primeras tienden a producir errores de usuario, se implementará la tercera.

Primero se define la declaración que agrega la variable al scope más interno, de manera que  oculta cualquier scope externo y así sabemos que la variable existe.  La marcamos como "no lista todavía" al vincular su nombre a `False` en el diccionario scope.

Se crea ahora el método visit_var_expr(), en el que primero se comprueba si la variable está siendo accedida desde dentro de su inicialización. Si la variable existe en actual scope pero tiene valor False, se retorna un error. Si no, se llama a resolveLocal(), función que de manera similar al Entorno busca desde el scope actual hacia arriba en busqueda de la variable, si se encuentra se resuelve pasandole el número de saltos entre scopes que se han realizado.

Para las asignaciones, tan solo se resuelve la expresion en visit_assign_expr.

Para las funciones, se declara y define la declaración y se llama a la funcion resolveFunction(), la cual abre un scope, declara y define los parámetros de la función, resuelve el cuerpo de esta y cierra el scope.

Finalmente, se añaden los demás nodos en los que no se hace nada especial más allá de resolver sus diferentes componentes.

#### 11.4. Interpretando Variables Resueltas

Veamos de que sirve el Resolver. Cada vez que se visita una variable, comunica al interprete el número de scopes que hay entre el actual y donde está definida la variable. Creamos un método resolve() que guarde en una nueva lista *locals* las expresiones y el numero de saltos para acceder a ellas.

Se modifica visit_var_expr() para que llame a una nueva función lookUpVariable() que comprueba en *locals* la distancia de la expresion que se va a tratar. Si la distancia no es nula llama a una nueva función del entorno llamada getAt(), de lo contrario toma el valor de *globals*.

En este momento se vuelve a desviar el contenido respecto del libro. En este caso, la función getAt() recibe una lista de distancias y un nombre de variable. Primeramente llama a un método auxiliar el cual crea una lista de diccionarios en la que almacena los distintos entornos a los que se quiere acceder mediante las distancias. Luego, para cada diccionario busca la variable y si la encuentra la retorna. Si no la encuentra y el entorno de clausura no es nulo se llama recursivamente a getAt() sobre este entorno de clausura con la misma lista de distancias; por último, si de ninguna de las maneras se encuentra la variable, se produce una excepción RuntimeError que el método lookUpVariable gestiona llamando al get() básico que buscará la variable en globals de forma normal.

De igual manera se hace con visit_assign_expr(), en este caso llamando a assignAt() que actúa de la misma manera que getAt() pero dando valor a las variables una vez las encuentra.

Para estos 3 métodos nos hemos ceñido una vez más al principio DRY tratando de refactorizar el código todo lo posible para no repetir acciones. Se han utilizado operadores Walrus.

Finalmente, se añade al programa principal la definición del resolver, y se hace una llamada a resolve() sobre el interprete antes de ser este otro ejecutado, para que en el momento en que se llame a interpret() tenga ya la lista con distancias para acceder a las variables de manera mucho más rápida. 

#### 11.5. Errores de Resolución

Se añade control de erores al Resolver para los casos en los que en un scope local se crean dos variables con un mismo nombre, y para prevenir llamadas return fuera de ningún scope.

<<<<<<< HEAD


=======
>>>>>>> clases
## 12. Clases

Se podría terminar el Interprete aquí pero hoy en día muchos lenguajes de programación populares soportan la programación orientada a objetos. Añadirlo será un extra para darle cierta familiaridad a los usuarios.

<<<<<<< HEAD


=======
>>>>>>> clases
#### 12.1. OOP y Clases

Existen 3 caminos hacia la programación orientada a objetos: clases, prototipos y multimétodos. Las clases fueron las primeras en inventarse y son las más populares actualmente.

El principal objetivo de una clase es agrupar datos con el código que actúa sobre ellos. Para eso los usuarios declaran una clase que:

- Expone un constructor que crea e inicializa nuevas instancias de la clase.

- Poporciona una manera de guardar y acceder a los campos de estas instancias.

- Define un grupo de métodos compartidos por todas las instancias de la misma clase que operan sobre el estado de cada instancia.

Ese sería un resumen muy general. Muchos lenguajes programados a objetos también implementan herencia para reutilizar el comportamiento entre clases, pero hasta aquí llegará este proyecto.

<<<<<<< HEAD


=======
>>>>>>> clases
#### 12.2. Declaración de Clases

Se comienza modificando la sintáxis. Cambian las reglas de nuestra gramática.

declaration    → classDecl
               | funDecl
               | varDecl
               | statement ;

classDecl      → "class" IDENTIFIER "{" function* "}" ;

<<<<<<< HEAD


=======
>>>>>>> clases
En Lox las clases se definen mediante la palabra clave "class" seguida del nombre de la clase. En su cuerpo se definen los métodos al igual que las funciones pero sin ser precedidas de la palabra clave "fun".

> class Breakfast {
>   cook() {
>     print "Eggs a-fryin'!";
>   }
>   serve(who) {
>     print "Enjoy your breakfast, " + who + ".";
>   }
> }

<<<<<<< HEAD


Se añade la regla classDecl al generador AST metaExpr. Esta guarda el nombre de la clase y los métodos en su cuerpo

Se añade en el parser en la función declaration() la detección del token CLASS. También se añade una nueva función classDeclaration(). Esta función consume un token que corresponde al nombre, gestiona los corchetes que definen el cuerpo y crea una lista en la que guarda los métodos de la clase.
=======
Se añade la regla classDecl al generador AST metaExpr. Esta guarda el nombre de la clase y los métodos en su cuerpo

Se añade en el parser en la función declaration() la detección del token CLASS. También se añade una nueva función classDeclaration(). Esta función consume un token que corresponde al nombre, gestiona los corchetes que definen el cuerpo y crea una lista en la que guarda los métodos de la clase.

Se añade también un método visit_class_stmt tanto al resolver como al intérprete. En el resolver, declaramos y definimos la sentencia. En el intérprete,  definimos la sentencia en el entorno ent, creamos una clase LoxClass y asignamos esta clase a la sentencia.

LoxClass es una nueva clase que creamos en el fichero LoxClass.py. En un principio esta clase tan solo contiene un constructor que inicializa el atributo nombre de la clase, y un método \_\_repr\_\_ para mostrar el nombre cuando la clase se tenga que mostrar.

En este momento, se comprueba si se parsean bien las clases con un pequeño programa de prueba que define una clase con un método y fuera de la clase hace un print de la clase. Como resultado se obtiene el nombre de la clase, tal y como se espera.

#### 12.3. Creando Instancias

Lox no tiene métodos estáticos a los que llamar dentro de la propia clase, por lo que sin instancias las clases son inútiles. Para crear estas instancias se hace uso de las clases y las funciones de llamada, de forma que una instancia sea una llamada a las clases. 

El primer paso es hacer que la clase LoxClass implemente LoxCallable y por ello definir las funciones call() y arity() heredadas. La función call() crea y retorna una instancia de la propia clase, mientras que arity() retorna directamente 0 ya que la llamada a la clase no recibe argumentos.

Toca crear la clase LoxInstance en un nuevo fichero LoxInstance.py. De momento solo definimos un \_\_init\_\_ en el que inicializamos una clase como atributo, y un \_\_repr\_\_ que imprima el nombre de la clase seguido de " instance".

Se comprueba que esto funciona creando otro fichero de prueba simpel que crea una clase vacía, inicializia una nueva variable con esta clase y hace un print de la variable.

#### 12.4. Propiedades de las Instancias

Cada instancia es una colección de valores nombrados. Los métodos tanto de dentro como de fuera de la clase pueden modificar los valores o propiedades de las clases. Si estas propiedades se acceden desde fuera se utiliza el carácter '.'. Este punto tiene la misma precedencia que el paréntesis de una llamada a una función por lo que se modifica la regla de llamada para incluirlo.

call           → primary ( "(" arguments? ")" | "." IDENTIFIER )* ;

###### 12.4.1. Expresiones Get

Se añade un nodo al árbol sintáctico y se modifíca el parser para que en la función call() si detecta '.' cree una expression Get con el identificador que continua el punto.

De igual manera se añade el método visit_get_expr tanto en el Resolver como en el Intérprete. Las propiedades no son resueltas ya que se visitan de forma dinámica. Por otro lado, en el intérprete se evalua la expresión y si el resultado es del tipo LoxInstance se trata de acceder a la propiedad, si no lo fuera se devuelve un error.

Es momento de añadir estados a las instancias. Se crea un diccionario en LoxInstance que inicializamos vacío en el constructor.

Definimos el método get mediante el que se accede a las propiedades de la instancia.

###### 12.4.2. Expresiones Set

Los setters tienen la misma sintáxis que los getters pero se situan en el lado izquierdo de la asignación. Por tanto, se modifica la regla de la gramática correspondiente a la asignación de la siguiente manera.

assignment     → ( call "." )? IDENTIFIER "=" assignment
               | logic_or ;

A diferencia de los getters, los setters no encadenan. Si tengo una sentencia "libro.novela.genero = romance" solo ".genero" actúa como setter.

Añadimos un nuevo nodo al generador AST.

Para el parser hacemos lo siguiente. Parseamos la parte izquierda de la asignación como una expresión normal y en el momento en el que llegamos al símbolo de igualdad tomamos esta expresión ya parseada y la tranformamos en el nodo del árbol sintáctico correcto para la asignación.

En el Resolver se añade visit_set_expr que resuelve el valor y el objeto a asignar.

En el Intérprete se evalua el objeto cuya propiedad se va a modificar y se comprueba si es del tipo LoxInstance. Si no lo es se genera un error. Si lo es se evalua el valor que se va a asignar y se guarda en la instancia mediante un método set que añadimos a la clase LoxInstance para añadir propiedades y sus respectivos valores al diccionario fields.

#### 12.5. Métodos en las Clases

En este punto se pueden crear instancias de clases y almacenar datos en ellas, pero las clases en sí no hacen nada. Las instancias no son más que simples diccionarios. El siguiente paso es añadir métodos de comportamiento.

En nuestra función visit_class_stmt del Resolver, añadimos un bucle que recorra los métodos de la clase, resolviendolos pasándole como argumento un nuevo valor del enumerado FunctionType 'METHOD'.

Ahora se pasa a modificar el Intérprete. En la misma función visit_class_stmt recorremos de igual modo los métodos de la clase, esta vez creando un objeto LoxFunction para cada uno de los métodos y añadiéndolos a un diccionario methods que se pasará como parámetro en el momento de creación de la clase.

Para que esto funcione se modifica LoxClass para recibir en el constructor este diccionario de funciones.

Las clases guardan los métodos mientras que sus instancias guardan los atributos o propiedades. Pero aún así, se accede a estos métodos a partir de las instancias, por lo que se añade al método get de LoxInstance una búsqueda del método en cuestión en la clase que contiene como atributo mediante un nuevo método llamado findMethod. Este métod se crea en la clase LoxClass y no hace más que buscar en el diccionario methods un método específico.

Se prueba que todo esto funciona nuevamente con otro pequeño programa de prueba prueba_clases3.lox.

#### 12.6. This

Lo siguiente es añadir una manera de acceder a las propiedades de la clase desde los métodos de esta, es decir el "this" de Java o el "self" de python.

Se añade un nuevo nodo a la sintáxis y se modifica el método primary() del parser para reconocer la palabra clave this.

En el resolver se crea un método visit_this_expr() que llama a resolveLocal(), pero this no es una variable que esté en el scope por lo que se modifica visit_class_stmt() para que despues de definir la variable, abra un nuevo scope y añada this a este, y antes de terminar cierre este nuevo scope.

Se modifica en get() de LoxInstance la linea que retornaba el método si este estaba vacío para que devuelva la llamada a bind(self) del método. La función bind() de LoxFunction crea un nuevo entorno en el que define "this" y retorna una función pasándole la declaración de la función y este nuevo entorno a su constructor.

Por último se crea el método visit_this_expr en el Intérprete para que busca la variable.

###### 12.6.1. Usos no válidos de This

¿Qué ocurre si se intenta acceder a this fuera de un método? esto no debería poderse hacer, se tiene que resolver este problema.

Para ello se crea un nuevo enumerado en el Resolver llamado ClassType que diferencia entre clases y no clases, y añadimos un atributo al resolver de este tipo inicializado a NONE. Este atributo lo cambiaremos a CLASS cuando se entra a visit_class_expr y se retornará a su estado previo antes de salir de este mismo método.

En visit_this_expr ahora se comprobará el tipo de clase actual y en caso de no ser de tipo clase se generará un error.

#### 12.7. Constructores e Inicializadores.

La construcción de un objeto se puede separar en dos partes:

- Se reserva espacio en memoria para la nueva instancia.

- Se hace una llamada a un código que inicializa el objeto por formar.



Toca crear el constructor de nuestras clases. Cuando una clase es llamada, justo despues de crear la nueva instancia se busca un método "init", utilizando el formato que sigue python para los constructores, y si se encuentra inmediatamente se vincula y se invoca pasandole la lista de argumentos.

Ahora que la clase llama al constructor y esta puede recibir argumentos, se tiene que modificar el método de aridad de la clase que se tenía puesto a un valor fijo de 0.



###### 12.7.1. Invocando init() directamente

En caso de llamarse directamente al método init() de una clase ya inicializada se ha decidido retornar el valor this. Para esto se modifica LoxFunction para que en el método call compruebe antes de retornar un valor si la función es una función de inicialización, si lo es retorna this, si no lo es retorna el valor a devolver.

La manera de comprobar si es una función de inicialización es crear un nuevo atributo booleano isInitializer que lo indique, y modificar el constructor de LoxFunction para recibir este booleano como argumento para su constructor.



###### 12.7.2. Retornando de init()

¿Qué pasaría si se tratase de retornar un valor en el constructor? Esto es algo que normalmente se trata de evitar ya que el constructor debe devolver el objeto creado.

La solución a este problema es crear un nuevo FunctionType en el Resolver 'INITIALIZER', en visit_class_stmt cuando se comprueban los métodos si el nombre del método es "init" se declara la función bajo este nuevo tipo, y lanzar un error en visit_return_stmt si el tipo de la función a retornar es initializer. 

Hecho esto todavía no se cubre el caso de hacer un return aislado en la inicialización. Esto se gestiona desde la función call de LoxFunction cuando se trata la excepción Return, si la función actual es inicializadora se busca this en el entorno de clausura. 
>>>>>>> clases
