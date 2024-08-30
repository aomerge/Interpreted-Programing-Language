## imports
from src.token_1 import Token, TokenType 
#from token_1 import Token, TokenType 
from re import match

## lexer class
class Lexer :
    """Lexer class: 
    This class is responsible for reading the source code and returning tokens
    """
    def __init__(self, source: str) -> None:
        self.source: str =  source
        self._character = ''
        self._read_position: int = 0
        self._position: int = 0        
        self._read_char()

    def next_token(self) -> Token:  
        """ next_token: 
        This function is responsible for reading the source code and returning tokens
        """
        self._skip_whitespace()      

        if self._character == '=':
            if self._peek_char() == '=':
                char = self._character
                self._read_char()
                token = Token(TokenType.EQUAL, char + self._character)
            else:
                token = Token(TokenType.ASSIGN, '=')     
        elif self._character == '>':
            if self._peek_char() == '=':
                char = self._character
                self._read_char()
                token = Token(TokenType.GTE, char + self._character)
            else:
                token = Token(TokenType.GT, self._character)
        elif self._character == '<':
            if self._peek_char() == '=':
                char = self._character
                self._read_char()
                token = Token(TokenType.LTE, char + self._character)
            else:
                token = Token(TokenType.LT, self._character)
        elif self._character.isalpha() or self._character == '_':
            literal = self._read_identifier()
            token_type = self._lookup_ident(literal)
            return Token(token_type, literal)
        elif self._character.isdigit():
            literal = self._read_number()
            return Token(TokenType.INT, literal)
        elif match(r'^\+$', self._character):
            token = Token(TokenType.PLUS, self._character)
        elif match(r'^\-$', self._character):
            token = Token(TokenType.MINUS, self._character)
        elif match(r'^\*$', self._character):
            token = Token(TokenType.MULTIPLICATION, self._character)
        elif self._character == '':            
            return Token(TokenType.EOF, '')
        elif match(r'^\($', self._character):
            token = Token(TokenType.LPAREN, self._character)
        elif match(r'^\)$', self._character):
            token = Token(TokenType.RPAREN, self._character)
        elif match(r'^{$', self._character):
            token = Token(TokenType.LBRACE, self._character)
        elif match(r'^}$', self._character):
            token = Token(TokenType.RBRACE, self._character)
        elif match(r'^,$', self._character):
            token = Token(TokenType.COMMA, self._character)
        elif match(r'^"$', self._character):
            token = Token(TokenType.QUOTE, self._character)
        elif match(r"^'$", self._character):
            token = Token(TokenType.QUOTE, self._character)
        elif match(r'^;$', self._character):
            token = Token(TokenType.SEMICOLON, self._character)
        elif match(r'^/$', self._character):
            token = Token(TokenType.DIVISION, self._character)
        elif match(r'^\$', self._character):
            token = Token(TokenType.BACKSLASH, self._character)
        elif match(r'^\!$', self._character):
            if self._peek_char() == '=':
                token = self._make_two_character_token(TokenType.NOT_EQUAL)
            else:
                token = Token(TokenType.NOT_EQUAL, self._character)
        else:
            token = Token(TokenType.ILLEGAL, self._character)
        
        self._read_char()

        return token
    ## creamos la funcion para leer numeros y los añadimos a un string
    def _read_number(self) -> str:
        number_str = ''
        while self._character.isdigit() or self._character == '.':
            number_str += self._character
            self._read_char()
        return number_str
    
    def _read_char(self) -> None:
        if self._read_position >= len(self.source):
            self._character = ''              
        else:
            self._character = self.source[self._read_position]        
        self._position = self._read_position
        self._read_position += 1

    def _peek_char(self):
        if self._read_position >= len(self.source):
            return ''
        else:
            return self.source[self._read_position]
        
    def _read_identifier(self):
        number_str = ''
        while self._character.isalpha() or self._character == '_':
            number_str += self._character
            self._read_char()
        return number_str
    
    def _lookup_ident(self, ident):
        keywords = {
            'let': TokenType.LET,
            'function': TokenType.FUNCTION,
            'return': TokenType.RETURN,
            'if': TokenType.CONDITIONAL,
            'class': TokenType.CLASS,
            'for': TokenType.LOOP,
            'public': TokenType.PUBLIC,
            'protected': TokenType.PROTECTED,
            'private': TokenType.PRIVATE,
            'static': TokenType.STATIC,
            'abstract': TokenType.ABSTRACT,
            'extends': TokenType.EXTENDS,
            'while': TokenType.LOOP,
            'in': TokenType.IN,
            'const': TokenType.CONST,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'self': TokenType.SELF,
            'super': TokenType.SUPER,
            'namespaces': TokenType.NAMESPACES,
            'and': TokenType.AND,            
            'or': TokenType.OR,
            'not': TokenType.NOT_EQUAL,            
            '!=': TokenType.NOT_EQUAL,            
            '<=': TokenType.LessThan,
            '>=': TokenType.GreaterThan,            
            '-': TokenType.MINUS,
            'extends': TokenType.EXTENDS,
            'href': TokenType.STRING,
        }
        return keywords.get(ident, TokenType.IDENT)
        
    def _skip_whitespace(self):
        while match(r'^\s$', self._character):
            self._read_char()
    
    def _make_two_character_token(self, token_type: TokenType) -> Token:
        char = self._character
        self._read_char()        
        return Token(token_type,f'{char}{self._character}')

    def __repr__(self) -> str:
        return f"Lexer({self.source})"
    
    def __str__(self) -> str:
        token = self.next_token()
        return f"lexer:{self.source}, {token}"


## example of use of the lexer
input: str = '''
            5 == 5;
        '''
lexer = Lexer(input)
token = lexer.next_token()
while token.type != TokenType.EOF:
    print(f"Token Type: {token.type}, Literal: {token.literal}")
    token = lexer.next_token()
