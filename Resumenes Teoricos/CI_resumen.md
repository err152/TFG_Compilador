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

-  Single-pass compilers: entrelaza parsing, analisis y generación de código generando código ejecutable directamente desde el parser.
- Tree-walk interpreters: ejecuta codigo justo despues del parsing, recorriendo el árbol sintáctico rama por rama y hoja por hoja linealmente.
- Transpilers: a la hora de 'bajar de nivel' a nuestro código podemos tratar de generar un código homólogo en otro idioma de alto lenguaje distinto, y utilizar las herramientas de compilación ya existentes de este para generar el código máquina.
- JIT:



#### Compiladores e Interpretes

Compilar es una técnica de implementación que trata de traducir un lenguaje fuente a otra forma, normalmente a nivel inferior. 

Un intérprete además de traducir el lenguaje lo ejecuta.

------



## 3. El lenguaje Lox

