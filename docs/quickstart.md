# Guía de Inicio Rápido

¡Bienvenido a LPP! Esta guía te ayudará a ejecutar tu primer programa en LPP en menos de 5 minutos.

## ⚡ Tu Primer Programa en 5 Minutos

### 1. Hola Mundo
Crea un archivo llamado `hola.lpp`:

```javascript
// Mi primer programa en LPP
return "¡Hola, Mundo!";
```

Ejecuta:
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

**Salida esperada:** `¡Hola, Mundo!`

### 2. Variables y Operaciones
```javascript
// Variables básicas
let numero = 42;
let texto = "LPP es genial";
let activo = true;

// Operación simple
let suma = 10 + 5;
return suma;
```

**Salida esperada:** `15`

### 3. Funciones
```javascript
// Definir una función
function multiplicar(a, b) {
    return a * b;
}

// Usar la función
let resultado = multiplicar(6, 7);
return resultado;
```

**Salida esperada:** `42`

## 🛠️ Herramientas de Desarrollo Incluidas

### Script de Pruebas Rápidas
```bash
# Ejecutar ejemplos predefinidos
python run_test.py
```

### Script de Validación del Parser
```bash
# Validar sintaxis de archivos
python validate_parser.py examples/mi_archivo.lpp
```

### Ejecutor Interactivo
Crea un archivo `repl.py`:

```python
from src.lexer.lexer import Lexer
from src.parser.parser_core import ModularParser
from src.interpreter.interpreter import Interpreter

def ejecutar_lpp(codigo):
    """Ejecuta código LPP y retorna el resultado."""
    try:
        lexer = Lexer(codigo)
        parser = ModularParser(lexer)
        program = parser.parse_program()
        
        if parser.errors:
            return f"Errores de sintaxis: {parser.errors}"
        
        interpreter = Interpreter()
        result = interpreter.interpret(program)
        return result.value if result else None
        
    except Exception as e:
        return f"Error: {e}"

# REPL simple
if __name__ == "__main__":
    print("LPP Interactive Shell (escribe 'quit' para salir)")
    while True:
        try:
            codigo = input("lpp> ")
            if codigo.lower() == 'quit':
                break
            resultado = ejecutar_lpp(codigo)
            print(f"=> {resultado}")
        except KeyboardInterrupt:
            break
        except EOFError:
            break
    print("\\n¡Hasta luego!")
```

Ejecuta tu REPL:
```bash
python repl.py
```

## 🎯 Ejemplos por Categoría

### Variables y Tipos de Datos
```javascript
// Números
let entero = 42;
let decimal = 3.14;
let negativo = -10;

// Cadenas
let saludo = "Hola";
let comillas = 'También funciona';
let concatenado = saludo + ", mundo!";

// Booleanos
let verdadero = true;
let falso = false;

return concatenado;  // "Hola, mundo!"
```

### Operadores Aritméticos
```javascript
let a = 10;
let b = 3;

let suma = a + b;        // 13
let resta = a - b;       // 7
let multiplicacion = a * b;  // 30
let division = a / b;    // 3.33...

return suma;
```

### Operadores de Comparación
```javascript
let x = 5;
let y = 10;

let mayor = x > y;       // false
let menor = x < y;       // true
let igual = x == y;      // false
let diferente = x != y;  // true

return menor;  // true
```

### Funciones con Parámetros
```javascript
// Función que calcula el área de un rectángulo
function area_rectangulo(ancho, alto) {
    return ancho * alto;
}

// Función que saluda personalmente
function saludar_personal(nombre, apellido) {
    return "Hola, " + nombre + " " + apellido + "!";
}

// Usar las funciones
let mi_area = area_rectangulo(5, 3);
let mi_saludo = saludar_personal("Juan", "Pérez");

return mi_area;  // 15
```

### Estructuras de Control Básicas
```javascript
// Condicional simple
let edad = 18;

if (edad >= 18) {
    return "Eres mayor de edad";
} else {
    return "Eres menor de edad";
}
```

## 🔧 Comandos Útiles

### Ejecución de Archivos
```bash
# Método directo con Python
python -c "
from src.lexer.lexer import Lexer
from src.parser.parser_core import ModularParser  
from src.interpreter.interpreter import Interpreter

with open('mi_programa.lpp', 'r') as f:
    code = f.read()

lexer = Lexer(code)
parser = ModularParser(lexer)
program = parser.parse_program()

if parser.errors:
    print('Errores:', parser.errors)
else:
    interpreter = Interpreter()
    result = interpreter.interpret(program)
    print('Resultado:', result.value if result else 'None')
"
```

### Depuración Básica
```python
# debug_lpp.py
from src.lexer.lexer import Lexer
from src.parser.parser_core import ModularParser

def debug_tokens(codigo):
    """Muestra todos los tokens de un código."""
    lexer = Lexer(codigo)
    tokens = []
    
    while True:
        token = lexer.next_token()
        tokens.append(token)
        if token.type.name == 'EOF':
            break
    
    for i, token in enumerate(tokens):
        print(f"{i:2d}: {token.type.name:15} | {repr(token.literal)}")

def debug_ast(codigo):
    """Muestra la estructura del AST."""
    lexer = Lexer(codigo)
    parser = ModularParser(lexer)
    program = parser.parse_program()
    
    print("AST Structure:")
    print(f"Program with {len(program.statements)} statements:")
    for i, stmt in enumerate(program.statements):
        print(f"  {i}: {type(stmt).__name__}")

# Ejemplo de uso
if __name__ == "__main__":
    codigo = "let x = 5; return x + 10;"
    print("=== TOKENS ===")
    debug_tokens(codigo)
    print("\\n=== AST ===")
    debug_ast(codigo)
```

## 🚀 Próximos Pasos

Ahora que ya ejecutaste tu primer programa:

1. 📚 **Aprende más sintaxis**: [Tutorial Completo](tutorial.md)
2. 🔍 **Explora ejemplos**: [Ejemplos de Código](examples.md)
3. 🏗️ **Entiende la arquitectura**: [Arquitectura del Sistema](architecture.md)
4. 🛠️ **APIs y desarrollo**: [API Reference](api-reference.md)

## 💡 Consejos Rápidos

### ✅ Buenas Prácticas
- Siempre termina las declaraciones con `;`
- Usa nombres descriptivos para variables y funciones
- Incluye comentarios con `//` para explicar código complejo
- Verifica errores del parser antes de interpretar

### ⚠️ Errores Comunes
- **Olvidar `;`**: `let x = 5` → `let x = 5;`
- **Comillas mal cerradas**: `"hola` → `"hola"`
- **Nombres reservados**: `let function = 5;` (función es palabra clave)
- **Paréntesis desbalanceados**: `if (x > 5 { }` → `if (x > 5) { }`

## 🆘 ¿Necesitas Ayuda?

- 📖 **Documentación**: [README principal](README.md)
- 🐛 **Problemas**: [Troubleshooting](troubleshooting.md) 
- ❓ **Preguntas**: [FAQ](faq.md)
- 🤝 **Contribuir**: [Guía de Contribución](contributing.md)

---

**¡Felicidades!** 🎉 Ya tienes LPP funcionando. ¡Ahora puedes crear programas increíbles!