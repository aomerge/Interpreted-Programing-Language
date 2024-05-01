from unittest import TestCase
from src.lexer import Lexer
from src.parser_1 import Parser
from typing import (    
    List,
    Union,
    cast,
    Any,
)
from src.ast import (
    Expression,
    ExpressionStatement,
    Program,
    Statement,
    LetStatement,
    ReturnStatement,
    Identifier
)
import logging


class ParcerTest(TestCase):
    logger = logging.getLogger(__name__)

    def test_parcer_program(self) -> None:
        """ test_parcer_program:
        This function is responsible for testing the parcer program 
        """
        source: str = 'var a = 1;'
        lexer:Lexer =  Lexer(source)
        parcer:Parser = Parser(lexer)
        
        program:Program = parcer.getProgram()

        self.logger.debug(f'Program test_parcer_program: {program}')

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
        
        program:Program = parcer.getProgram()        

        self.assertEqual(len(program.statements), 3)

        for statement in program.statements:
            self.assertEqual(statement.token_literal(), 'let')
            self.assertIsInstance(statement, LetStatement)
    
    def test_name_in_let_statement(self) -> None:
        """ test_name_in_let_statement:
        This function is responsible for testing the name in let statement 
        """
        source: str = '''
            let x = 5;
            let y = 10; 
            let foobar = 838383;
        '''
        lexer:Lexer =  Lexer(source)
        parcer:Parser = Parser(lexer)
        program:Program = parcer.getProgram()

        names:List[str] = ['x', 'y', 'foobar']
        for i, statement in enumerate(program.statements):            
            self.assertEqual(statement.name.value, names[i])
    
    def test_parse_errors(self) -> None:
        """ test_parse_errors:
        This function is responsible for testing the parse errors 
        """
        source: str = '''
            let x 5;
        '''
        lexer:Lexer =  Lexer(source)
        parser:Parser = Parser(lexer)
        program:Program = parser.getProgram()

        self.assertEqual(len(parser.errors), 1)   

    def test_parse_return_statement(self) -> None:
        """ test_parse_return_statement:
        This function is responsible for testing the parse return statement 
        """
        source: str = '''
            return 5;
            return 10;
            return 838383;
        '''
        lexer:Lexer =  Lexer(source)
        parser:Parser = Parser(lexer)
        program:Program = parser.getProgram()        

        for statement in program.statements:
            self.assertEqual(statement.token_literal(), 'return')
            self.assertIsInstance(statement, ReturnStatement)
    
    def test_parse_identifier_expression(self) -> None:
        """ test_parse_identifier_expression:
        This function is responsible for testing the parse identifier expression 
        """
        source: str = 'foobar;'
        lexer:Lexer =  Lexer(source)
        parser:Parser = Parser(lexer)
        program:Program = parser.getProgram()

        self._test_program_statement(parser, program)        

        self.logger.debug(f'Program out: {program}')

        expression_statement = cast(ExpressionStatement, program.statements[0])

        
        self._test_literal_expression(expression_statement.expression, "foobar")

    def _test_program_statement(self,parser: Parser, program: Program, expected_statement_Count: int = 1 ) -> None:
        """ test_program_statement:
        This function is responsible for testing the program statement 
        """        
        if parser.errors:
            print(parser.errors)

        self.assertEqual(len(parser.errors), 0)
        
        self.assertEqual(len(program.statements), expected_statement_Count)
        self.assertIsInstance(program.statements[0], ExpressionStatement)
    
    def _test_literal_expression(self, expression:Expression, value:Any) -> None:
        """ _test_literal_expression:
        This function is responsible for testing the literal expression 
        """
        value_type: type = type(value)
        if value_type == str:
            self._test_identifier_expression(expression, value)
        elif value_type == int:
            self._test_identifier_expression(expression, value)
        elif value_type == bool:
            self._test_identifier_expression(expression, value)
        else:
            self.fail(f'Type of value not handled. Got={value_type}')
    
    def _test_identifier_expression(self, expression: Expression, value:str) -> None:
        """ test_identifier_expression:
        This function is responsible for testing the identifier expression 
        """
        self.assertIsInstance(expression, Identifier)

        expression = cast(Identifier, expression)     
        self.assertEqual(expression.value, value)
        self.assertEqual(expression.token_literal(), value)   

