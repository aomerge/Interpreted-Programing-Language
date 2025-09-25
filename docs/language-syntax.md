# Sintaxis y Referencia del Lenguaje LPP

LPP es un lenguaje de programación interpretado con sintaxis similar a JavaScript. Esta guía cubre toda la sintaxis y características del lenguaje.

## 📋 Tabla de Contenidos

- [Elementos Básicos](#elementos-básicos)
- [Variables](#variables)
- [Tipos de Datos](#tipos-de-datos)
- [Operadores](#operadores)
- [Funciones](#funciones)
- [Estructuras de Control](#estructuras-de-control)
- [Expresiones](#expresiones)
- [Comentarios](#comentarios)
- [Palabras Reservadas](#palabras-reservadas)
- [BNF y Gramática](#bnf-y-gramática)

## 🔤 Elementos Básicos

### Terminadores de Declaración
Todas las declaraciones deben terminar con punto y coma `;`

```javascript
let x = 5;
return x;
```

### Identificadores
Los identificadores deben:
- Comenzar con letra (a-z, A-Z) o guión bajo (_)
- Continuar con letras, números o guiones bajos
- Ser sensibles a mayúsculas y minúsculas

**Válidos:**
```javascript
variable
_privada
miVariable
numero1
CONSTANTE
```

**Inválidos:**
```javascript
1variable    // No puede empezar con número
mi-variable  // No se permiten guiones
let         // Palabra reservada
```

## 🔧 Variables

### Declaración
```javascript
// Declaración básica
let nombre_variable = valor;

// Ejemplos
let numero = 42;
let texto = "Hola mundo";
let activo = true;
```

### Asignación
```javascript
// Asignación después de declaración
numero = 100;
texto = "Nuevo valor";
activo = false;
```

### Reasignación
```javascript
let contador = 0;
contador = contador + 1;  // contador vale 1
contador = 10;            // contador vale 10
```

## 📊 Tipos de Datos

### Números (Number)
```javascript
// Enteros
let entero = 42;
let negativo = -10;
let cero = 0;

// Decimales
let decimal = 3.14159;
let pequeno = 0.001;
let cientifico = 1.23e-4;  // Pendiente de implementación
```

### Cadenas de Texto (String)
```javascript
// Comillas dobles
let saludo = "Hola, mundo!";

// Comillas simples
let despedida = 'Adiós';

// Cadenas vacías
let vacia = "";
let vacia2 = '';

// Caracteres especiales
let especial = "Línea 1\nLínea 2\tTabulada";
```

#### Escape de Caracteres
```javascript
let comillas = "Él dijo: \"Hola\"";
let apostrofe = 'It\'s working';
let barra = "Ruta: C:\\Usuario\\Documento";
let salto = "Primera línea\nSegunda línea";
let tab = "Columna1\tColumna2";
```

### Booleanos (Boolean)
```javascript
let verdadero = true;
let falso = false;

// Resultado de comparaciones
let mayor = 5 > 3;      // true
let igual = 10 == 10;   // true
let diferente = 1 != 2; // true
```

### Null y Undefined
```javascript
// Null (valor explícitamente vacío)
let vacio = null;

// Undefined (pendiente de implementación completa)
let indefinido;  // undefined implícito
```

## ⚙️ Operadores

### Operadores Aritméticos
```javascript
let a = 10;
let b = 3;

// Básicos
let suma = a + b;           // 13
let resta = a - b;          // 7
let multiplicacion = a * b; // 30
let division = a / b;       // 3.333...

// Con paréntesis
let complejo = (a + b) * 2; // 26
let anidado = ((a + b) * 2) / 4; // 6.5
```

### Operadores de Comparación
```javascript
let x = 5;
let y = 10;

// Relacionales
let mayor = x > y;        // false
let mayor_igual = x >= y; // false
let menor = x < y;        // true
let menor_igual = x <= y; // true

// Igualdad
let igual = x == y;       // false
let diferente = x != y;   // true
```

### Operadores Lógicos
```javascript
let a = true;
let b = false;

// AND lógico
let and = a && b;         // false

// OR lógico  
let or = a || b;          // true

// NOT lógico
let not_a = !a;           // false
let not_b = !b;           // true
```

### Operadores con Cadenas
```javascript
// Concatenación
let nombre = "Juan";
let apellido = "Pérez";
let completo = nombre + " " + apellido; // "Juan Pérez"

// Con números
let texto = "El número es: " + 42; // "El número es: 42"
```

### Precedencia de Operadores
```
1. Paréntesis             ( )
2. Negación lógica        !
3. Multiplicación/División  * /
4. Suma/Resta             + -
5. Comparación            < <= > >=
6. Igualdad              == !=
7. AND lógico            &&
8. OR lógico             ||
```

**Ejemplos:**
```javascript
let resultado1 = 2 + 3 * 4;        // 14 (no 20)
let resultado2 = (2 + 3) * 4;      // 20
let resultado3 = 10 > 5 && 3 < 7;  // true
let resultado4 = !false || true;   // true
```

## 🔨 Funciones

### Definición de Funciones
```javascript
// Función sin parámetros
function saludar() {
    return "¡Hola!";
}

// Función con parámetros
function sumar(a, b) {
    return a + b;
}

// Función con múltiples parámetros
function presentar(nombre, edad, ciudad) {
    return "Soy " + nombre + ", tengo " + edad + " años y vivo en " + ciudad;
}
```

### Llamada de Funciones
```javascript
// Sin parámetros
let mensaje = saludar();         // "¡Hola!"

// Con parámetros
let total = sumar(5, 3);         // 8
let info = presentar("Ana", 25, "Madrid"); // "Soy Ana, tengo 25 años..."

// Funciones anidadas
let complejo = sumar(sumar(1, 2), 3); // 6
```

### Funciones con Lógica
```javascript
function maximo(a, b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

function factorial(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);  // Recursión
    }
}
```

### Parámetros y Argumentos
```javascript
// Definición: parámetros formales
function multiplicar(numero1, numero2, factor) {
    return (numero1 + numero2) * factor;
}

// Llamada: argumentos reales
let resultado = multiplicar(10, 5, 2);  // 30
```

## 🔀 Estructuras de Control

### Condicionales If-Else
```javascript
// If simple
let edad = 18;
if (edad >= 18) {
    return "Mayor de edad";
}

// If-Else
if (edad >= 18) {
    return "Mayor de edad";
} else {
    return "Menor de edad";
}

// If-Else anidado
let nota = 85;
if (nota >= 90) {
    return "Excelente";
} else {
    if (nota >= 80) {
        return "Muy bien";
    } else {
        if (nota >= 70) {
            return "Bien";
        } else {
            return "Necesita mejorar";
        }
    }
}
```

### Bloques de Código
```javascript
// Bloque con múltiples declaraciones
if (true) {
    let temporal = 10;
    let doble = temporal * 2;
    return doble;
}
```

## 📝 Expresiones

### Expresiones Primarias
```javascript
// Literales
42              // Número
"texto"         // Cadena
true            // Booleano
false           // Booleano

// Identificadores
mi_variable     // Variable
mi_funcion      // Función
```

### Expresiones con Paréntesis
```javascript
let resultado = (5 + 3) * 2;        // 16
let logico = (true && false) || true; // true
```

### Expresiones de Llamada
```javascript
// Llamadas a función
funcion()                    // Sin argumentos
sumar(1, 2)                 // Con argumentos
calcular(obtener_x(), 5)    // Funciones anidadas
```

### Expresiones Complejas
```javascript
// Combinando operadores
let compleja = (a + b) * c / d - e;

// Con funciones
let mixta = sumar(multiplicar(2, 3), dividir(10, 5));

// Con condicionales
let condicional = x > 0 ? x : -x;  // Pendiente de implementación
```

## 💬 Comentarios

### Comentarios de Línea
```javascript
// Este es un comentario de una línea
let x = 5;  // Comentario al final de línea

// Los comentarios pueden contener cualquier texto
// TODO: Implementar más funcionalidades
// BUG: Revisar este cálculo
```

### Comentarios Múltiples
```javascript
/*
   Este es un comentario
   de múltiples líneas
   (Pendiente de implementación)
*/
```

## 🔑 Palabras Reservadas

Estas palabras no pueden usarse como identificadores:

```javascript
// Declaraciones
let         // Declaración de variable
function    // Definición de función
return      // Retorno de valor

// Control de flujo
if          // Condicional
else        // Alternativa condicional

// Valores literales
true        // Booleano verdadero
false       // Booleano falso
null        // Valor nulo

// Futuros (reservadas para extensiones)
const       // Constantes
var         // Variables (alternativa)
while       // Bucle mientras
for         // Bucle para
break       // Interrupción
continue    // Continuación
switch      // Selector múltiple
case        // Caso de selector
default     // Caso por defecto
```

## 📐 BNF y Gramática

### Gramática Formal del Lenguaje

```bnf
// Programa principal
program ::= statement*

// Declaraciones
statement ::= letStatement
           | returnStatement  
           | expressionStatement
           | blockStatement
           | ifStatement
           | functionStatement

// Declaración de variable
letStatement ::= "let" identifier "=" expression ";"

// Declaración de retorno
returnStatement ::= "return" expression? ";"

// Declaración de expresión
expressionStatement ::= expression ";"

// Bloque de código
blockStatement ::= "{" statement* "}"

// Condicional
ifStatement ::= "if" "(" expression ")" statement ("else" statement)?

// Función
functionStatement ::= "function" identifier "(" parameterList? ")" blockStatement
parameterList ::= identifier ("," identifier)*

// Expresiones
expression ::= logicalOrExpression

logicalOrExpression ::= logicalAndExpression ("||" logicalAndExpression)*
logicalAndExpression ::= equalityExpression ("&&" equalityExpression)*
equalityExpression ::= relationalExpression (("==" | "!=") relationalExpression)*
relationalExpression ::= additiveExpression (("<" | "<=" | ">" | ">=") additiveExpression)*
additiveExpression ::= multiplicativeExpression (("+" | "-") multiplicativeExpression)*
multiplicativeExpression ::= unaryExpression (("*" | "/") unaryExpression)*
unaryExpression ::= ("!" | "-")? primaryExpression
primaryExpression ::= identifier
                   | numberLiteral
                   | stringLiteral
                   | booleanLiteral
                   | nullLiteral
                   | "(" expression ")"
                   | functionCall

// Llamada de función
functionCall ::= identifier "(" argumentList? ")"
argumentList ::= expression ("," expression)*

// Tokens básicos
identifier ::= letter (letter | digit | "_")*
numberLiteral ::= digit+ ("." digit+)?
stringLiteral ::= "\"" character* "\"" | "'" character* "'"
booleanLiteral ::= "true" | "false"
nullLiteral ::= "null"

// Caracteres básicos
letter ::= "a".."z" | "A".."Z"
digit ::= "0".."9"
character ::= cualquier carácter excepto comillas
```

### Ejemplos de Análisis Sintáctico

**Expresión simple:**
```
"let x = 5 + 3;"

program
└── letStatement
    ├── identifier: "x"
    └── additiveExpression
        ├── numberLiteral: "5"
        ├── operator: "+"
        └── numberLiteral: "3"
```

**Función con condicional:**
```
"function max(a, b) { if (a > b) { return a; } else { return b; } }"

program
└── functionStatement
    ├── identifier: "max"
    ├── parameterList
    │   ├── identifier: "a"
    │   └── identifier: "b"
    └── blockStatement
        └── ifStatement
            ├── condition: relationalExpression (a > b)
            ├── thenStatement: blockStatement (return a;)
            └── elseStatement: blockStatement (return b;)
```

## 🚀 Ejemplos Avanzados

### Función Recursiva
```javascript
function fibonacci(n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

let resultado = fibonacci(10); // 55
```

### Función con Múltiples Condiciones
```javascript
function clasificar_edad(edad) {
    if (edad < 0) {
        return "Edad inválida";
    } else {
        if (edad < 13) {
            return "Niño";
        } else {
            if (edad < 20) {
                return "Adolescente";
            } else {
                if (edad < 60) {
                    return "Adulto";
                } else {
                    return "Adulto mayor";
                }
            }
        }
    }
}
```

### Cálculos Complejos
```javascript
function calcular_promedio(a, b, c, d, e) {
    let suma = a + b + c + d + e;
    let cantidad = 5;
    return suma / cantidad;
}

function es_numero_perfecto(numero) {
    let suma_divisores = 0;
    let i = 1;
    
    // Esta lógica requeriría bucles (pendiente de implementación)
    // Por ahora, ejemplo conceptual
    return suma_divisores == numero;
}
```

---

## 📚 Referencias Relacionadas

- [Guía de Inicio Rápido](quickstart.md) - Primeros pasos con LPP
- [Ejemplos de Código](examples.md) - Programas de ejemplo completos
- [Arquitectura](architecture.md) - Cómo funciona internamente el intérprete
- [API Reference](api-reference.md) - Referencia técnica para desarrolladores
- [Troubleshooting](troubleshooting.md) - Solución de problemas comunes

Esta documentación de sintaxis cubre las características actualmente implementadas en LPP. El lenguaje está en desarrollo activo y se añadirán más funcionalidades en futuras versiones.