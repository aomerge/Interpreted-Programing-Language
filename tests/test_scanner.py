"""Tests for Scanner class."""

import unittest
from unittest.mock import Mock, patch
from src.lexer.scanner import Scanner
from src.lexer.charstream import CharStream
from src.config.token_1 import Token, TokenType


class TestScanner(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures."""
        self.mock_char_stream = Mock(spec=CharStream)
        self.scanner = Scanner(self.mock_char_stream)
    
    def test_init(self):
        """Test Scanner initialization."""
        char_stream = Mock()
        scanner = Scanner(char_stream)
        self.assertEqual(scanner.char_stream, char_stream)
    
    def test_skip_whitespace_and_comments(self):
        """Test skipping whitespace and comments together."""
        with unittest.mock.patch.object(self.scanner, '_skip_whitespace') as mock_whitespace, \
             unittest.mock.patch.object(self.scanner, '_skip_comments') as mock_comments:
            
            self.scanner.skip_whitespace_and_comments()
            
            mock_whitespace.assert_called_once()
            mock_comments.assert_called_once()
    
    def test_skip_whitespace(self):
        """Test skipping whitespace characters."""
        self.scanner._skip_whitespace()
        
        self.mock_char_stream.skip_while.assert_called_once()
        # Verify the lambda function skips whitespace
        skip_func = self.mock_char_stream.skip_while.call_args[0][0]
        self.assertTrue(skip_func(' '))
        self.assertTrue(skip_func('\t'))
        self.assertTrue(skip_func('\r'))
        self.assertTrue(skip_func('\n'))
        self.assertFalse(skip_func('a'))
    
    def test_skip_comments_no_comments(self):
        """Test skip_comments when no comments are present."""
        with unittest.mock.patch.object(self.scanner, '_is_line_comment', return_value=False), \
             unittest.mock.patch.object(self.scanner, '_is_block_comment', return_value=False):
            
            self.scanner._skip_comments()
    
    def test_skip_comments_line_comment(self):
        """Test skipping line comments."""
        with unittest.mock.patch.object(self.scanner, '_is_line_comment', side_effect=[True, False]), \
             unittest.mock.patch.object(self.scanner, '_is_block_comment', return_value=False), \
             unittest.mock.patch.object(self.scanner, '_skip_line_comment') as mock_skip_line:
            
            self.scanner._skip_comments()
            
            mock_skip_line.assert_called_once()
    
    def test_skip_comments_block_comment(self):
        """Test skipping block comments."""
        with unittest.mock.patch.object(self.scanner, '_is_line_comment', return_value=False), \
             unittest.mock.patch.object(self.scanner, '_is_block_comment', side_effect=[True, False]), \
             unittest.mock.patch.object(self.scanner, '_skip_block_comment') as mock_skip_block:
            
            self.scanner._skip_comments()
            
            mock_skip_block.assert_called_once()
    
    def test_is_line_comment_true(self):
        """Test detection of line comment start."""
        self.mock_char_stream.current_char = '/'
        self.mock_char_stream.peek_char = '/'
        
        result = self.scanner._is_line_comment()
        
        self.assertTrue(result)
    
    def test_is_line_comment_false(self):
        """Test non-line-comment detection."""
        self.mock_char_stream.current_char = '/'
        self.mock_char_stream.peek_char = '*'
        
        result = self.scanner._is_line_comment()
        
        self.assertFalse(result)
    
    def test_is_block_comment_true(self):
        """Test detection of block comment start."""
        self.mock_char_stream.current_char = '/'
        self.mock_char_stream.peek_char = '*'
        
        result = self.scanner._is_block_comment()
        
        self.assertTrue(result)
    
    def test_is_block_comment_false(self):
        """Test non-block-comment detection."""
        self.mock_char_stream.current_char = '/'
        self.mock_char_stream.peek_char = '/'
        
        result = self.scanner._is_block_comment()
        
        self.assertFalse(result)
    
    def test_skip_line_comment(self):
        """Test skipping line comment."""
        self.mock_char_stream.current_char = '\n'
        
        self.scanner._skip_line_comment()
        
        # Should read two '/' characters, skip until newline, then read newline
        self.assertEqual(self.mock_char_stream.read_char.call_count, 3)
        self.mock_char_stream.skip_while.assert_called_once()
    
    def test_skip_line_comment_no_newline(self):
        """Test skipping line comment without newline at end."""
        self.mock_char_stream.current_char = ''  # EOF
        
        self.scanner._skip_line_comment()
        
        # Should read two '/' characters and skip until EOF
        self.assertEqual(self.mock_char_stream.read_char.call_count, 2)
        self.mock_char_stream.skip_while.assert_called_once()
    
    def test_skip_block_comment(self):
        """Test skipping block comment."""
        # Mock EOF and character sequence
        eof_calls = [False, False, False, True]  # Not EOF for first 3 calls
        self.mock_char_stream.eof.side_effect = eof_calls
        
        # Mock character sequence: /* ... */
        self.mock_char_stream.current_char = '*'
        self.mock_char_stream.peek_char = '/'
        
        self.scanner._skip_block_comment()
        
        # Should consume initial '/*' and final '*/'
        self.assertEqual(self.mock_char_stream.read_char.call_count, 4)
    
    def test_skip_block_comment_eof(self):
        """Test skipping block comment that reaches EOF."""
        self.mock_char_stream.eof.return_value = True
        
        self.scanner._skip_block_comment()
        
        # Should consume initial '/*' 
        self.assertEqual(self.mock_char_stream.read_char.call_count, 2)
    
    def test_read_identifier_simple(self):
        """Test reading simple identifier using real CharStream."""
        from src.lexer.charstream import CharStream
        real_stream = CharStream("hello")
        scanner = Scanner(real_stream)
        
        result = scanner.read_identifier()
        
        self.assertEqual(result, "hello")
    
    def test_read_identifier_with_underscore(self):
        """Test reading identifier with underscore using real CharStream."""
        from src.lexer.charstream import CharStream
        real_stream = CharStream("_var")
        scanner = Scanner(real_stream)
        
        result = scanner.read_identifier()
        
        self.assertEqual(result, "_var")
    
    def test_read_identifier_with_numbers(self):
        """Test reading identifier with numbers using real CharStream."""
        from src.lexer.charstream import CharStream
        real_stream = CharStream("var123")
        scanner = Scanner(real_stream)
        
        result = scanner.read_identifier()
        
        self.assertEqual(result, "var123")
    
    def test_read_identifier_invalid_start(self):
        """Test reading identifier with invalid starting character."""
        self.mock_char_stream.current_char = '1'
        
        result = self.scanner.read_identifier()
        
        self.assertEqual(result, '')
    
    def test_read_number_simple(self):
        """Test reading simple number using real CharStream."""
        from src.lexer.charstream import CharStream
        real_stream = CharStream("123")
        scanner = Scanner(real_stream)
        
        result = scanner.read_number()
        
        self.assertEqual(result, "123")
    
    def test_read_number_decimal(self):
        """Test reading decimal number using real CharStream."""
        from src.lexer.charstream import CharStream
        real_stream = CharStream("12.5")
        scanner = Scanner(real_stream)
        
        result = scanner.read_number()
        
        self.assertEqual(result, "12.5")
    
    def test_read_string_simple(self):
        """Test reading simple string using real CharStream."""
        from src.lexer.charstream import CharStream
        real_stream = CharStream('"hello"')
        scanner = Scanner(real_stream)
        
        result, closed = scanner.read_string()
        
        self.assertEqual(result, "hello")
        self.assertTrue(closed)
    
    def test_read_string_single_quotes(self):
        """Test reading string with single quotes using real CharStream."""
        from src.lexer.charstream import CharStream
        real_stream = CharStream("'world'")
        scanner = Scanner(real_stream)
        
        result, closed = scanner.read_string()
        
        self.assertEqual(result, "world")
        self.assertTrue(closed)
    
    def test_read_string_with_escape(self):
        """Test reading string with escape sequences using real CharStream."""
        from src.lexer.charstream import CharStream
        real_stream = CharStream(r'"hello\nworld"')
        scanner = Scanner(real_stream)
        
        result, closed = scanner.read_string()
        
        self.assertEqual(result, "hello\nworld")
        self.assertTrue(closed)
    
    def test_read_string_unclosed(self):
        """Test reading unclosed string using real CharStream."""
        from src.lexer.charstream import CharStream
        real_stream = CharStream('"hello')
        scanner = Scanner(real_stream)
        
        result, closed = scanner.read_string()
        
        self.assertEqual(result, "hello")
        self.assertFalse(closed)
    
    def test_handle_escape_sequence_newline(self):
        """Test handling newline escape sequence."""
        self.mock_char_stream.ch = 'n'
        
        result = self.scanner._handle_escape_sequence()
        
        self.assertEqual(result, '\n')
        self.assertEqual(self.mock_char_stream.read_char.call_count, 2)
    
    def test_handle_escape_sequence_tab(self):
        """Test handling tab escape sequence."""
        self.mock_char_stream.ch = 't'
        
        result = self.scanner._handle_escape_sequence()
        
        self.assertEqual(result, '\t')
    
    def test_handle_escape_sequence_quote(self):
        """Test handling quote escape sequence."""
        self.mock_char_stream.ch = '"'
        
        result = self.scanner._handle_escape_sequence()
        
        self.assertEqual(result, '"')
    
    def test_handle_escape_sequence_unknown(self):
        """Test handling unknown escape sequence."""
        self.mock_char_stream.ch = 'x'
        
        result = self.scanner._handle_escape_sequence()
        
        self.assertEqual(result, 'x')  # Returns the character as-is
    
    def test_two_char_if_two_chars(self):
        """Test two_char_if when two characters match."""
        self.mock_char_stream.peek_char = '='
        self.mock_char_stream.ch = '='
        
        result = self.scanner.two_char_if('=', TokenType.EQ, TokenType.ASSIGN, '=')
        
        self.assertEqual(result.type, TokenType.EQ)
        self.assertEqual(result.literal, '==')
        self.assertEqual(self.mock_char_stream.read_char.call_count, 2)
    
    def test_two_char_if_one_char(self):
        """Test two_char_if when only one character matches."""
        self.mock_char_stream.peek_char = 'x'
        
        result = self.scanner.two_char_if('=', TokenType.EQ, TokenType.ASSIGN, '=')
        
        self.assertEqual(result.type, TokenType.ASSIGN)
        self.assertEqual(result.literal, '=')
        self.assertEqual(self.mock_char_stream.read_char.call_count, 1)


if __name__ == '__main__':
    unittest.main()