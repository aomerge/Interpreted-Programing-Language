from src.lexer.lexer import Lexer
from src.parser.parser_core import Parser  # Usar el nuevo parser modular
from src.interpreter.interpreter import Interpreter  # Fixed import path
from src.ast import Program  # Asegúrate de que el archivo se llama custom_ast.py
from src.confg.object import Integer

# Código fuente de ejemplo en tu lenguaje (simplificado para pruebas)
codigo_fuente = '''
let x = 5;
let y = 10;
return x + y;
'''

# Crear un lexer y un parser modular
lexer = Lexer(codigo_fuente)
parser = Parser(lexer)

print("=== PARSER MODULAR ===")
print(f"Componentes cargados:")
print(f"  - StatementParser: {type(parser.statement_parser).__name__}")
print(f"  - ExpressionParser: {type(parser.expression_parser).__name__}")
print(f"  - FunctionParser: {type(parser.function_parser).__name__}")
print()

# Parsear el código fuente para obtener el AST
program = parser.getProgram()

# Verificar errores de parseo
if parser.errors:
    print("Errores de parseo:")
    for error in parser.errors:
        print(error)
else:
    # Si no hay errores, interpretar el programa
    interpreter = Interpreter()
    resultado = interpreter.interpret(program)
    
    # Si el resultado es un objeto Integer, muestra su valor
    if isinstance(resultado, Integer):
        print(f"Resultado del programa: {resultado.value}")
    else:
        print(f"Resultado del programa: {resultado}")

