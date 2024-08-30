from unittest import TestCase
from src.lexer import Lexer
from src.token_1 import Token, TokenType
from typing import List

import logging

class LexerTest(TestCase):
    logger = logging.getLogger(__name__)

    def test_illegal(self) -> None:
        source: str = '¡¿@'
        lexer: Lexer = Lexer(source)        
        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())        

        expected_tokens: List[Token] = [            
            Token(TokenType.ILLEGAL, '¡'),
            Token(TokenType.ILLEGAL, '¿'),            
            Token(TokenType.ILLEGAL, '@')            
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_one_character_tokens(self) -> None:
        source: str = '=+(){},;"</>'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.QUOTE, '"'),
            Token(TokenType.LT, '<'),            
            Token(TokenType.DIVISION, '/'),
            Token(TokenType.GT, '>'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def tetst_eof(self) -> None:
        source: str = 'a'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.IDENT, 'a'),
            Token(TokenType.EOF, ''),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_next_token(self) -> None:
        source: str = '=+(){},;'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_two_character_tokens(self) -> None:
        source: str = '==!=<>'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.EQUAL, '=='),
            Token(TokenType.NOT_EQUAL, '!='),
            Token(TokenType.LT, '<'),
            Token(TokenType.GT, '>'),
            Token(TokenType.EOF, ''),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_identifiers(self) -> None:
        source: str = 'foobar Foobar_ _fOobar'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        while True:
            token = lexer.next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break

        expected_tokens: List[Token] = [
            Token(TokenType.IDENT, 'foobar'),            
            Token(TokenType.IDENT, 'Foobar_'),            
            Token(TokenType.IDENT, '_fOobar'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_keywords(self) -> None:
        source: str = 'let function if else return true false' 
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        while True:
            token = lexer.next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'let'),            
            Token(TokenType.FUNCTION, 'function'),
            Token(TokenType.CONDITIONAL, 'if'),
            Token(TokenType.IDENT, 'else'),
            Token(TokenType.RETURN, 'return'),
            Token(TokenType.TRUE, 'true'),
            Token(TokenType.FALSE, 'false'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_integers(self) -> None:
        source: str = '1234567890'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        while True:
            token = lexer.next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break

        expected_tokens: List[Token] = [
            Token(TokenType.INT, '1234567890'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)  

    def test_function_declaration (self)-> None:
        source: str = 'function add(a,b){return a+b;}'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        while True:
            token = lexer.next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break

        expected_tokens: List[Token] = [
            Token(TokenType.FUNCTION, 'function'),
            Token(TokenType.IDENT, 'add'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENT, 'a'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.IDENT, 'b'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RETURN, 'return'),
            Token(TokenType.IDENT, 'a'),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.IDENT, 'b'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_class_declaration (self) -> None:
        source: str = '''
        class Person {
            let name; 
            let age; 
            public sayName(){
                return name;
                } 
            public sayAge(){
                return age;
                }
            }
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []    
        while True:
            token = lexer.next_token()
            tokens.append(token)
            if token.type == TokenType.EOF:
                break

        expected_tokens: List[Token] = [
            Token(TokenType.CLASS, 'class'),
            Token(TokenType.IDENT, 'Person'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.LET, 'let'),
            Token(TokenType.IDENT, 'name'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.LET, 'let'),
            Token(TokenType.IDENT, 'age'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.PUBLIC, 'public'),
            Token(TokenType.IDENT, 'sayName'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RETURN, 'return'),
            Token(TokenType.IDENT, 'name'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.PUBLIC, 'public'),
            Token(TokenType.IDENT, 'sayAge'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RETURN, 'return'),
            Token(TokenType.IDENT, 'age'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)    
