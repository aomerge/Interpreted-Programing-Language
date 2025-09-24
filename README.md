# Interpreted Programming Language

Un lenguaje de programación interpretado personalizado implementado en Python con características similares a JavaScript y otros lenguajes modernos.

## Descripción

Este proyecto implementa un intérprete completo para un lenguaje de programación personalizado que incluye:
- **Lexer**: Análisis léxico para tokenizar el código fuente
- **Parser**: Análisis sintáctico para construir el AST (Abstract Syntax Tree)
- **Interpreter**: Evaluación del AST para ejecutar el programa

## Características del Lenguaje

### Tipos de Datos Soportados
- **Enteros**: `5`, `25`, `-10`
- **Cadenas**: `"Hello, World!"`, `'texto'`
- **Booleanos**: `true`, `false`

### Palabras Clave
- `let` - Declaración de variables
- `function` - Definición de funciones
- `return` - Retorno de valores
- `if` - Condicionales
- `class` - Definición de clases
- `for`, `while` - Bucles
- `const` - Constantes
- `public`, `private`, `protected` - Modificadores de acceso
- `static`, `abstract` - Modificadores de clase
- `extends` - Herencia
- `self`, `super` - Referencias de objeto
- `and`, `or`, `not` - Operadores lógicos

### Operadores
- **Aritméticos**: `+`, `-`, `*`, `/`
- **Comparación**: `==`, `!=`, `>`, `<`, `>=`, `<=`
- **Asignación**: `=`
- **Lógicos**: `and`, `or`, `not`

### Símbolos
- **Paréntesis**: `(`, `)`
- **Llaves**: `{`, `}`
- **Delimitadores**: `;`, `,`
- **Comillas**: `"`, `'`

## Estructura del Proyecto

```
src/
├── lexer.py          # Analizador léxico
├── parser_1.py       # Analizador sintáctico
├── interpreter.py    # Intérprete
├── ast.py           # Definiciones del AST
├── object.py        # Tipos de objetos
└── token_1.py       # Definiciones de tokens

run_test.py          # Archivo de pruebas y ejemplos
README.md           # Este archivo
```

## Instalación y Uso

### Prerrequisitos
- Python 3.x

### Ejecución
1. Clona el repositorio:
```bash
git clone https://github.com/aomerge/Interpreted-Programing-Language.git
cd Interpreted-Programing-Language
```

2. Ejecuta el archivo de prueba:
```bash
python run_test.py
```

### Uso Programático

```python
from src.lexer import Lexer
from src.parser_1 import Parser
from src.interpreter import Interpreter

# Código fuente en tu lenguaje
codigo_fuente = '''
let x = 5;
let y = 25;
return x + y;
'''

# Crear lexer y parser
lexer = Lexer(codigo_fuente)
parser = Parser(lexer)

# Parsear el código
program = parser.getProgram()

# Verificar errores
if parser.errors:
    for error in parser.errors:
        print(error)
else:
    # Interpretar el programa
    interpreter = Interpreter()
    resultado = interpreter.interpret(program)
    print(f"Resultado: {resultado}")
```

## Ejemplos de Código

### Ejemplo Básico - Operaciones Aritméticas
```javascript
let x = 5;
let y = 25;
return x + y;
```
**Salida**: `30`

### Ejemplo con Cadenas
```javascript
return "Hello, World!";
```
**Salida**: `"Hello, World!"`

### Ejemplo Complejo (Sintaxis Soportada)
```javascript
let nombre = "Juan";
let edad = 25;
let activo = true;

function saludar(nombre) {
    return "Hola, " + nombre;
}

if (edad >= 18) {
    return saludar(nombre);
}
```

## Tokens Soportados

| Token | Descripción | Ejemplo |
|-------|-------------|---------|
| `LET` | Declaración de variable | `let x = 5;` |
| `FUNCTION` | Definición de función | `function test() {}` |
| `RETURN` | Retorno de valor | `return x;` |
| `INT` | Número entero | `42` |
| `STRING` | Cadena de texto | `"texto"` |
| `IDENT` | Identificador | `variable` |
| `ASSIGN` | Asignación | `=` |
| `PLUS` | Suma | `+` |
| `MINUS` | Resta | `-` |
| `MULTIPLICATION` | Multiplicación | `*` |
| `DIVISION` | División | `/` |
| `EQUAL` | Igualdad | `==` |
| `NOT_EQUAL` | Desigualdad | `!=` |

## Ejecutar Pruebas

El archivo `run_test.py` contiene ejemplos de uso del intérprete:

```bash
python run_test.py
```

Este archivo demuestra:
- Declaración de variables con `let`
- Operaciones aritméticas
- Retorno de valores
- Manejo de cadenas

## Arquitectura

### 1. Lexer (Análisis Léxico)
- Convierte el código fuente en tokens
- Reconoce palabras clave, identificadores, números y operadores
- Maneja espacios en blanco y caracteres especiales

### 2. Parser (Análisis Sintáctico)
- Construye el AST a partir de los tokens
- Implementa la gramática del lenguaje
- Detecta errores de sintaxis

### 3. Interpreter (Intérprete)
- Evalúa el AST
- Ejecuta las operaciones
- Maneja el entorno de variables

## Contribuir

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Añadir nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Autor

**aomerge** - [GitHub Profile](https://github.com/aomerge)

---

*Este es un proyecto educativo para aprender sobre la implementación de lenguajes de programación e intérpretes.*
