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
