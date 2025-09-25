# Interpreted Programming Language (LPP) - Documentación

Bienvenido a la documentación completa del **Interpreted Programming Language (LPP)**, un lenguaje de programación interpretado implementado en Python con características modernas y funcionalidades robustas.

## 📚 Índice de Documentación

### 🚀 Guías de Inicio
- [**Guía de Instalación**](installation.md) - Configuración y requisitos del sistema
- [**Guía de Inicio Rápido**](quickstart.md) - Primeros pasos con LPP
- [**Tutorial Básico**](tutorial.md) - Aprende LPP desde cero

### 📖 Referencias del Lenguaje
- [**Sintaxis del Lenguaje**](language-syntax.md) - Especificación completa de la sintaxis
- [**Tipos de Datos**](data-types.md) - Tipos soportados y sus características
- [**Operadores**](operators.md) - Operadores aritméticos, lógicos y de comparación
- [**Palabras Clave**](keywords.md) - Todas las palabras reservadas del lenguaje

### 🛠️ Arquitectura Técnica
- [**Arquitectura General**](architecture.md) - Visión general del sistema
- [**Lexer (Análisis Léxico)**](lexer.md) - Tokenización y análisis léxico
- [**Parser (Análisis Sintáctico)**](parser.md) - Construcción del AST
- [**Interpreter (Intérprete)**](interpreter.md) - Evaluación y ejecución
- [**AST (Abstract Syntax Tree)**](ast.md) - Estructura del árbol sintáctico

### 🔧 API y Desarrollo
- [**API Reference**](api-reference.md) - Documentación completa de la API
- [**Guía de Contribución**](contributing.md) - Cómo contribuir al proyecto
- [**Testing**](testing.md) - Ejecución y creación de pruebas
- [**Debugging**](debugging.md) - Técnicas de depuración

### 📝 Ejemplos y Casos de Uso
- [**Ejemplos de Código**](examples.md) - Ejemplos prácticos y casos de uso
- [**Best Practices**](best-practices.md) - Mejores prácticas de desarrollo
- [**FAQ**](faq.md) - Preguntas frecuentes

### 🔧 Herramientas y Utilidades
- [**Herramientas de Desarrollo**](development-tools.md) - Utilidades incluidas
- [**Configuración**](configuration.md) - Opciones de configuración
- [**Troubleshooting**](troubleshooting.md) - Solución de problemas comunes

## 🌟 Características Principales

LPP es un lenguaje de programación interpretado que incluye:

### ✨ Características del Lenguaje
- **Sintaxis moderna** inspirada en JavaScript y Python
- **Tipado dinámico** con verificación en tiempo de ejecución
- **Soporte para funciones** con parámetros y valores de retorno
- **Estructuras de control** (if, for, while)
- **Programación orientada a objetos** (clases, herencia)
- **Manejo de errores** robusto

### 🏗️ Arquitectura Robusta
- **Lexer modular** con soporte para comentarios y strings
- **Parser recursivo descendente** con manejo de precedencia
- **Intérprete eficiente** con evaluación de expresiones y sentencias
- **AST bien estructurado** para análisis y optimización

### 🧪 Calidad de Código
- **99% de cobertura de tests** en módulos críticos
- **208 tests unitarios** automatizados
- **Integración con SonarQube** para análisis de calidad
- **Documentación completa** con ejemplos

## 📈 Estado del Proyecto

| Componente | Cobertura | Tests | Estado |
|------------|-----------|-------|---------|
| **Lexer** | 99% | 29 tests | ✅ Completo |
| **Parser** | 93% | 47 tests | ✅ Completo |
| **Interpreter** | 91% | 48 tests | ✅ Completo |
| **AST** | 87% | 15 tests | ✅ Completo |
| **Total** | **88%** | **208 tests** | ✅ **Producción** |

## 🚀 Inicio Rápido

### Ejemplo Básico
```javascript
// Declaración de variables
let nombre = "LPP";
let version = 1.0;
let activo = true;

// Función simple
function saludar(nombre) {
    return "¡Hola, " + nombre + "!";
}

// Uso de la función
return saludar(nombre);
```

### Ejecución
```bash
python -m lpp archivo.lpp
```

## 🤝 Contribuir

¿Interesado en contribuir? Revisa nuestra [Guía de Contribución](contributing.md) para comenzar.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT. Ver [LICENSE](../LICENSE) para más detalles.

---

**Developed with ❤️ by [aomerge](https://github.com/aomerge)**