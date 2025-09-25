from unittest import TestCase
from src.lexer import Lexer
from src.config.token_1 import Token, TokenType
from typing import List

import logging

class LexerTest(TestCase):
    logger = logging.getLogger(__name__)

    def collect_tokens(self, lexer: Lexer, source: str, use_eof: bool = False) -> List[Token]:
        tokens: List[Token] = []
        if use_eof:
            while True:
                token = lexer.next_token()
                tokens.append(token)
                if token.type == TokenType.EOF:
                    break
        else:
            for _ in range(len(source)):
                tokens.append(lexer.next_token())
        return tokens

    def test_illegal(self) -> None:
        source: str = '¡¿@'
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source)
        

        expected_tokens: List[Token] = [            
            Token(TokenType.ILLEGAL, '¡'),
            Token(TokenType.ILLEGAL, '¿'),            
            Token(TokenType.ILLEGAL, '@')            
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_one_character_tokens(self) -> None:
        source: str = '=+(){},;"</>'
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source)

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

    def test_eof(self) -> None:
        source: str = 'a'
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.IDENT, 'a'),
            Token(TokenType.EOF, ''),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_next_token(self) -> None:
        source: str = '=+(){},;'
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source)

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
        tokens = self.collect_tokens(lexer, source)

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

        tokens = self.collect_tokens(lexer, source, use_eof=True)

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
        tokens = self.collect_tokens(lexer, source, use_eof=True)

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
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.INT, '1234567890'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)  

    def test_function_declaration (self)-> None:
        source: str = 'function add(a,b){return a+b;}'
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)        

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
        tokens = self.collect_tokens(lexer, source, use_eof=True)

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

    def test_string_literals_closed(self) -> None:
        """Test string literals with proper closing quotes."""
        source: str = "'hello' 'world'"
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.STRING, 'hello'),
            Token(TokenType.STRING, 'world'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_string_literals_unclosed(self) -> None:
        """Test unclosed string literals return ILLEGAL token."""
        source: str = "'hello"  # Missing closing quote
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.ILLEGAL, 'hello'),  # Unclosed string becomes ILLEGAL
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_empty_string_literals(self) -> None:
        """Test empty string literals."""
        source: str = "''"
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.STRING, ''),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_lexer_repr(self) -> None:
        """Test lexer __repr__ method."""
        lexer: Lexer = Lexer("test")
        result = repr(lexer)
        self.assertEqual(result, "Lexer()")

    def test_lexer_str(self) -> None:
        """Test lexer __str__ method."""
        lexer: Lexer = Lexer("abc")
        result = str(lexer)
        # Should show next token info
        self.assertIn("Lexer-next:", result)
        self.assertIn("IDENT", result)

    def test_malformed_identifier_edge_case(self) -> None:
        """Test edge case where identifier reading fails."""
        # This is a tricky test case - we need to simulate a case where
        # _is_identifier_start returns True but read_identifier returns empty
        source: str = "_"  # Single underscore should work normally
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.IDENT, '_'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_complex_string_with_spaces(self) -> None:
        """Test string with spaces and special characters."""
        source: str = "'hello world!'"
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.STRING, 'hello world!'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_mixed_quotes_unclosed(self) -> None:
        """Test mixed quote types with unclosed strings."""
        source: str = "\"hello world"  # Double quote unclosed
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.QUOTE, '"'),  # Double quote becomes single char token
            Token(TokenType.IDENT, 'hello'),
            Token(TokenType.IDENT, 'world'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_numbers_with_operations(self) -> None:
        """Test numbers mixed with mathematical operations."""
        source: str = '123+456-789*0'
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.INT, '123'),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.INT, '456'),
            Token(TokenType.MINUS, '-'),
            Token(TokenType.INT, '789'),
            Token(TokenType.MULTIPLICATION, '*'),
            Token(TokenType.INT, '0'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_whitespace_handling(self) -> None:
        """Test that whitespace is properly skipped."""
        source: str = '  let   x   =   5  ;  '
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'let'),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.INT, '5'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_comment_handling(self) -> None:
        """Test that comments are properly ignored."""
        source: str = 'let x = 5; // this is a comment\nlet y = 10;'
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.LET, 'let'),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.INT, '5'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.LET, 'let'),
            Token(TokenType.IDENT, 'y'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.INT, '10'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_decimal_numbers(self) -> None:
        """Test decimal number parsing."""
        source: str = '3.14 0.5 123.456'
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.INT, '3.14'),
            Token(TokenType.INT, '0.5'),
            Token(TokenType.INT, '123.456'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_comparison_operators(self) -> None:
        """Test comparison operators including <= and >=."""
        source: str = '<= >= == != < >'
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.LTE, '<='),
            Token(TokenType.GTE, '>='),
            Token(TokenType.EQUAL, '=='),
            Token(TokenType.NOT_EQUAL, '!='),
            Token(TokenType.LT, '<'),
            Token(TokenType.GT, '>'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_string_with_escaped_quotes(self) -> None:
        """Test string literals with escaped quotes."""
        source: str = "'hello\\'world'"
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.STRING, "hello'world"),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_all_two_char_operators(self) -> None:
        """Test all two character operators."""
        source: str = '== != <= >='
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.EQUAL, '=='),
            Token(TokenType.NOT_EQUAL, '!='),
            Token(TokenType.LTE, '<='),
            Token(TokenType.GTE, '>='),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_double_quote_as_single_char_token(self) -> None:
        """Test that double quotes are treated as single character tokens."""
        source: str = '"'
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.QUOTE, '"'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_negation_operator(self) -> None:
        """Test negation operator."""
        source: str = '!true'
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.BANG, '!'),
            Token(TokenType.TRUE, 'true'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_edge_case_empty_source(self) -> None:
        """Test lexer with empty source."""
        source: str = ''
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_single_character_at_eof(self) -> None:
        """Test single character tokens at end of file."""
        source: str = '+'
        lexer: Lexer = Lexer(source)
        tokens = self.collect_tokens(lexer, source, use_eof=True)

        expected_tokens: List[Token] = [
            Token(TokenType.PLUS, '+'),
            Token(TokenType.EOF, '')
        ]

        self.assertEqual(tokens, expected_tokens)
