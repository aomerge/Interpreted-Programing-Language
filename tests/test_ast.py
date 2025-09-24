from unittest import TestCase
from src.astNode import (
    Identifier,
    Program,
    Statement,
    LetStatement,
    ReturnStatement
)
from src.config.token_1 import Token, TokenType

import logging

class ASTTest(TestCase):
    logger = logging.getLogger(__name__)

    def test_let_program(self) -> None:
        source: str = 'let x = 5;'
        program: Program = Program(statements=[
    
            LetStatement(
                token=Token(TokenType.LET, 'let'),
                name=Identifier(
                    token=Token(TokenType.IDENT, 'x'),
                    value='x'
                ),
                value=Identifier(
                    token=Token(TokenType.INT, '5'),
                    value='5'
                )
            )
         ])
        
        program_str = str(program)

        self.assertEqual(program_str, source)
    
    def test_return_program(self) -> None:
        source: str = 'return = 5;'
        program: Program = Program(statements=[
    
            ReturnStatement(
                token=Token(TokenType.RETURN, 'return'),
                return_value=Identifier(
                    token=Token(TokenType.INT, '5'),
                    value='5'
                )
            )
         ]) 
        program_str = str(program)

        self.assertEqual(program_str, "return 5;")


