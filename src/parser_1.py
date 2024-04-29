from src.lexer import Lexer
from typing import Optional
from src.ast import (Program, Statement, LetStatement, Identifier)
from src.token_1 import (Token, TokenType)

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer = lexer        
        self.current_token:Optional[Token]  = None
        self._peek_token:Optional[Token] = None

        self._next_token()
        self._next_token()

    def getProgram(self) -> Program:
        program: Program = Program(statements=[])

        assert self.current_token is not None

        while self.current_token.type != TokenType.EOF:
            statement = self._parce_statement()
            if statement is not None:
                program.statements.append(statement)
            self._next_token()

        return program
    
    def _next_token(self) -> None:
        self.current_token = self._peek_token
        self._peek_token = self.lexer.next_token()

    def _expected_tokens(self, token_type: TokenType) -> bool:
        assert self.current_token is not None
        if self._peek_token.type == token_type:
            self._next_token()
            return True
        
        return False
    
    def _parse_let_statement(self) -> Optional[Statement]:
        assert self.current_token is not None

        let_statement = LetStatement(token=self.current_token)

        if not self._expected_tokens(TokenType.IDENT):
            return None

        let_statement.name = Identifier(token=self.current_token, value=self.current_token.literal)

        if not self._expected_tokens(TokenType.ASSIGN):
            return None
        
        while self.current_token.type != TokenType.SEMICOLON:
            self._next_token()
        
        return let_statement
    
    def _parce_statement(self) -> Optional[Statement]:
        if self.current_token.type == TokenType.LET:
            return self._parse_let_statement()
        else:
            return None