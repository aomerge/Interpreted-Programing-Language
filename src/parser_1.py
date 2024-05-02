from src.lexer import Lexer
from typing import (
    Optional, 
    List,
    Callable,
    Dict           
)
from src.ast import (
    Program, 
    Statement, 
    LetStatement, 
    Identifier, 
    ReturnStatement, 
    ExpressionStatement, 
    Expression,
    Integer
)
from src.token_1 import (Token, TokenType)

prefix_parse_fn = Callable[[], Optional[Statement]]
infix_parse_fn = Callable[[Statement], Optional[Statement]]
prefix_parse_fns = Dict[TokenType, prefix_parse_fn]
infix_parse_fns = Dict[TokenType, infix_parse_fn]

class Parser:
    
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer        
        self._current_token:Optional[Token]  = None
        self._peek_token:Optional[Token] = None
        self._errors: List[str] = []
        self._prefix_parse_fns: prefix_parse_fns = self._register_prefix_fns()
        self._infix_parse_fns: infix_parse_fns = self._register_infix_fns()
        self._next_token()
        self._next_token()
    
    @property
    def errors(self) -> List[str]:
        return self._errors
    def getProgram(self) -> Program:
        program: Program = Program(statements=[])

        assert self._current_token is not None

        while self._current_token.type != TokenType.EOF:
            statement = self._parce_statement()
            if statement is not None:
                program.statements.append(statement)
            self._next_token()

        return program
    
    def _next_token(self) -> None:
        self._current_token = self._peek_token
        self._peek_token = self.lexer.next_token()

    def _expected_tokens(self, token_type: TokenType) -> bool:
        assert self._current_token is not None
        if self._peek_token.type == token_type:
            self._next_token()
            return True
        self._peek_error(token_type)
        return False
    
    def _parse_identifier(self) -> Optional[Statement]:
        assert self._current_token is not None
        return Identifier(token=self._current_token, value=self._current_token.literal)
    
    def _parse_let_statement(self) -> Optional[Statement]:
        assert self._current_token is not None

        let_statement = LetStatement(token=self._current_token)

        if not self._expected_tokens(TokenType.IDENT):
            return None

        let_statement.name = self._parse_identifier()

        if not self._expected_tokens(TokenType.ASSIGN):
            return None
        
        while self._current_token.type != TokenType.SEMICOLON:
            self._next_token()
        
        return let_statement

    def _parse_Expression(self) -> Optional[Expression]:
        assert self._current_token is not None
        try:
            prefix_parse_fn = self._prefix_parse_fns[self._current_token.type]
        except KeyError:
            return None
        left_expression = prefix_parse_fn()
        return left_expression
        
    def _parse_expression_statement(self) -> Optional[ExpressionStatement]:
        assert self._current_token is not None
        expression_statement = ExpressionStatement(token=self._current_token)
        expression_statement.expression = self._parse_Expression()

        assert self._peek_token is not None
        if self._peek_token.type == TokenType.SEMICOLON:
            self._next_token()

        return expression_statement
    
    def _parese_identifier(self) -> Identifier:
        assert self._current_token is not None
        return Identifier(token=self._current_token, value=self._current_token.literal)        
    
    def _parse_integer_literal(self) -> Optional[Integer]:
        assert self._current_token is not None
        integer = Integer(token=self._current_token)

        try:
            integer.value = int(self._current_token.literal)
        except ValueError:
            self._errors.append(f'could not parse {self._current_token.literal} as integer')
            return None
        
        return integer

    def _parce_statement(self) -> Optional[Statement]:
        if self._current_token.type == TokenType.LET:
            return self._parse_let_statement()
        elif self._current_token.type == TokenType.RETURN:
            return self._parse_return_statement()
        else:
            return self._parse_expression_statement()

    def _parse_return_statement(self) -> Optional[Statement]:
        assert self._current_token is not None
        return_Statement = ReturnStatement(token=self._current_token)
        self._next_token()

        while self._current_token.type != TokenType.SEMICOLON:
            self._next_token()

        return return_Statement

    def _peek_error(self, token_type: TokenType) -> None:
        assert self._peek_token is not None
        self._errors.append(f'expected next token to be {token_type}, got {self._peek_token.type} instead')
    
    def _register_prefix_fns(self) -> prefix_parse_fns:
        return {
            TokenType.IDENT: self._parse_identifier,
            TokenType.LET: self._parse_let_statement,
            TokenType.RETURN: self._parse_return_statement,
            TokenType.INT: self._parse_integer_literal
        }
    
    def _register_infix_fns(self) -> infix_parse_fns:
        return {}
    
    def __str__(self) -> str:
        return f'Parser: current_token={self._current_token}, peek_token={self._peek_token}'
