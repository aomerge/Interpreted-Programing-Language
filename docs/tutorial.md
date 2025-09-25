# Tutorial Completo de LPP

Bienvenido al tutorial completo de LPP (Language Programming Project). Este tutorial te guiará paso a paso desde los conceptos básicos hasta características avanzadas del lenguaje.

## 📋 Tabla de Contenidos

- [¿Qué es LPP?](#qué-es-lpp)
- [Tu Primer Programa](#tu-primer-programa)
- [Variables y Tipos de Datos](#variables-y-tipos-de-datos)
- [Operadores](#operadores)
- [Funciones](#funciones)
- [Estructuras de Control](#estructuras-de-control)
- [Conceptos Avanzados](#conceptos-avanzados)
- [Mejores Prácticas](#mejores-prácticas)
- [Proyectos Prácticos](#proyectos-prácticos)

## 🚀 ¿Qué es LPP?

LPP es un lenguaje de programación interpretado diseñado para ser:
- **Fácil de aprender**: Sintaxis clara y familiar
- **Expresivo**: Permite escribir código elegante y legible
- **Modular**: Arquitectura bien organizada y extensible
- **Educativo**: Perfecto para aprender conceptos de programación

### Características Principales
- Tipado dinámico
- Sintaxis similar a JavaScript
- Soporte para funciones recursivas
- Sistema de variables con scope
- Manejo de errores integrado

## 👋 Tu Primer Programa

### Hola Mundo
El programa más simple en LPP:

```javascript
return "¡Hola, Mundo!";
```

**¿Cómo ejecutarlo?**
```bash
python -c "
from src.lexer.lexer import Lexer
from src.parser.parser_core import ModularParser
from src.interpreter.interpreter import Interpreter

code = 'return \"¡Hola, Mundo!\";'
lexer = Lexer(code)
parser = ModularParser(lexer)
program = parser.parse_program()
interpreter = Interpreter()
result = interpreter.interpret(program)
print(result.value)
"
```

### Tu Primera Variable
```javascript
let mensaje = "¡Hola desde LPP!";
return mensaje;
```

**Salida**: `¡Hola desde LPP!`

### Tu Primera Función
```javascript
function saludar(nombre) {
    return "Hola, " + nombre + "!";
}

return saludar("Programador");
```

**Salida**: `Hola, Programador!`

## 📊 Variables y Tipos de Datos

### Declaración de Variables

En LPP, todas las variables se declaran con `let`:

```javascript
let numero = 42;
let texto = "Hola mundo";
let activo = true;
let vacio = null;
```

**Reglas importantes:**
- Siempre usar `let` para declarar variables
- Los nombres de variables son sensibles a mayúsculas y minúsculas
- Deben empezar con letra o guión bajo
- Terminar declaraciones con `;`

### Tipos de Datos

#### 1. Números
```javascript
// Números enteros
let edad = 25;
let negativo = -10;
let cero = 0;

// Números decimales
let precio = 19.99;
let pi = 3.14159;
let pequeño = 0.001;

return precio; // 19.99
```

#### 2. Cadenas de Texto
```javascript
// Con comillas dobles
let saludo = "Hola mundo";

// Con comillas simples
let despedida = 'Adiós';

// Cadenas vacías
let vacia = "";

// Concatenación
let nombre = "Juan";
let apellido = "Pérez";
let completo = nombre + " " + apellido;

return completo; // "Juan Pérez"
```

#### 3. Booleanos
```javascript
let verdadero = true;
let falso = false;

// Resultado de comparaciones
let mayor = 10 > 5;  // true
let igual = 3 == 3;  // true

return mayor; // true
```

#### 4. Null
```javascript
let sin_valor = null;
let indefinido = null;  // LPP usa null para valores vacíos

return sin_valor; // null
```

### Ejercicios Prácticos

**Ejercicio 1**: Crea variables para almacenar información personal
```javascript
let mi_nombre = "Tu Nombre";
let mi_edad = 25;
let soy_estudiante = true;
let mi_promedio = 8.5;

return "Mi nombre es " + mi_nombre + " y tengo " + mi_edad + " años";
```

**Ejercicio 2**: Practica con diferentes tipos
```javascript
let entero = 100;
let decimal = 15.75;
let resultado = entero + decimal;  // 115.75

let texto1 = "El resultado es: ";
let mensaje = texto1 + resultado;

return mensaje;
```

## ⚙️ Operadores

### Operadores Aritméticos

```javascript
let a = 10;
let b = 3;

let suma = a + b;           // 13
let resta = a - b;          // 7
let multiplicacion = a * b; // 30
let division = a / b;       // 3.333...

return "Suma: " + suma + ", División: " + division;
```

**Precedencia de operadores:**
```javascript
let resultado1 = 2 + 3 * 4;      // 14 (no 20)
let resultado2 = (2 + 3) * 4;    // 20
let resultado3 = 10 / 2 + 3;     // 8
let resultado4 = 10 / (2 + 3);   // 2

return resultado1; // 14
```

### Operadores de Comparación

```javascript
let x = 5;
let y = 10;

let mayor = x > y;          // false
let menor = x < y;          // true
let mayor_igual = x >= y;   // false
let menor_igual = x <= y;   // true
let igual = x == y;         // false
let diferente = x != y;     // true

return menor; // true
```

### Operadores Lógicos

```javascript
let lluvia = true;
let frio = false;

let quedo_en_casa = lluvia || frio;      // true (OR)
let voy_al_parque = !lluvia && !frio;    // false (AND con negación)
let no_llueve = !lluvia;                 // false (NOT)

return quedo_en_casa; // true
```

### Trabajando con Strings

```javascript
let nombre = "Ana";
let apellido = "García";
let edad = 28;

// Concatenación
let presentacion = "Hola, soy " + nombre + " " + apellido;
let info_completa = presentacion + " y tengo " + edad + " años";

// Números y strings
let numero = 42;
let texto_con_numero = "El número es: " + numero; // "El número es: 42"

return info_completa;
```

### Ejercicios de Operadores

**Ejercicio 3**: Calculadora básica
```javascript
function calculadora(num1, num2, operacion) {
    if (operacion == "suma") {
        return num1 + num2;
    } else {
        if (operacion == "resta") {
            return num1 - num2;
        } else {
            if (operacion == "multiplicacion") {
                return num1 * num2;
            } else {
                if (operacion == "division") {
                    return num1 / num2;
                } else {
                    return "Operación no válida";
                }
            }
        }
    }
}

return calculadora(15, 3, "multiplicacion"); // 45
```

**Ejercicio 4**: Comparaciones
```javascript
let edad1 = 25;
let edad2 = 30;
let edad3 = 25;

let son_iguales = edad1 == edad3;        // true
let primera_mayor = edad1 > edad2;       // false
let todas_adultas = edad1 >= 18 && edad2 >= 18 && edad3 >= 18; // true

return "Son iguales: " + son_iguales + ", Todas adultas: " + todas_adultas;
```

## 🔨 Funciones

Las funciones son bloques de código reutilizable que realizan tareas específicas.

### Funciones Básicas

```javascript
// Función sin parámetros
function saludar() {
    return "¡Hola!";
}

// Función con parámetros
function saludar_persona(nombre) {
    return "¡Hola, " + nombre + "!";
}

// Función con múltiples parámetros
function sumar(a, b) {
    return a + b;
}

// Usando las funciones
let saludo_generico = saludar();              // "¡Hola!"
let saludo_personal = saludar_persona("Ana"); // "¡Hola, Ana!"
let resultado = sumar(5, 3);                  // 8

return resultado;
```

### Funciones con Lógica

```javascript
function determinar_mayor(a, b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

function calcular_descuento(precio, porcentaje) {
    let descuento = precio * porcentaje / 100;
    let precio_final = precio - descuento;
    return precio_final;
}

let mayor = determinar_mayor(15, 23);     // 23
let con_descuento = calcular_descuento(100, 20); // 80

return "Mayor: " + mayor + ", Con descuento: " + con_descuento;
```

### Funciones Recursivas

La recursión es cuando una función se llama a sí misma:

```javascript
// Factorial: 5! = 5 * 4 * 3 * 2 * 1 = 120
function factorial(n) {
    if (n <= 1) {
        return 1;  // Caso base
    } else {
        return n * factorial(n - 1);  // Llamada recursiva
    }
}

// Fibonacci: 0, 1, 1, 2, 3, 5, 8, 13...
function fibonacci(n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

let fact5 = factorial(5);    // 120
let fib7 = fibonacci(7);     // 13

return "Factorial(5): " + fact5 + ", Fibonacci(7): " + fib7;
```

### Scope y Variables

```javascript
let global_var = "Soy global";

function mostrar_scope() {
    let local_var = "Soy local";
    
    // Puede acceder a variables globales
    let mensaje = global_var + " - " + local_var;
    return mensaje;
}

// Esta función no puede acceder a local_var
function otra_funcion() {
    return global_var; // Solo acceso a variables globales
}

return mostrar_scope(); // "Soy global - Soy local"
```

### Ejercicios de Funciones

**Ejercicio 5**: Calculadora de área
```javascript
function area_rectangulo(ancho, alto) {
    return ancho * alto;
}

function area_triangulo(base, altura) {
    return (base * altura) / 2;
}

function area_circulo(radio) {
    let pi = 3.14159;
    return pi * radio * radio;
}

let rect = area_rectangulo(5, 8);     // 40
let tri = area_triangulo(6, 4);       // 12
let circ = area_circulo(3);           // 28.27...

return "Rectángulo: " + rect + ", Triángulo: " + tri;
```

**Ejercicio 6**: Validaciones
```javascript
function es_par(numero) {
    let resto = numero / 2;
    let entero = resto * 2;
    return numero == entero;
}

function es_positivo(numero) {
    return numero > 0;
}

function validar_numero(num) {
    let par = es_par(num);
    let positivo = es_positivo(num);
    
    if (positivo && par) {
        return "Número positivo y par";
    } else {
        if (positivo) {
            return "Número positivo pero impar";
        } else {
            return "Número negativo";
        }
    }
}

return validar_numero(8); // "Número positivo y par"
```

## 🔀 Estructuras de Control

### Condicionales If-Else

```javascript
let temperatura = 25;

if (temperatura > 30) {
    return "Hace calor";
} else {
    if (temperatura > 20) {
        return "Temperatura agradable";
    } else {
        if (temperatura > 10) {
            return "Hace fresco";
        } else {
            return "Hace frío";
        }
    }
}
```

### Condicionales Complejas

```javascript
function evaluar_estudiante(nota, asistencia) {
    let nota_aprobada = nota >= 60;
    let asistencia_ok = asistencia >= 75;
    
    if (nota_aprobada && asistencia_ok) {
        if (nota >= 90) {
            return "Excelente - Aprobado";
        } else {
            if (nota >= 80) {
                return "Muy bien - Aprobado";
            } else {
                return "Bien - Aprobado";
            }
        }
    } else {
        if (nota_aprobada) {
            return "Buena nota pero falta asistencia - Reprobado";
        } else {
            if (asistencia_ok) {
                return "Buena asistencia pero nota baja - Reprobado";
            } else {
                return "Nota y asistencia insuficientes - Reprobado";
            }
        }
    }
}

return evaluar_estudiante(85, 80); // "Muy bien - Aprobado"
```

### Bloques de Código

```javascript
function procesar_pedido(cantidad, precio_unitario) {
    if (cantidad > 0) {
        let subtotal = cantidad * precio_unitario;
        let descuento = 0;
        
        // Bloque para calcular descuento
        if (cantidad >= 10) {
            descuento = subtotal * 0.15; // 15% descuento
        } else {
            if (cantidad >= 5) {
                descuento = subtotal * 0.10; // 10% descuento
            }
        }
        
        let total = subtotal - descuento;
        return "Total: $" + total + " (Descuento: $" + descuento + ")";
    } else {
        return "Cantidad inválida";
    }
}

return procesar_pedido(12, 25); // "Total: $255 (Descuento: $45)"
```

### Ejercicios de Control de Flujo

**Ejercicio 7**: Sistema de calificaciones
```javascript
function sistema_notas(puntos) {
    if (puntos >= 95) {
        return "A+ (Sobresaliente)";
    } else {
        if (puntos >= 90) {
            return "A (Excelente)";
        } else {
            if (puntos >= 85) {
                return "B+ (Muy bueno)";
            } else {
                if (puntos >= 80) {
                    return "B (Bueno)";
                } else {
                    if (puntos >= 75) {
                        return "C+ (Satisfactorio)";
                    } else {
                        if (puntos >= 70) {
                            return "C (Suficiente)";
                        } else {
                            return "F (Reprobado)";
                        }
                    }
                }
            }
        }
    }
}

return sistema_notas(87); // "B+ (Muy bueno)"
```

**Ejercicio 8**: Calculadora de impuestos
```javascript
function calcular_impuestos(salario_anual) {
    let impuestos = 0;
    
    if (salario_anual <= 20000) {
        impuestos = 0; // Exento
    } else {
        if (salario_anual <= 50000) {
            impuestos = (salario_anual - 20000) * 0.15; // 15%
        } else {
            if (salario_anual <= 100000) {
                let primera_parte = 30000 * 0.15;         // 15% hasta 50k
                let segunda_parte = (salario_anual - 50000) * 0.25; // 25% resto
                impuestos = primera_parte + segunda_parte;
            } else {
                let primera = 30000 * 0.15;               // 15% hasta 50k
                let segunda = 50000 * 0.25;               // 25% hasta 100k
                let tercera = (salario_anual - 100000) * 0.35;     // 35% resto
                impuestos = primera + segunda + tercera;
            }
        }
    }
    
    let salario_neto = salario_anual - impuestos;
    return "Salario: $" + salario_anual + ", Impuestos: $" + impuestos + ", Neto: $" + salario_neto;
}

return calcular_impuestos(60000);
```

## 🎯 Conceptos Avanzados

### Funciones como Valores

En LPP, las funciones son ciudadanos de primera clase:

```javascript
function operacion_matematica(a, b, tipo_operacion) {
    if (tipo_operacion == "suma") {
        return a + b;
    } else {
        if (tipo_operacion == "resta") {
            return a - b;
        } else {
            if (tipo_operacion == "multiplicacion") {
                return a * b;
            } else {
                if (tipo_operacion == "division") {
                    return a / b;
                } else {
                    return 0;
                }
            }
        }
    }
}

function calcular_multiple(x, y) {
    let suma = operacion_matematica(x, y, "suma");
    let producto = operacion_matematica(x, y, "multiplicacion");
    return "Suma: " + suma + ", Producto: " + producto;
}

return calcular_multiple(6, 4); // "Suma: 10, Producto: 24"
```

### Closures y Scope Anidado

```javascript
function crear_contador(inicial) {
    let contador = inicial;
    
    function incrementar() {
        contador = contador + 1;
        return contador;
    }
    
    function obtener_valor() {
        return contador;
    }
    
    // En LPP actual, retornamos el valor directamente
    // En futuras versiones podríamos retornar las funciones
    return contador;
}

function contador_avanzado() {
    let privado = 0;
    
    function sumar_uno() {
        privado = privado + 1;
        return privado;
    }
    
    function sumar_n(n) {
        privado = privado + n;
        return privado;
    }
    
    // Simulamos comportamiento de closure
    let valor1 = sumar_uno();    // 1
    let valor2 = sumar_n(5);     // 6
    let valor3 = sumar_uno();    // 7
    
    return valor3;
}

return contador_avanzado(); // 7
```

### Recursión Avanzada

```javascript
// Torres de Hanoi (algoritmo recursivo clásico)
function torres_hanoi(n, origen, destino, auxiliar) {
    if (n == 1) {
        return "Mover disco 1 de " + origen + " a " + destino;
    } else {
        // Esta sería la implementación completa con múltiples movimientos
        // Por simplicidad, retornamos el número de movimientos necesarios
        let movimientos = torres_hanoi(n - 1, origen, auxiliar, destino);
        // mover disco n de origen a destino
        let mas_movimientos = torres_hanoi(n - 1, auxiliar, destino, origen);
        return (2 * (n - 1)) + 1; // Fórmula: 2^n - 1
    }
}

// Búsqueda binaria recursiva (concepto)
function busqueda_binaria(lista_size, objetivo, inicio, fin) {
    if (inicio > fin) {
        return -1; // No encontrado
    } else {
        let medio = (inicio + fin) / 2;
        let valor_medio = medio; // Simulamos acceso al valor
        
        if (valor_medio == objetivo) {
            return medio; // Encontrado
        } else {
            if (objetivo < valor_medio) {
                return busqueda_binaria(lista_size, objetivo, inicio, medio - 1);
            } else {
                return busqueda_binaria(lista_size, objetivo, medio + 1, fin);
            }
        }
    }
}

let movimientos = torres_hanoi(3, "A", "C", "B"); // 7 movimientos
return "Torres de Hanoi (3 discos): " + movimientos + " movimientos";
```

## 💡 Mejores Prácticas

### 1. Nomenclatura Clara

```javascript
// ✅ Bueno: nombres descriptivos
function calcular_precio_con_descuento(precio_original, porcentaje_descuento) {
    let descuento = precio_original * porcentaje_descuento / 100;
    return precio_original - descuento;
}

// ❌ Malo: nombres no descriptivos
function calc(p, d) {
    let x = p * d / 100;
    return p - x;
}
```

### 2. Funciones Pequeñas y Enfocadas

```javascript
// ✅ Bueno: funciones con responsabilidad única
function validar_email(email) {
    // Lógica de validación específica
    return email != null && email != "";
}

function enviar_email(destinatario, asunto, mensaje) {
    if (validar_email(destinatario)) {
        return "Email enviado a: " + destinatario;
    } else {
        return "Email inválido";
    }
}

// ✅ Bueno: función para un cálculo específico
function calcular_iva(precio) {
    let iva_porcentaje = 21;
    return precio * iva_porcentaje / 100;
}

function calcular_precio_final(precio_base) {
    let iva = calcular_iva(precio_base);
    return precio_base + iva;
}
```

### 3. Manejo de Errores

```javascript
function dividir_seguro(dividendo, divisor) {
    if (divisor == 0) {
        return "Error: No se puede dividir por cero";
    } else {
        if (divisor == null) {
            return "Error: El divisor no puede ser nulo";
        } else {
            return dividendo / divisor;
        }
    }
}

function obtener_raiz_cuadrada_aproximada(numero) {
    if (numero < 0) {
        return "Error: No se puede calcular raíz de número negativo";
    } else {
        if (numero == 0) {
            return 0;
        } else {
            // Aproximación simple (método babilónico)
            let aproximacion = numero / 2;
            let iteraciones = 5;
            
            function mejorar_aproximacion(actual, original, restantes) {
                if (restantes == 0) {
                    return actual;
                } else {
                    let nueva = (actual + original / actual) / 2;
                    return mejorar_aproximacion(nueva, original, restantes - 1);
                }
            }
            
            return mejorar_aproximacion(aproximacion, numero, iteraciones);
        }
    }
}

let resultado1 = dividir_seguro(10, 2);    // 5
let resultado2 = dividir_seguro(10, 0);    // "Error: No se puede dividir por cero"
let raiz = obtener_raiz_cuadrada_aproximada(16); // ~4

return "División: " + resultado1 + ", Raíz de 16: " + raiz;
```

### 4. Comentarios Útiles

```javascript
// Función para calcular el interés compuesto
// P = principal, r = tasa anual, t = tiempo en años, n = veces que se compone por año
function interes_compuesto(principal, tasa_anual, tiempo_años, frecuencia) {
    // Convertir tasa porcentual a decimal
    let tasa_decimal = tasa_anual / 100;
    
    // Fórmula: A = P(1 + r/n)^(nt)
    // Donde A = monto final, P = principal, r = tasa, n = frecuencia, t = tiempo
    
    let factor_interes = 1 + (tasa_decimal / frecuencia);
    let exponente = frecuencia * tiempo_años;
    
    // Simulamos potenciación con función recursiva
    function potencia(base, exp) {
        if (exp == 0) {
            return 1;
        } else {
            if (exp == 1) {
                return base;
            } else {
                return base * potencia(base, exp - 1);
            }
        }
    }
    
    let monto_final = principal * potencia(factor_interes, exponente);
    let interes_ganado = monto_final - principal;
    
    return "Capital inicial: $" + principal + 
           ", Monto final: $" + monto_final + 
           ", Interés ganado: $" + interes_ganado;
}

// Ejemplo: $1000 al 5% anual durante 2 años, compuesto anualmente
return interes_compuesto(1000, 5, 2, 1);
```

## 🏗️ Proyectos Prácticos

### Proyecto 1: Sistema de Gestión de Estudiantes

```javascript
// Función para calcular promedio de 4 notas
function calcular_promedio(nota1, nota2, nota3, nota4) {
    let suma = nota1 + nota2 + nota3 + nota4;
    return suma / 4;
}

// Función para determinar la letra de calificación
function obtener_letra(promedio) {
    if (promedio >= 90) {
        return "A";
    } else {
        if (promedio >= 80) {
            return "B";
        } else {
            if (promedio >= 70) {
                return "C";
            } else {
                if (promedio >= 60) {
                    return "D";
                } else {
                    return "F";
                }
            }
        }
    }
}

// Función para determinar si está aprobado
function esta_aprobado(promedio) {
    return promedio >= 60;
}

// Función para generar reporte completo
function reporte_estudiante(nombre, n1, n2, n3, n4) {
    let promedio = calcular_promedio(n1, n2, n3, n4);
    let letra = obtener_letra(promedio);
    let aprobado = esta_aprobado(promedio);
    let estado = "";
    
    if (aprobado) {
        estado = "APROBADO";
    } else {
        estado = "REPROBADO";
    }
    
    return "=== REPORTE ESTUDIANTIL ===" +
           "\nEstudiante: " + nombre +
           "\nNotas: " + n1 + ", " + n2 + ", " + n3 + ", " + n4 +
           "\nPromedio: " + promedio +
           "\nCalificación: " + letra +
           "\nEstado: " + estado;
}

// Función para comparar dos estudiantes
function comparar_estudiantes(nombre1, notas1_1, notas1_2, notas1_3, notas1_4,
                             nombre2, notas2_1, notas2_2, notas2_3, notas2_4) {
    let prom1 = calcular_promedio(notas1_1, notas1_2, notas1_3, notas1_4);
    let prom2 = calcular_promedio(notas2_1, notas2_2, notas2_3, notas2_4);
    
    if (prom1 > prom2) {
        return nombre1 + " tiene mejor promedio: " + prom1 + " vs " + prom2;
    } else {
        if (prom2 > prom1) {
            return nombre2 + " tiene mejor promedio: " + prom2 + " vs " + prom1;
        } else {
            return nombre1 + " y " + nombre2 + " tienen el mismo promedio: " + prom1;
        }
    }
}

// Ejemplo de uso
return reporte_estudiante("María González", 85, 92, 78, 88);
```

### Proyecto 2: Calculadora Financiera

```javascript
// Sistema completo de cálculos financieros

function calcular_interes_simple(principal, tasa, tiempo) {
    let interes = principal * tasa * tiempo / 100;
    let total = principal + interes;
    return "Capital: $" + principal + ", Interés: $" + interes + ", Total: $" + total;
}

function calcular_pago_prestamo(monto, tasa_mensual, meses) {
    // Fórmula de pago mensual: P = L[c(1 + c)^n]/[(1 + c)^n - 1]
    let tasa_decimal = tasa_mensual / 100;
    
    // Simulamos (1 + tasa)^meses con función recursiva
    function potencia_interes(base, exponente) {
        if (exponente == 0) {
            return 1;
        } else {
            if (exponente == 1) {
                return base;
            } else {
                return base * potencia_interes(base, exponente - 1);
            }
        }
    }
    
    let factor = potencia_interes(1 + tasa_decimal, meses);
    let numerador = monto * tasa_decimal * factor;
    let denominador = factor - 1;
    
    let pago_mensual = numerador / denominador;
    let total_pagado = pago_mensual * meses;
    let interes_total = total_pagado - monto;
    
    return "Préstamo: $" + monto + 
           ", Pago mensual: $" + pago_mensual + 
           ", Total a pagar: $" + total_pagado + 
           ", Interés total: $" + interes_total;
}

function calcular_ahorro_mensual(objetivo, tasa_anual, años) {
    let meses = años * 12;
    let tasa_mensual = tasa_anual / 12 / 100;
    
    // Fórmula de anualidad: PMT = FV * r / [(1 + r)^n - 1]
    function potencia_ahorro(base, exp) {
        if (exp == 0) return 1;
        if (exp == 1) return base;
        return base * potencia_ahorro(base, exp - 1);
    }
    
    let factor = potencia_ahorro(1 + tasa_mensual, meses);
    let ahorro_mensual = objetivo * tasa_mensual / (factor - 1);
    let total_ahorrado = ahorro_mensual * meses;
    let interes_ganado = objetivo - total_ahorrado;
    
    return "Para ahorrar $" + objetivo + " en " + años + " años:" +
           "\nAhorro mensual necesario: $" + ahorro_mensual +
           "\nTotal aportado: $" + total_ahorrado +
           "\nInterés ganado: $" + interes_ganado;
}

function planificador_financiero(edad_actual, edad_retiro, salario_actual, meta_ahorro) {
    let años_para_retiro = edad_retiro - edad_actual;
    let ahorro_anual_necesario = meta_ahorro / años_para_retiro;
    let porcentaje_salario = ahorro_anual_necesario / salario_actual * 100;
    
    return "Planificación para el retiro:" +
           "\nEdad actual: " + edad_actual + ", Edad de retiro: " + edad_retiro +
           "\nAños disponibles: " + años_para_retiro +
           "\nMeta de ahorro: $" + meta_ahorro +
           "\nAhorro anual necesario: $" + ahorro_anual_necesario +
           "\nPorcentaje del salario: " + porcentaje_salario + "%";
}

// Ejemplo de uso del sistema
return calcular_pago_prestamo(100000, 1.5, 240); // Casa de $100k a 20 años
```

### Proyecto 3: Juego de Adivinanzas (Simulado)

```javascript
// Sistema de juego de adivinanza de números

function generar_numero_aleatorio_simulado(semilla) {
    // Simulamos aleatoriedad usando una fórmula simple
    let numero = (semilla * 7 + 13) % 100 + 1;
    return numero;
}

function evaluar_adivinanza(numero_secreto, adivinanza) {
    if (adivinanza == numero_secreto) {
        return "¡Correcto! Has adivinado el número " + numero_secreto;
    } else {
        if (adivinanza < numero_secreto) {
            let diferencia = numero_secreto - adivinanza;
            if (diferencia <= 5) {
                return "Muy cerca, pero más alto";
            } else {
                if (diferencia <= 10) {
                    return "Cerca, pero más alto";
                } else {
                    return "Más alto";
                }
            }
        } else {
            let diferencia = adivinanza - numero_secreto;
            if (diferencia <= 5) {
                return "Muy cerca, pero más bajo";
            } else {
                if (diferencia <= 10) {
                    return "Cerca, pero más bajo";
                } else {
                    return "Más bajo";
                }
            }
        }
    }
}

function calcular_puntuacion(intentos, tiempo_segundos) {
    let puntuacion_base = 1000;
    let penalizacion_intentos = (intentos - 1) * 100;
    let penalizacion_tiempo = tiempo_segundos * 2;
    
    let puntuacion_final = puntuacion_base - penalizacion_intentos - penalizacion_tiempo;
    
    if (puntuacion_final < 0) {
        puntuacion_final = 0;
    }
    
    return puntuacion_final;
}

function simular_juego_completo(semilla_numero, lista_adivinanzas) {
    let numero_secreto = generar_numero_aleatorio_simulado(semilla_numero);
    let intentos = 0;
    let adivinanza_actual = 0;
    
    // Simulamos múltiples intentos
    function procesar_intento(intento_num) {
        if (intento_num == 1) {
            adivinanza_actual = 50; // Primera adivinanza: mitad del rango
        } else {
            if (intento_num == 2) {
                adivinanza_actual = 25; // Ajuste basado en respuesta anterior
            } else {
                adivinanza_actual = 75; // Siguiente ajuste
            }
        }
        
        let evaluacion = evaluar_adivinanza(numero_secreto, adivinanza_actual);
        
        return "Intento " + intento_num + ": Adivinanza = " + adivinanza_actual + 
               ", Resultado: " + evaluacion;
    }
    
    let resultado1 = procesar_intento(1);
    let resultado2 = procesar_intento(2);
    let resultado3 = procesar_intento(3);
    
    let puntuacion = calcular_puntuacion(3, 45); // 3 intentos, 45 segundos
    
    return "=== JUEGO DE ADIVINANZAS ===" +
           "\nNúmero secreto: " + numero_secreto +
           "\n" + resultado1 +
           "\n" + resultado2 + 
           "\n" + resultado3 +
           "\nPuntuación final: " + puntuacion;
}

// Ejecutar simulación del juego
return simular_juego_completo(42);
```

## 🎓 Conclusión y Próximos Pasos

¡Felicidades! Has completado el tutorial completo de LPP. Ahora tienes las herramientas necesarias para:

### Lo que has aprendido:
✅ Sintaxis básica del lenguaje LPP  
✅ Manejo de variables y tipos de datos  
✅ Operadores aritméticos, lógicos y de comparación  
✅ Creación y uso de funciones  
✅ Estructuras de control (if-else, bloques)  
✅ Recursión y conceptos avanzados  
✅ Mejores prácticas de programación  
✅ Desarrollo de proyectos completos  

### Para continuar tu aprendizaje:

1. **Practica regularmente**: Crea tus propios programas y experimenta
2. **Lee código de otros**: Revisa los [ejemplos](examples.md) adicionales
3. **Entiende la arquitectura**: Estudia cómo funciona el intérprete en [architecture.md](architecture.md)
4. **Contribuye al proyecto**: Revisa la [guía de contribución](contributing.md)
5. **Explora extensiones**: LPP está en desarrollo continuo

### Recursos adicionales:
- [Sintaxis completa](language-syntax.md) - Referencia detallada
- [API Reference](api-reference.md) - Para desarrolladores avanzados
- [Troubleshooting](troubleshooting.md) - Solución de problemas
- [FAQ](faq.md) - Preguntas frecuentes

### ¡Tu viaje de programación con LPP apenas comienza!

¿Tienes ideas para nuevos proyectos? ¿Quieres contribuir al desarrollo del lenguaje? ¡La comunidad LPP te da la bienvenida!

---

**¡Feliz programación!** 🚀