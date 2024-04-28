from unittest import TestCase
from src.lexer import Lexer
from src.parser_1 import Parser
from src.ast import Program


class ParcerTest(TestCase):
    def test_parcer_program(self) -> None:
        source: str = 'var a = 1;'
        lexer:Lexer =  Lexer(source)
        parcer:Parser = Parser(lexer)
        
        program:Program = parcer.getProgram()

        self.assertIsNotNone(program)
        self.assertEqual(program, Program)