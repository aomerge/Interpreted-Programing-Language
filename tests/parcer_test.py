from unittest import TestCase
from src.lexer import Lexer
from src.parser_1 import Parser
from typing import (    
    List,
    Union
)
from src.ast import (
    Program,
    Statement,
    LetStatement
)


class ParcerTest(TestCase):
    def test_parcer_program(self) -> None:
        """ test_parcer_program:
        This function is responsible for testing the parcer program 
        """
        source: str = 'var a = 1;'
        lexer:Lexer =  Lexer(source)
        parcer:Parser = Parser(lexer)
        
        program:Program = parcer.getProgram()

        self.assertIsNotNone(program)
        self.assertIsInstance(program, Program)

    
    def test_parcer_let_statement(self) -> None:
        """ test_parcer_let_statement:
        This function is responsible for testing the parcer let statement 
        """
        source: str = '''
            let x = 5;
            let y = 10; 
            let foobar = 838383;
        '''
        lexer:Lexer =  Lexer(source)
        parcer:Parser = Parser(lexer)
        print(parcer) 
        
        program:Program = parcer.getProgram()        

        self.assertEqual(len(program.statements), 3)

        for statement in program.statements:
            self.assertEqual(statement.token_literal(), 'let')
            self.assertIsInstance(statement, LetStatement)