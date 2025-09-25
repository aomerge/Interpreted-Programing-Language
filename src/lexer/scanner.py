from typing import Tuple
from .charstream import CharStream
from src.config.token_1 import TokenType, Token


class Scanner:
    """
    Funciones de escaneo de lexemas (números, identificadores, strings, espacios, comentarios, etc.).
    No decide qué TokenType devolver ante un signo: eso lo hará el Lexer.
    """

    def __init__(self, char_stream: CharStream) -> None:
        self.char_stream = char_stream

    def skip_whitespace_and_comments(self) -> None:
        """
        Salta espacios en blanco y comentarios (de línea y de bloque).
        """
        self._skip_whitespace()
        self._skip_comments()

    def _skip_whitespace(self) -> None:
        """
        Salta caracteres de espacio en blanco.
        """
        self.char_stream.skip_while(lambda char: char in " \t\r\n")

    def _skip_comments(self) -> None:
        """
        Salta comentarios de línea (//...) y de bloque (/* ... */).
        """
        while True:
            if self._is_line_comment():
                self._skip_line_comment()
            elif self._is_block_comment():
                self._skip_block_comment()
            else:
                break

    def _is_line_comment(self) -> bool:
        return self.char_stream.current_char == "/" and self.char_stream.peek_char == "/"

    def _is_block_comment(self) -> bool:
        return self.char_stream.current_char == "/" and self.char_stream.peek_char == "*"

    def _skip_line_comment(self) -> None:
        """
        Salta un comentario de línea (//...).
        """
        self.char_stream.read_char()  # consumir '/'
        self.char_stream.read_char()  # consumir '/'
        self.char_stream.skip_while(lambda char: char not in ("\n", ""))
        if self.char_stream.current_char == "\n":
            self.char_stream.read_char()

    def _skip_block_comment(self) -> None:
        """
        Salta un comentario de bloque (/* ... */).
        """
        self.char_stream.read_char()  # consumir '/'
        self.char_stream.read_char()  # consumir '*'
        while not self.char_stream.eof():
            if self.char_stream.current_char == "*" and self.char_stream.peek_char == "/":
                self.char_stream.read_char()  # consumir '*'
                self.char_stream.read_char()  # consumir '/'
                break
            self.char_stream.read_char()

    def read_identifier(self) -> str:
        """
        Lee un identificador. Regla: primer char [A-Za-z_], siguientes [A-Za-z0-9_].
        """
        identifier = ""
        if self.char_stream.current_char.isalpha() or self.char_stream.current_char == "_":
            while self.char_stream.current_char.isalnum() or self.char_stream.current_char == "_":
                identifier += self.char_stream.current_char
                self.char_stream.read_char()
        return identifier

    def read_number(self) -> str:
        """
        Lee un número (entero o decimal). No valida exponentes.
        """
        number = ""
        has_dot = False
        while self.char_stream.current_char.isdigit() or (self.char_stream.current_char == "." and not has_dot):
            if self.char_stream.current_char == ".":
                has_dot = True
            number += self.char_stream.current_char
            self.char_stream.read_char()
        return number

    def read_string(self) -> Tuple[str, bool]:
        """
        Lee un literal de cadena entre comillas dobles "..." o simples '...'.
        Devuelve (literal, cerrado_correctamente).
        Admite escapes básicos: \" y \'.
        """
        quote = self.char_stream.current_char
        assert quote in ("'", '"')
        self.char_stream.read_char()  # consumir comilla inicial

        buffer = []
        closed = False

        while not self.char_stream.eof():
            current_char = self.char_stream.current_char
            if current_char == "\\":
                buffer.append(self._handle_escape_sequence())
            elif current_char == quote:
                closed = True
                self.char_stream.read_char()  # consumir comilla de cierre
                break
            else:
                buffer.append(current_char)
                self.char_stream.read_char()

        return "".join(buffer), closed

    def _handle_escape_sequence(self) -> str:
        """
        Maneja secuencias de escape dentro de cadenas.
        """
        self.char_stream.read_char()  # consumir '\'
        escape_char = self.char_stream.ch
        escape_map = {
            "n": "\n",
            "t": "\t",
            "r": "\r",
            '"': '"',
            "'": "'",
            "\\": "\\",
        }
        self.char_stream.read_char()
        return escape_map.get(escape_char, escape_char)

    def two_char_if(self, expected_second: str, tok_if_two: TokenType, tok_if_one: TokenType, literal_one: str) -> Token:
        """
        Maneja tokens de uno o dos caracteres según el siguiente carácter.
        """
        if self.char_stream.peek_char == expected_second:
            first_char = self.char_stream.ch
            self.char_stream.read_char()
            literal = first_char + self.char_stream.ch
            self.char_stream.read_char()
            return Token(tok_if_two, literal)
        else:
            literal = literal_one
            self.char_stream.read_char()
            return Token(tok_if_one, literal)
