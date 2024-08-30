from src.lexer import Lexer
from src.parser_1 import Parser
from src.interpreter import Interpreter
from src.ast import Program  # Asegúrate de que el archivo se llama custom_ast.py

# Código fuente de ejemplo en tu lenguaje
codigo_fuente = '''
let x = 5;
let y = x + 10;
return y;
'''

# Crear un lexer y un parser
lexer = Lexer(codigo_fuente)
parser = Parser(lexer)

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
    print(f"Resultado del programa: {resultado}")

