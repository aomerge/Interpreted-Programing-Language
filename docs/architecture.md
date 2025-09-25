# Arquitectura del Intérprete LPP

Esta documentación describe la arquitectura interna del intérprete LPP, sus componentes principales y cómo interactúan entre sí para ejecutar programas.

## 📋 Tabla de Contenidos

- [Visión General](#visión-general)
- [Pipeline de Procesamiento](#pipeline-de-procesamiento)
- [Componentes Principales](#componentes-principales)
- [Flujo de Datos](#flujo-de-datos)
- [Estructuras de Datos](#estructuras-de-datos)
- [Patrones de Diseño](#patrones-de-diseño)
- [Extensibilidad](#extensibilidad)
- [Rendimiento](#rendimiento)

## 🏗️ Visión General

LPP es un intérprete modular construido en Python que sigue una arquitectura de pipeline clásica para procesamiento de lenguajes. El sistema se divide en varias fases independientes que transforman el código fuente paso a paso hasta su ejecución.

### Arquitectura de Alto Nivel

```
Código Fuente (String)
        ↓
    [LEXER] → Tokens
        ↓
    [PARSER] → AST (Abstract Syntax Tree)
        ↓
    [INTERPRETER] → Resultado/Valor
```

### Principios de Diseño

1. **Separación de Responsabilidades**: Cada componente tiene una función específica y bien definida
2. **Modularidad**: Los componentes pueden ser desarrollados, probados y mantenidos independientemente
3. **Extensibilidad**: Facilita la adición de nuevas características del lenguaje
4. **Testabilidad**: Cada componente puede ser probado de forma aislada
5. **Claridad**: El código es legible y autodocumentado

## 🔄 Pipeline de Procesamiento

### Fase 1: Análisis Léxico (Lexer)
**Entrada**: Código fuente como string  
**Salida**: Secuencia de tokens  
**Responsabilidad**: Convertir caracteres en tokens significativos

```python
"let x = 42;" → [LET, IDENTIFIER(x), ASSIGN, NUMBER(42), SEMICOLON]
```

### Fase 2: Análisis Sintáctico (Parser)
**Entrada**: Secuencia de tokens  
**Salida**: Árbol de Sintaxis Abstracta (AST)  
**Responsabilidad**: Verificar sintaxis y crear estructura jerárquica

```python
[LET, IDENTIFIER(x), ASSIGN, NUMBER(42)] → LetStatement(identifier=x, value=NumberLiteral(42))
```

### Fase 3: Interpretación (Interpreter)
**Entrada**: AST  
**Salida**: Valor ejecutado/resultado  
**Responsabilidad**: Ejecutar las instrucciones y producir resultados

```python
LetStatement(x, 42) → Object(INTEGER, 42) almacenado en entorno
```

## 🧩 Componentes Principales

### 1. Sistema de Tokens (`src/config/token_1.py`)

```python
class TokenType(Enum):
    # Literales
    NUMBER = "NUMBER"
    STRING = "STRING" 
    IDENTIFIER = "IDENTIFIER"
    
    # Palabras clave
    LET = "LET"
    FUNCTION = "FUNCTION"
    RETURN = "RETURN"
    IF = "IF"
    ELSE = "ELSE"
    TRUE = "TRUE"
    FALSE = "FALSE"
    NULL = "NULL"
    
    # Operadores
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    ASTERISK = "*"
    SLASH = "/"
    
    # Delimitadores
    SEMICOLON = ";"
    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"
```

**Características**:
- Enumeración type-safe para todos los tipos de tokens
- Mapeo directo entre código fuente y representación interna
- Extensible para nuevos tokens sin romper compatibilidad

### 2. Análisis Léxico (Lexer)

#### CharStream (`src/lexer/charstream.py`)
```python
class CharStream:
    def __init__(self, input_text: str):
        self.input = input_text
        self.position = 0
        self.current_char = self.input[0] if input_text else None
    
    def advance(self) -> None:
        """Avanza al siguiente carácter"""
        
    def peek(self, offset: int = 1) -> str:
        """Ve el carácter en posición actual + offset"""
```

**Responsabilidades**:
- Gestión de la posición actual en el código fuente
- Lectura carácter por carácter con look-ahead
- Manejo de fin de archivo

#### Scanner (`src/lexer/scanner.py`)
```python
class Scanner:
    def __init__(self, charstream: CharStream):
        self.charstream = charstream
    
    def read_string(self, quote_char: str) -> str:
        """Lee una cadena completa entre comillas"""
    
    def read_number(self) -> str:
        """Lee un número (entero o decimal)"""
    
    def read_identifier(self) -> str:
        """Lee un identificador o palabra clave"""
```

**Responsabilidades**:
- Reconocimiento de patrones de tokens complejos
- Manejo de strings con caracteres de escape
- Diferenciación entre números enteros y decimales

#### Lexer Principal (`src/lexer/lexer.py`)
```python
class Lexer:
    def __init__(self, input_text: str):
        self.charstream = CharStream(input_text)
        self.scanner = Scanner(self.charstream)
        self.keywords = Keywords()
    
    def next_token(self) -> Token:
        """Obtiene el siguiente token del código fuente"""
    
    def skip_whitespace(self) -> None:
        """Omite espacios en blanco y comentarios"""
```

**Características**:
- Integra CharStream y Scanner para análisis completo
- Maneja whitespace y comentarios automáticamente
- Reconoce palabras clave vs identificadores

### 3. Análisis Sintáctico (Parser)

#### AST Nodes (`src/astNode/`)

**Jerarquía de Nodos**:
```python
ASTNode (abstracto)
├── Statement (abstracto)
│   ├── LetStatement
│   ├── ReturnStatement
│   ├── ExpressionStatement
│   ├── BlockStatement
│   └── IfStatement
└── Expression (abstracto)
    ├── NumberLiteral
    ├── StringLiteral
    ├── BooleanLiteral
    ├── NullLiteral
    ├── Identifier
    ├── InfixExpression
    ├── PrefixExpression
    └── FunctionCall
```

**Ejemplo de Nodo**:
```python
class LetStatement(Statement):
    def __init__(self, identifier: Identifier, value: Expression):
        self.identifier = identifier
        self.value = value
    
    def token_literal(self) -> str:
        return "let"
    
    def __str__(self) -> str:
        return f"let {self.identifier} = {self.value};"
```

#### Parser Core (`src/parser/parser_core.py`)
```python
class ModularParser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.errors = []
        self.current_token = None
        self.peek_token = None
    
    def parse_program(self) -> Program:
        """Punto de entrada principal del parser"""
    
    def parse_statement(self) -> Statement:
        """Delega parsing de statements a parsers específicos"""
```

#### Parsers Especializados

**Statement Parser** (`src/parser/statement_parser.py`):
```python
class StatementParser:
    def parse_let_statement(self) -> LetStatement:
    def parse_return_statement(self) -> ReturnStatement:
    def parse_if_statement(self) -> IfStatement:
    def parse_block_statement(self) -> BlockStatement:
```

**Expression Parser** (`src/parser/expression_parser.py`):
```python
class ExpressionParser:
    def parse_expression(self, precedence: Precedence) -> Expression:
    def parse_infix_expression(self, left: Expression) -> Expression:
    def parse_prefix_expression(self) -> Expression:
```

**Function Parser** (`src/parser/function_parser.py`):
```python
class FunctionParser:
    def parse_function_definition(self) -> FunctionDefinition:
    def parse_function_call(self, function: Expression) -> FunctionCall:
    def parse_function_parameters(self) -> List[Identifier]:
```

### 4. Sistema de Interpretación

#### Evaluadores Especializados

**Expression Evaluator** (`src/interpreter/eval_expressions.py`):
```python
class ExpressionEvaluator:
    def evaluate(self, node: Expression, env: Environment) -> Object:
        """Punto de entrada para evaluar expresiones"""
    
    def eval_infix_expression(self, operator: str, left: Object, right: Object) -> Object:
        """Evalúa operaciones binarias (+, -, *, /, ==, !=, etc.)"""
    
    def eval_prefix_expression(self, operator: str, right: Object) -> Object:
        """Evalúa operaciones unarias (-, !)"""
```

**Statement Evaluator** (`src/interpreter/eval_statements.py`):
```python
class StatementEvaluator:
    def evaluate(self, node: Statement, env: Environment) -> Object:
        """Punto de entrada para evaluar statements"""
    
    def eval_let_statement(self, node: LetStatement, env: Environment) -> Object:
        """Evalúa declaraciones de variables"""
    
    def eval_if_statement(self, node: IfStatement, env: Environment) -> Object:
        """Evalúa condicionales if-else"""
```

#### Sistema de Objetos (`src/config/object.py`)
```python
class ObjectType(Enum):
    INTEGER = "INTEGER"
    STRING = "STRING"
    BOOLEAN = "BOOLEAN"
    NULL = "NULL"
    RETURN_VALUE = "RETURN_VALUE"
    ERROR = "ERROR"
    FUNCTION = "FUNCTION"

class Object:
    def __init__(self, obj_type: ObjectType, value):
        self.type = obj_type
        self.value = value
```

#### Entorno de Ejecución (`src/config/environment.py`)
```python
class Environment:
    def __init__(self, outer: Optional['Environment'] = None):
        self.store = {}
        self.outer = outer  # Entorno padre para scope anidado
    
    def get(self, name: str) -> Object:
        """Busca variable en scope actual y padres"""
    
    def set(self, name: str, value: Object) -> Object:
        """Define variable en scope actual"""
```

## 🔄 Flujo de Datos

### Ejemplo Completo: `let x = 5 + 3;`

#### Fase 1: Tokenización
```
Input: "let x = 5 + 3;"
Lexer Process:
  'l','e','t' → LET token
  ' ' → skip whitespace  
  'x' → IDENTIFIER token
  ' ' → skip whitespace
  '=' → ASSIGN token
  ' ' → skip whitespace
  '5' → NUMBER token (value: 5)
  ' ' → skip whitespace
  '+' → PLUS token
  ' ' → skip whitespace
  '3' → NUMBER token (value: 3)
  ';' → SEMICOLON token

Output: [LET, IDENTIFIER(x), ASSIGN, NUMBER(5), PLUS, NUMBER(3), SEMICOLON]
```

#### Fase 2: Parsing
```
Tokens: [LET, IDENTIFIER(x), ASSIGN, NUMBER(5), PLUS, NUMBER(3), SEMICOLON]
Parser Process:
  1. Reconoce LET → StatementParser.parse_let_statement()
  2. Expects IDENTIFIER → obtiene 'x'
  3. Expects ASSIGN → confirma '='
  4. Llama ExpressionParser.parse_expression()
     - Reconoce NUMBER(5) → NumberLiteral(5)
     - Reconoce PLUS → operador infijo
     - Reconoce NUMBER(3) → NumberLiteral(3)
     - Construye InfixExpression(NumberLiteral(5), "+", NumberLiteral(3))
  5. Expects SEMICOLON → confirma ';'
  
Output: LetStatement(
    identifier=Identifier("x"),
    value=InfixExpression(
        left=NumberLiteral(5),
        operator="+", 
        right=NumberLiteral(3)
    )
)
```

#### Fase 3: Interpretación
```
AST: LetStatement(identifier="x", value=InfixExpression(...))
Interpreter Process:
  1. StatementEvaluator.eval_let_statement()
  2. Evalúa value usando ExpressionEvaluator
     - eval_infix_expression("+", Object(5), Object(3))
     - Retorna Object(INTEGER, 8)
  3. Environment.set("x", Object(INTEGER, 8))
  4. Variable 'x' ahora disponible con valor 8

Output: Object(INTEGER, 8) stored in environment["x"]
```

## 🗂️ Estructuras de Datos

### 1. Tokens
```python
@dataclass
class Token:
    type: TokenType
    literal: str
    
# Ejemplo:
Token(TokenType.NUMBER, "42")
Token(TokenType.IDENTIFIER, "variable_name")
Token(TokenType.PLUS, "+")
```

### 2. AST Program
```python
class Program(ASTNode):
    def __init__(self):
        self.statements = []  # Lista de Statement objects
    
    def add_statement(self, stmt: Statement):
        self.statements.append(stmt)
```

### 3. Environment Stack
```python
# Entorno global
global_env = Environment()

# Entorno de función (anidado)
function_env = Environment(outer=global_env)

# Búsqueda en cascade:
# function_env.get("var") → busca en function_env.store
# Si no encuentra → busca en global_env.store
# Si no encuentra → retorna error
```

### 4. Object System
```python
# Diferentes tipos de objetos runtime
integer_obj = Object(ObjectType.INTEGER, 42)
string_obj = Object(ObjectType.STRING, "hello")
bool_obj = Object(ObjectType.BOOLEAN, True)
null_obj = Object(ObjectType.NULL, None)
return_obj = Object(ObjectType.RETURN_VALUE, integer_obj)
error_obj = Object(ObjectType.ERROR, "Division by zero")
```

## 🎨 Patrones de Diseño

### 1. Visitor Pattern (en AST)
```python
# Cada nodo AST sabe cómo ser evaluado
class NumberLiteral(Expression):
    def accept(self, evaluator):
        return evaluator.visit_number_literal(self)

# El evaluador implementa la lógica específica
class ExpressionEvaluator:
    def visit_number_literal(self, node: NumberLiteral) -> Object:
        return Object(ObjectType.INTEGER, node.value)
```

### 2. Strategy Pattern (en Parsing)
```python
class ModularParser:
    def __init__(self, lexer: Lexer):
        # Diferentes estrategias para diferentes tipos
        self.statement_parser = StatementParser(self)
        self.expression_parser = ExpressionParser(self)
        self.function_parser = FunctionParser(self)
    
    def parse_statement(self) -> Statement:
        # Delega a la estrategia apropiada
        if self.current_token.type == TokenType.LET:
            return self.statement_parser.parse_let_statement()
        elif self.current_token.type == TokenType.FUNCTION:
            return self.function_parser.parse_function_definition()
```

### 3. Chain of Responsibility (en Error Handling)
```python
class Parser:
    def __init__(self):
        self.errors = []  # Colecciona todos los errores
    
    def add_error(self, message: str):
        self.errors.append(f"Parse error: {message}")
    
    def has_errors(self) -> bool:
        return len(self.errors) > 0
```

### 4. Factory Pattern (en Object Creation)
```python
class ObjectFactory:
    @staticmethod
    def create_integer(value: int) -> Object:
        return Object(ObjectType.INTEGER, value)
    
    @staticmethod  
    def create_boolean(value: bool) -> Object:
        return Object(ObjectType.BOOLEAN, value)
    
    @staticmethod
    def create_error(message: str) -> Object:
        return Object(ObjectType.ERROR, message)
```

## 🔧 Extensibilidad

### Añadir Nuevo Tipo de Token

1. **Actualizar TokenType**:
```python
class TokenType(Enum):
    # ... tokens existentes ...
    WHILE = "WHILE"  # Nuevo token
```

2. **Actualizar Keywords**:
```python
KEYWORDS = {
    # ... palabras existentes ...
    "while": TokenType.WHILE,
}
```

3. **El Lexer automáticamente reconocerá la nueva palabra clave**

### Añadir Nueva Statement

1. **Crear AST Node**:
```python
class WhileStatement(Statement):
    def __init__(self, condition: Expression, body: Statement):
        self.condition = condition
        self.body = body
```

2. **Extender StatementParser**:
```python
class StatementParser:
    def parse_while_statement(self) -> WhileStatement:
        # Lógica de parsing específica
        pass
```

3. **Extender StatementEvaluator**:
```python
class StatementEvaluator:
    def eval_while_statement(self, node: WhileStatement, env: Environment) -> Object:
        # Lógica de evaluación específica
        pass
```

### Añadir Nuevo Operador

1. **Añadir TokenType**:
```python
MODULO = "%"
```

2. **Actualizar Precedencia**:
```python
class Precedence(Enum):
    PRODUCT = 5  # *, /, % (mismo nivel)
```

3. **Extender ExpressionEvaluator**:
```python
def eval_infix_expression(self, operator: str, left: Object, right: Object) -> Object:
    if operator == "%":
        return self.eval_modulo_operation(left, right)
```

## ⚡ Rendimiento

### Optimizaciones Actuales

1. **Single-Pass Lexer**: No requiere pre-procesamiento
2. **Recursive Descent Parser**: Eficiente para gramáticas LL(1)
3. **Tree-Walking Interpreter**: Simple y directo
4. **Lazy Token Generation**: Tokens generados on-demand

### Métricas de Performance

```python
# Benchmark típico (Python 3.12):
# Lexer: ~10,000 tokens/segundo
# Parser: ~5,000 statements/segundo  
# Interpreter: ~2,000 operations/segundo

# Memoria:
# Token: ~64 bytes cada uno
# AST Node: ~128-256 bytes dependiendo del tipo
# Object: ~96 bytes cada uno
```

### Estrategias de Optimización Futuras

1. **Bytecode Generation**: Compilar AST a bytecode intermedio
2. **Constant Folding**: Optimizar expresiones constantes en tiempo de compilación
3. **Tail Call Optimization**: Para recursión eficiente
4. **Environment Caching**: Cache de lookups de variables frecuentes

## 🧪 Testing Architecture

### Estructura de Tests
```
tests/
├── test_lexer.py           # Tests unitarios del lexer
├── test_scanner.py         # Tests del scanner
├── test_parser_core.py     # Tests del parser principal
├── test_expression_parser.py # Tests de parsing de expresiones
├── test_function_parser.py  # Tests de parsing de funciones
├── test_statement_parser.py # Tests de parsing de statements
├── test_eval_expressions.py # Tests de evaluación de expresiones
├── test_eval_statements.py # Tests de evaluación de statements
├── test_ast.py            # Tests de nodos AST
└── test_dispatcher.py     # Tests del dispatcher
```

### Estrategia de Testing

1. **Unit Tests**: Cada componente testado independientemente
2. **Integration Tests**: Testing del pipeline completo
3. **Mocking**: Uso extensivo de mocks para aislar componentes
4. **Coverage**: 88% de cobertura de código fuente

---

## 📚 Referencias

- [Guía de Inicio Rápido](quickstart.md) - Para comenzar a usar LPP
- [Sintaxis del Lenguaje](language-syntax.md) - Especificación completa del lenguaje
- [Ejemplos de Código](examples.md) - Programas de ejemplo
- [API Reference](api-reference.md) - Documentación técnica detallada

Esta arquitectura proporciona una base sólida para el desarrollo continuo de LPP, permitiendo extensiones futuras manteniendo la claridad y modularidad del código.