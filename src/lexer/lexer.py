from typing import Final, Optional
from src.config.token_1 import Token, TokenType
from src.lexer.charstream import CharStream
from src.lexer.scanner import Scanner
from src.lexer.keywords import lookup_ident


class Lexer:
    """
    Orquesta el proceso de tokenización.

    Delegación:
      - CharStream: lectura de caracteres (actual/peek/avance).
      - Scanner: escaneo de lexemas (identificadores, números, strings, espacios/comentarios).
    """

    # --- Constantes para evitar literales mágicos ---
    _EMPTY: Final[str] = ""
    _DOUBLE_QUOTE: Final[str] = '"'
    _SINGLE_QUOTE: Final[str] = "'"

    # Mapeo de tokens de un solo carácter (fácil de extender/leer)
    _SINGLE_CHAR_TOKEN_MAP: Final[dict[str, TokenType]] = {
        "+": TokenType.PLUS,
        "-": TokenType.MINUS,
        "*": TokenType.MULTIPLICATION,
        "/": TokenType.DIVISION,
        "(": TokenType.LPAREN,
        ")": TokenType.RPAREN,
        "{": TokenType.LBRACE,
        "}": TokenType.RBRACE,
        ",": TokenType.COMMA,
        ";": TokenType.SEMICOLON,
        '"': TokenType.QUOTE,
        "<": TokenType.LT,
        ">": TokenType.GT,
        # Si realmente desea mapear barra invertida (\):
        # "\\": TokenType.BACKSLASH,
        # Si desea mapear el signo de dólar ($) a algún token:
        # "$": TokenType.DOLLAR,
    }

    def __init__(self, source: str) -> None:
        self.char_stream: CharStream = CharStream(source)
        self.scanner: Scanner = Scanner(self.char_stream)

    # ------------------------------------------------------------------ #
    # API pública
    # ------------------------------------------------------------------ #
    def next_token(self) -> Token:
        """
        Devuelve el siguiente token del flujo de entrada.
        """
        self.scanner.skip_whitespace_and_comments()

        current_char: str = self.char_stream.ch
        if current_char == self._EMPTY:
            return Token(TokenType.EOF, "")

        # Identificadores / palabras clave
        if self._is_identifier_start(current_char):
            identifier: str = self.scanner.read_identifier()
            if not identifier:
                # Caso raro: no se pudo leer ident; consumimos y marcamos ilegal
                self.char_stream.read_char()
                return Token(TokenType.ILLEGAL, current_char)
            return Token(lookup_ident(identifier), identifier)

        # Números
        if current_char.isdigit():
            number_literal: str = self.scanner.read_number()
            return Token(TokenType.INT, number_literal)

        # Operadores de dos caracteres: ==, !=, <=, >=
        two_char_token: Optional[Token] = self._try_two_char_operator(current_char)
        if two_char_token is not None:
            return two_char_token

        # Operadores / símbolos de un carácter (incluyendo comillas)
        if current_char in self._SINGLE_CHAR_TOKEN_MAP:
            return self._emit_single_char_token(current_char)

        # Strings (solo si no es una comilla individual)
        if current_char in (self._SINGLE_QUOTE,):  # Removemos DOUBLE_QUOTE de aquí
            string_literal, closed = self.scanner.read_string()
            if not closed:
                # Cadena sin cierre: señalamos ILLEGAL con el literal leído
                return Token(TokenType.ILLEGAL, string_literal)
            return Token(TokenType.STRING, string_literal)

        # Carácter desconocido/ilegal
        illegal = Token(TokenType.ILLEGAL, current_char)
        self.char_stream.read_char()
        return illegal

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        # Solo muestra el siguiente token (no consuma en bucle aquí).
        next_tok = self.next_token()
        return f"{self.__class__.__name__}-next: {next_tok}"

    # ------------------------------------------------------------------ #
    # Helpers privados (legibles y testeables)
    # ------------------------------------------------------------------ #
    def _emit_single_char_token(self, char: str) -> Token:
        """
        Emite un token de un solo carácter y avanza el flujo.
        """
        token_type = self._SINGLE_CHAR_TOKEN_MAP[char]
        token = Token(token_type, char)
        self.char_stream.read_char()
        return token

    def _try_two_char_operator(self, char: str) -> Optional[Token]:
        """
        Intenta formar un operador de dos caracteres a partir del carácter actual.
        Si procede, consume ambos; si no, no consume nada y devuelve None.
        """
        if char == "=":
            # '==' o '='
            return self.scanner.two_char_if("=", TokenType.EQUAL, TokenType.ASSIGN, "=")
        if char == "!":
            # '!=' o '!'
            return self.scanner.two_char_if("=", TokenType.NOT_EQUAL, TokenType.BANG, "!")
        if char == "<":
            # '<=' o '<'
            return self.scanner.two_char_if("=", TokenType.LTE, TokenType.LT, "<")
        if char == ">":
            # '>=' o '>'
            return self.scanner.two_char_if("=", TokenType.GTE, TokenType.GT, ">")
        return None

    @staticmethod
    def _is_identifier_start(char: str) -> bool:
        """
        Regla estándar: primer carácter de un identificador debe ser letra o '_'.
        (Los dígitos pueden aparecer a partir del segundo carácter; lo maneja read_identifier()).
        """
        return char.isalpha() or char == "_"
