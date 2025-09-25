# Ejemplos de Código LPP

Esta sección contiene ejemplos prácticos y detallados del lenguaje LPP, organizados por categorías y nivel de complejidad.

## 📋 Tabla de Contenidos

- [Ejemplos Básicos](#ejemplos-básicos)
- [Trabajo con Números](#trabajo-con-números)
- [Manipulación de Cadenas](#manipulación-de-cadenas)
- [Funciones Útiles](#funciones-útiles)
- [Lógica y Decisiones](#lógica-y-decisiones)
- [Programas Completos](#programas-completos)
- [Casos de Prueba](#casos-de-prueba)
- [Patrones Comunes](#patrones-comunes)

## 🌟 Ejemplos Básicos

### Hello World Variations
```javascript
// Versión básica
return "¡Hola, Mundo!";
```

```javascript
// Con variable
let saludo = "¡Hola, Mundo!";
return saludo;
```

```javascript
// Con función
function saludar() {
    return "¡Hola, Mundo!";
}

return saludar();
```

```javascript
// Saludo personalizado
function saludar_persona(nombre) {
    return "¡Hola, " + nombre + "!";
}

let mi_saludo = saludar_persona("María");
return mi_saludo;
```

### Variables y Asignaciones
```javascript
// Diferentes tipos de datos
let numero_entero = 42;
let numero_decimal = 3.14159;
let texto = "LPP es genial";
let verdadero = true;
let falso = false;
let vacio = null;

// Mostrar valores
return "Entero: " + numero_entero + ", Decimal: " + numero_decimal;
```

```javascript
// Reasignación de variables
let contador = 0;
contador = contador + 1;
contador = contador * 2;
contador = contador - 1;

return contador; // Resultado: 1
```

## 🔢 Trabajo con Números

### Operaciones Aritméticas Básicas
```javascript
function calculadora_basica(a, b) {
    let suma = a + b;
    let resta = a - b;
    let multiplicacion = a * b;
    let division = a / b;
    
    return "Suma: " + suma + ", Resta: " + resta + 
           ", Multiplicación: " + multiplicacion + 
           ", División: " + division;
}

return calculadora_basica(15, 3);
// "Suma: 18, Resta: 12, Multiplicación: 45, División: 5"
```

### Cálculos Matemáticos
```javascript
// Función para calcular área de círculo
function area_circulo(radio) {
    let pi = 3.14159;
    return pi * radio * radio;
}

// Función para calcular hipotenusa
function hipotenusa(cateto1, cateto2) {
    let cuadrado1 = cateto1 * cateto1;
    let cuadrado2 = cateto2 * cateto2;
    let suma_cuadrados = cuadrado1 + cuadrado2;
    // Aproximación de raíz cuadrada (método Babilónico simplificado)
    let aproximacion = suma_cuadrados / 2;
    return aproximacion;
}

let area = area_circulo(5);
let lado = hipotenusa(3, 4);

return "Área del círculo: " + area + ", Hipotenusa: " + lado;
```

### Números y Comparaciones
```javascript
function numero_mayor(a, b, c) {
    let mayor = a;
    
    if (b > mayor) {
        mayor = b;
    }
    
    if (c > mayor) {
        mayor = c;
    }
    
    return mayor;
}

function es_par(numero) {
    let division = numero / 2;
    let multiplicacion = division * 2;
    return multiplicacion == numero;
}

let mayor = numero_mayor(10, 25, 15);
let par = es_par(8);

return "Mayor: " + mayor + ", Es par: " + par;
```

## 🔤 Manipulación de Cadenas

### Construcción de Cadenas
```javascript
// Función para crear un saludo completo
function saludo_completo(nombre, apellido, titulo) {
    if (titulo != null) {
        return "Hola, " + titulo + " " + nombre + " " + apellido;
    } else {
        return "Hola, " + nombre + " " + apellido;
    }
}

// Función para repetir texto
function repetir_texto(texto, veces) {
    let resultado = "";
    let contador = 0;
    
    // Simulamos un bucle con recursión
    function repetir_recursivo(texto_base, restantes) {
        if (restantes <= 0) {
            return resultado;
        } else {
            resultado = resultado + texto_base;
            return repetir_recursivo(texto_base, restantes - 1);
        }
    }
    
    return repetir_recursivo(texto, veces);
}

let saludo1 = saludo_completo("Juan", "Pérez", "Dr.");
let saludo2 = saludo_completo("Ana", "García", null);
let repetido = repetir_texto("¡Hola! ", 3);

return saludo1 + " - " + saludo2;
```

### Análisis de Cadenas
```javascript
// Función para contar caracteres (simulación)
function contar_caracteres(texto) {
    // En un lenguaje completo tendríamos .length
    // Por ahora simulamos con lógica básica
    let contador = 0;
    // Esta sería la implementación real con bucles
    return "Texto: '" + texto + "' tiene aproximadamente " + 10 + " caracteres";
}

// Función para crear iniciales
function crear_iniciales(nombre, apellido) {
    // En un lenguaje completo usaríamos substring/charAt
    // Por ahora simulamos
    return "Iniciales simuladas: X.Y.";
}

let analisis = contar_caracteres("Hola mundo");
let iniciales = crear_iniciales("Juan", "Pérez");

return analisis + " - " + iniciales;
```

## ⚙️ Funciones Útiles

### Funciones Matemáticas Avanzadas
```javascript
// Función factorial (recursiva)
function factorial(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

// Función potencia (recursiva)
function potencia(base, exponente) {
    if (exponente == 0) {
        return 1;
    } else {
        if (exponente == 1) {
            return base;
        } else {
            return base * potencia(base, exponente - 1);
        }
    }
}

// Función para número de Fibonacci
function fibonacci(n) {
    if (n <= 1) {
        return n;
    } else {
        return fibonacci(n - 1) + fibonacci(n - 2);
    }
}

let fact5 = factorial(5);
let dos_elevado_8 = potencia(2, 8);
let fib10 = fibonacci(10);

return "Factorial(5): " + fact5 + ", 2^8: " + dos_elevado_8 + ", Fib(10): " + fib10;
```

### Funciones de Utilidad
```javascript
// Función para intercambiar valores
function intercambiar(a, b) {
    let temp = a;
    a = b;
    b = temp;
    return "Intercambio: a=" + a + ", b=" + b;
}

// Función para valor absoluto
function valor_absoluto(numero) {
    if (numero < 0) {
        return -numero;
    } else {
        return numero;
    }
}

// Función para encontrar mínimo
function minimo(a, b) {
    if (a < b) {
        return a;
    } else {
        return b;
    }
}

// Función para encontrar máximo
function maximo(a, b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}

let intercambio = intercambiar(10, 20);
let absoluto = valor_absoluto(-15);
let min = minimo(5, 8);
let max = maximo(12, 7);

return "Absoluto: " + absoluto + ", Min: " + min + ", Max: " + max;
```

## 🧠 Lógica y Decisiones

### Condicionales Complejas
```javascript
// Función para clasificar temperatura
function clasificar_temperatura(celsius) {
    if (celsius < 0) {
        return "Congelante";
    } else {
        if (celsius <= 10) {
            return "Frío";
        } else {
            if (celsius <= 20) {
                return "Templado";
            } else {
                if (celsius <= 30) {
                    return "Cálido";
                } else {
                    return "Caluroso";
                }
            }
        }
    }
}

// Función para calcular descuento
function calcular_descuento(precio, categoria_cliente) {
    let descuento = 0;
    
    if (categoria_cliente == "premium") {
        descuento = precio * 0.20; // 20%
    } else {
        if (categoria_cliente == "gold") {
            descuento = precio * 0.15; // 15%
        } else {
            if (categoria_cliente == "silver") {
                descuento = precio * 0.10; // 10%
            } else {
                descuento = 0; // Sin descuento
            }
        }
    }
    
    return precio - descuento;
}

let temp = clasificar_temperatura(25);
let precio_final = calcular_descuento(100, "gold");

return "Temperatura: " + temp + ", Precio con descuento: " + precio_final;
```

### Lógica Booleana
```javascript
// Función para validar rango
function en_rango(valor, minimo, maximo) {
    return valor >= minimo && valor <= maximo;
}

// Función para validar contraseña (simulada)
function validar_password(longitud, tiene_numeros, tiene_mayusculas) {
    let longitud_ok = longitud >= 8;
    let contenido_ok = tiene_numeros && tiene_mayusculas;
    return longitud_ok && contenido_ok;
}

// Función para determinar si es día laboral
function es_dia_laboral(dia) {
    let es_fin_semana = dia == "sabado" || dia == "domingo";
    return !es_fin_semana;
}

let en_rango_edad = en_rango(25, 18, 65);
let password_valida = validar_password(10, true, true);
let laboral = es_dia_laboral("lunes");

return "En rango: " + en_rango_edad + ", Password OK: " + password_valida + ", Laboral: " + laboral;
```

## 🏗️ Programas Completos

### Calculadora de IMC (Índice de Masa Corporal)
```javascript
function calcular_imc(peso, altura) {
    let altura_metros = altura / 100; // Convertir cm a metros
    let imc = peso / (altura_metros * altura_metros);
    return imc;
}

function clasificar_imc(imc) {
    if (imc < 18.5) {
        return "Bajo peso";
    } else {
        if (imc < 25) {
            return "Peso normal";
        } else {
            if (imc < 30) {
                return "Sobrepeso";
            } else {
                return "Obesidad";
            }
        }
    }
}

function reporte_imc(peso, altura_cm) {
    let imc = calcular_imc(peso, altura_cm);
    let clasificacion = clasificar_imc(imc);
    
    return "Peso: " + peso + "kg, Altura: " + altura_cm + "cm" +
           " -> IMC: " + imc + " (" + clasificacion + ")";
}

// Ejemplo de uso
return reporte_imc(70, 175);
```

### Sistema de Notas
```javascript
function calcular_promedio(nota1, nota2, nota3, nota4) {
    let suma = nota1 + nota2 + nota3 + nota4;
    return suma / 4;
}

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

function esta_aprobado(promedio) {
    return promedio >= 60;
}

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
    
    return "Estudiante: " + nombre + 
           " | Promedio: " + promedio + 
           " | Letra: " + letra + 
           " | Estado: " + estado;
}

// Ejemplo de uso
return reporte_estudiante("Juan Pérez", 85, 92, 78, 88);
```

### Conversor de Unidades
```javascript
function celsius_a_fahrenheit(celsius) {
    return (celsius * 9 / 5) + 32;
}

function fahrenheit_a_celsius(fahrenheit) {
    return (fahrenheit - 32) * 5 / 9;
}

function metros_a_pies(metros) {
    return metros * 3.28084;
}

function pies_a_metros(pies) {
    return pies / 3.28084;
}

function kilos_a_libras(kilos) {
    return kilos * 2.20462;
}

function libras_a_kilos(libras) {
    return libras / 2.20462;
}

function conversor_universal(valor, conversion) {
    if (conversion == "c_to_f") {
        return celsius_a_fahrenheit(valor);
    } else {
        if (conversion == "f_to_c") {
            return fahrenheit_a_celsius(valor);
        } else {
            if (conversion == "m_to_ft") {
                return metros_a_pies(valor);
            } else {
                if (conversion == "ft_to_m") {
                    return pies_a_metros(valor);
                } else {
                    return "Conversión no soportada";
                }
            }
        }
    }
}

// Ejemplos de uso
let temp_f = celsius_a_fahrenheit(25);
let distancia_pies = metros_a_pies(10);
let peso_libras = kilos_a_libras(70);

return "25°C = " + temp_f + "°F, 10m = " + distancia_pies + "ft, 70kg = " + peso_libras + "lb";
```

## 🧪 Casos de Prueba

### Testing de Funciones
```javascript
// Función a probar
function dividir(a, b) {
    if (b == 0) {
        return "Error: División por cero";
    } else {
        return a / b;
    }
}

// Casos de prueba
function test_dividir() {
    // Test 1: División normal
    let test1 = dividir(10, 2);
    let esperado1 = 5;
    let resultado1 = test1 == esperado1;
    
    // Test 2: División por cero
    let test2 = dividir(10, 0);
    let esperado2 = "Error: División por cero";
    let resultado2 = test2 == esperado2;
    
    // Test 3: División con decimales
    let test3 = dividir(7, 2);
    let esperado3 = 3.5;
    let resultado3 = test3 == esperado3;
    
    let todos_ok = resultado1 && resultado2 && resultado3;
    
    return "Test 1: " + resultado1 + 
           ", Test 2: " + resultado2 + 
           ", Test 3: " + resultado3 + 
           " -> Todos: " + todos_ok;
}

return test_dividir();
```

### Validaciones de Entrada
```javascript
function validar_edad(edad) {
    let es_numero = edad >= 0; // Simulación de validación numérica
    let rango_valido = edad >= 0 && edad <= 150;
    
    if (!es_numero) {
        return "Error: Debe ser un número";
    } else {
        if (!rango_valido) {
            return "Error: Edad debe estar entre 0 y 150";
        } else {
            return "Edad válida";
        }
    }
}

function validar_email_simple(email) {
    // Simulación básica (en un lenguaje completo usaríamos expresiones regulares)
    let tiene_arroba = email == "usuario@ejemplo.com"; // Simulación
    
    if (tiene_arroba) {
        return "Email válido";
    } else {
        return "Email inválido";
    }
}

// Pruebas de validación
let edad_ok = validar_edad(25);
let edad_error = validar_edad(-5);
let email_ok = validar_email_simple("usuario@ejemplo.com");

return "Edad 25: " + edad_ok + ", Edad -5: " + edad_error + ", Email: " + email_ok;
```

## 🔄 Patrones Comunes

### Patrón de Acumulador
```javascript
// Suma de números del 1 al n (con recursión)
function suma_consecutivos(n) {
    if (n <= 0) {
        return 0;
    } else {
        return n + suma_consecutivos(n - 1);
    }
}

// Producto de números del 1 al n (factorial)
function producto_consecutivos(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * producto_consecutivos(n - 1);
    }
}

let suma = suma_consecutivos(5);  // 1+2+3+4+5 = 15
let producto = producto_consecutivos(5);  // 1*2*3*4*5 = 120

return "Suma 1-5: " + suma + ", Producto 1-5: " + producto;
```

### Patrón de Decisión en Cadena
```javascript
function procesar_codigo_error(codigo) {
    if (codigo == 200) {
        return "OK: Operación exitosa";
    } else {
        if (codigo == 400) {
            return "Error: Solicitud incorrecta";
        } else {
            if (codigo == 404) {
                return "Error: No encontrado";
            } else {
                if (codigo == 500) {
                    return "Error: Error interno del servidor";
                } else {
                    return "Error: Código desconocido";
                }
            }
        }
    }
}

// Patrón de tabla de valores (simulado)
function obtener_dia_semana(numero) {
    if (numero == 1) {
        return "Lunes";
    } else {
        if (numero == 2) {
            return "Martes";
        } else {
            if (numero == 3) {
                return "Miércoles";
            } else {
                if (numero == 4) {
                    return "Jueves";
                } else {
                    if (numero == 5) {
                        return "Viernes";
                    } else {
                        if (numero == 6) {
                            return "Sábado";
                        } else {
                            if (numero == 7) {
                                return "Domingo";
                            } else {
                                return "Día inválido";
                            }
                        }
                    }
                }
            }
        }
    }
}

let error = procesar_codigo_error(404);
let dia = obtener_dia_semana(3);

return "Código 404: " + error + ", Día 3: " + dia;
```

### Patrón de Constructor/Factory
```javascript
// "Constructor" de persona
function crear_persona(nombre, edad, email) {
    let info_basica = "Nombre: " + nombre + ", Edad: " + edad;
    let info_contacto = "Email: " + email;
    return info_basica + ", " + info_contacto;
}

// "Constructor" de producto
function crear_producto(nombre, precio, categoria) {
    let precio_con_iva = precio * 1.21; // 21% IVA
    return "Producto: " + nombre + 
           ", Categoría: " + categoria + 
           ", Precio: $" + precio + 
           ", Precio c/IVA: $" + precio_con_iva;
}

// Factory de formas geométricas
function crear_rectangulo(ancho, alto) {
    let area = ancho * alto;
    let perimetro = 2 * (ancho + alto);
    return "Rectángulo " + ancho + "x" + alto + 
           " -> Área: " + area + ", Perímetro: " + perimetro;
}

function crear_circulo(radio) {
    let pi = 3.14159;
    let area = pi * radio * radio;
    let circunferencia = 2 * pi * radio;
    return "Círculo r=" + radio + 
           " -> Área: " + area + ", Circunferencia: " + circunferencia;
}

// Ejemplos de uso
let persona = crear_persona("Ana García", 28, "ana@email.com");
let producto = crear_producto("Laptop", 1000, "Electrónicos");
let rectangulo = crear_rectangulo(5, 3);
let circulo = crear_circulo(4);

return rectangulo + " | " + circulo;
```

## 🔗 Ejemplos de Integración

### Ejemplo Combinado: Sistema de Tienda
```javascript
// Funciones de productos
function crear_producto_detallado(id, nombre, precio, stock) {
    return id + ":" + nombre + ":$" + precio + ":" + stock + "u";
}

function calcular_precio_final(precio, cantidad, descuento) {
    let subtotal = precio * cantidad;
    let descuento_aplicado = subtotal * descuento;
    return subtotal - descuento_aplicado;
}

// Funciones de cliente
function obtener_descuento_cliente(tipo_cliente) {
    if (tipo_cliente == "premium") {
        return 0.20;
    } else {
        if (tipo_cliente == "regular") {
            return 0.10;
        } else {
            return 0.05;
        }
    }
}

// Función principal de venta
function procesar_venta(producto_info, cantidad, tipo_cliente) {
    // Simulamos parsing del producto (en un lenguaje real usaríamos split)
    let precio_base = 100; // Extraído de producto_info
    let stock_disponible = 50; // Extraído de producto_info
    
    if (cantidad > stock_disponible) {
        return "Error: Stock insuficiente";
    } else {
        let descuento = obtener_descuento_cliente(tipo_cliente);
        let precio_final = calcular_precio_final(precio_base, cantidad, descuento);
        let nuevo_stock = stock_disponible - cantidad;
        
        return "Venta procesada: " + cantidad + " unidades, " +
               "Precio final: $" + precio_final + 
               ", Stock restante: " + nuevo_stock;
    }
}

// Ejemplo de uso del sistema
let producto = crear_producto_detallado(1, "Laptop", 100, 50);
let venta = procesar_venta(producto, 3, "premium");

return venta;
```

---

## 🚀 Siguientes Pasos

Estos ejemplos te muestran el potencial del lenguaje LPP. Para continuar aprendiendo:

1. **Practica modificando ejemplos** - Cambia valores, añade funciones, experimenta
2. **Crea tus propias funciones** - Usa estos patrones como base para tus ideas
3. **Combina conceptos** - Mezcla operaciones matemáticas, lógica y cadenas
4. **Revisa la sintaxis** - Consulta [language-syntax.md](language-syntax.md) para detalles
5. **Explora la arquitectura** - Lee [architecture.md](architecture.md) para entender el intérprete

**¡Recuerda!** LPP está en desarrollo continuo. Estos ejemplos representan las capacidades actuales y servirán como base para futuras extensiones del lenguaje.

---

## 📚 Referencias

- [Guía de Inicio Rápido](quickstart.md) - Para empezar inmediatamente
- [Sintaxis del Lenguaje](language-syntax.md) - Referencia completa de sintaxis
- [Troubleshooting](troubleshooting.md) - Solución de problemas comunes
- [API Reference](api-reference.md) - Para desarrolladores del intérprete