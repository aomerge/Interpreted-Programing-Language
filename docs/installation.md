# Guía de Instalación

Esta guía te llevará paso a paso a través del proceso de instalación y configuración del Interpreted Programming Language (LPP).

## 📋 Requisitos del Sistema

### Requisitos Mínimos
- **Python**: 3.8 o superior
- **Sistema Operativo**: Windows 10, macOS 10.14, o Linux (Ubuntu 18.04+)
- **RAM**: 512 MB disponible
- **Espacio en Disco**: 100 MB libres

### Requisitos Recomendados
- **Python**: 3.11 o superior
- **RAM**: 2 GB disponible
- **Espacio en Disco**: 500 MB libres
- **Git**: Para clonar el repositorio

## 🛠️ Instalación

### Método 1: Clonación desde GitHub (Recomendado)

1. **Clonar el repositorio**
```bash
git clone https://github.com/aomerge/Interpreted-Programing-Language.git
cd Interpreted-Programing-Language
```

2. **Crear entorno virtual (Opcional pero recomendado)**
```bash
# En Windows
python -m venv venv
venv\\Scripts\\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Verificar instalación**
```bash
python run_test.py
```

### Método 2: Descarga Directa

1. **Descargar ZIP**
   - Ve a la [página del repositorio](https://github.com/aomerge/Interpreted-Programing-Language)
   - Haz clic en "Code" > "Download ZIP"
   - Extrae el archivo en tu directorio preferido

2. **Navegar al directorio**
```bash
cd Interpreted-Programing-Language
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 📦 Dependencias

### Dependencias de Producción
```txt
# Sin dependencias externas requeridas
# LPP utiliza solo la biblioteca estándar de Python
```

### Dependencias de Desarrollo
```txt
# Testing
coverage==7.10.7
pytest==7.4.4
pytest-cov==4.1.0

# Linting
flake8==6.0.0
black==23.12.1

# Documentación
mkdocs==1.5.3
mkdocs-material==9.4.8
```

## ⚙️ Configuración

### Configuración Básica

No se requiere configuración adicional para el uso básico de LPP. El intérprete funciona con la configuración predeterminada.

### Configuración Avanzada

Para configuraciones avanzadas, puedes crear un archivo `lpp.config.json`:

```json
{
  "debug": false,
  "max_recursion_depth": 1000,
  "memory_limit": "100MB",
  "output_format": "json",
  "error_reporting": "verbose"
}
```

### Variables de Entorno

```bash
# Opcional: Configurar nivel de logging
export LPP_LOG_LEVEL=INFO

# Opcional: Directorio de trabajo personalizado
export LPP_WORK_DIR=/path/to/workspace
```

## 🧪 Verificación de la Instalación

### Prueba Básica
```bash
# Ejecutar tests básicos
python run_test.py
```

### Prueba Completa
```bash
# Ejecutar suite completa de tests
python -m unittest discover tests -v

# Verificar cobertura
coverage run -m unittest discover tests
coverage report
```

### Prueba Interactiva
```python
# test_installation.py
from src.lexer.lexer import Lexer
from src.parser.parser_core import ModularParser
from src.interpreter.interpreter import Interpreter

# Código de prueba
code = '''
let x = 5;
let y = 10;
return x + y;
'''

# Crear e ejecutar
lexer = Lexer(code)
parser = ModularParser(lexer)
program = parser.parse_program()

if parser.errors:
    print("Errores encontrados:", parser.errors)
else:
    interpreter = Interpreter()
    result = interpreter.interpret(program)
    print(f"Resultado: {result}")  # Debería mostrar: 15
```

## 🐛 Solución de Problemas Comunes

### Error: "Module not found"
```bash
# Asegúrate de estar en el directorio correcto
pwd
# Debería mostrar: .../Interpreted-Programing-Language

# Verifica que Python puede encontrar los módulos
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### Error: "Permission denied"
```bash
# En sistemas Unix/Linux, podrías necesitar permisos
chmod +x run_test.py
```

### Error: "Python version incompatible"
```bash
# Verifica tu versión de Python
python --version
# Debería ser 3.8 o superior

# Si tienes múltiples versiones, usa python3
python3 --version
```

### Problemas con el Entorno Virtual
```bash
# Recrear entorno virtual
rm -rf venv
python -m venv venv

# Activar
source venv/bin/activate  # Linux/macOS
# o
venv\\Scripts\\activate  # Windows

# Reinstalar dependencias
pip install -r requirements.txt
```

## 📋 Verificación Post-Instalación

Ejecuta el siguiente checklist para confirmar que todo está funcionando:

- [ ] ✅ Python 3.8+ instalado
- [ ] ✅ Repositorio clonado/descargado
- [ ] ✅ Dependencias instaladas
- [ ] ✅ Tests básicos pasan (`python run_test.py`)
- [ ] ✅ Tests unitarios pasan (`python -m unittest discover tests`)
- [ ] ✅ Importación exitosa de módulos principales

## 🚀 Próximos Pasos

Una vez completada la instalación:

1. 📖 Lee la [Guía de Inicio Rápido](quickstart.md)
2. 🎓 Sigue el [Tutorial Básico](tutorial.md)
3. 💡 Explora los [Ejemplos de Código](examples.md)
4. 🔧 Revisa la [API Reference](api-reference.md)

## 🆘 Obtener Ayuda

Si encuentras problemas durante la instalación:

1. **Revisa el [Troubleshooting](troubleshooting.md)**
2. **Consulta las [FAQ](faq.md)**
3. **Abre un issue en GitHub**
4. **Contacta al mantenedor**

---

**¿Instalación exitosa?** ¡Continúa con la [Guía de Inicio Rápido](quickstart.md)! 🎉