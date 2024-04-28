from src.lexer import Lexer
from src.ast import Program
class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer        

    def getProgram(self) -> Program:
        program: Program = Program(statements=[])
        return program