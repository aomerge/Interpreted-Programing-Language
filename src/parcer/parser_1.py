from src.lexer import Lexer
from typing import (
    Optional, 
    List,
    Callable,
    Dict,
             
)
from src.ast import (
    Program, 
    Statement, 
    LetStatement, 
    Identifier, 
    ReturnStatement, 
    ExpressionStatement, 
    Expression,
    Integer,
    Boolean,
    Function,
    If,
    Prefix,
    Infix,
    StringLiteral,
    Call
)
from src.token_1 import (Token, TokenType)
from enum import IntEnum

prefix_parse_fn = Callable[[], Optional[Statement]]
infix_parse_fn = Callable[[Statement], Optional[Statement]]
prefix_parse_fns = Dict[TokenType, prefix_parse_fn]
infix_parse_fns = Dict[TokenType, infix_parse_fn]


class Precedence(IntEnum):
    LOWEST = 1
    EQUALS = 2
    LESSGREATER = 3
    SUM = 4
    PRODUCT = 5
    PREFIX = 6
    CALL = 7

PRECEDENCES: Dict[TokenType, Precedence] = {
    TokenType.EQUAL: Precedence.EQUALS,
    TokenType.NOT_EQUAL: Precedence.EQUALS,
    TokenType.LT: Precedence.LESSGREATER,
    TokenType.GT: Precedence.LESSGREATER,
    TokenType.PLUS: Precedence.SUM,
    TokenType.MINUS: Precedence.SUM,
    TokenType.DIVISION: Precedence.PRODUCT,
    TokenType.MULTIPLICATION: Precedence.PRODUCT    
}

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
        program = Program(statements=[])

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
    
    def _parse_boolean(self) -> Boolean:
        assert self._current_token is not None

        return Boolean(token=self._current_token,
                       value=self._current_token.token_type == TokenType.TRUE)
    
    def _parse_call(self, function: Expression) -> Call:
        assert self._current_token is not None
        call = Call(self._current_token, function)
        call.arguments = self._parse_call_arguments()

        return call
    
    def _parse_grouped_expression(self) -> Optional[Expression]:
        self._next_token()

        expression = self._parse_expression(Precedence.LOWEST)

        if not self._expected_token(TokenType.RPAREN):
            return None

        return expression
    
    def _parse_prefix_expression(self) -> Prefix:
        assert self._current_token is not None
        prefix_expression = Prefix(token=self._current_token,
                                   operator=self._current_token.literal)

        self._next_token()

        prefix_expression.right = self._parse_expression(Precedence.PREFIX)

        return prefix_expression
    
    def _parse_function(self) -> Optional[Function]:
        assert self._current_token is not None
        function = Function(token=self._current_token)

        if not self._expected_token(TokenType.LPAREN):
            return None

        function.parameters = self._parse_function_parameters()

        if not self._expected_token(TokenType.LBRACE):
            return None

        function.body = self._parse_block()

        return function
    
    def _parse_identifier(self) -> Optional[Statement]:
        assert self._current_token is not None
        return Identifier(token=self._current_token, value=self._current_token.literal)
    
    def _parse_integer(self) -> Optional[Integer]:
        assert self._current_token is not None
        integer = Integer(token=self._current_token)

        try:
            integer.value = int(self._current_token.literal)
        except ValueError:
            message = f'No se ha podido parsear {self._current_token.literal} ' + \
                'como entero.'
            self._errors.append(message)

            return None

        return integer
    
    def _parse_let_statement(self) -> Optional[LetStatement]:
        assert self._current_token is not None

        let_statement = LetStatement(token=self._current_token)

        # Verificamos que el siguiente token sea un identificador (nombre de la variable)
        if not self._expected_tokens(TokenType.IDENT):
            return None

        let_statement.name = self._parse_identifier()

        # Verificamos que el siguiente token sea el signo de asignación (=)
        if not self._expected_tokens(TokenType.ASSIGN):
            return None
        
        # Avanzamos al siguiente token para empezar a parsear la expresión
        self._next_token()

        # Aquí parseamos la expresión que representa el valor de la variable
        let_statement.value = self._parse_Expression(Precedence.LOWEST)

        # Verificamos si hay un punto y coma al final de la declaración
        if self._peek_token.type == TokenType.SEMICOLON:
            self._next_token()

        return let_statement

    def _parse_Expression(self, precedence: Precedence) -> Optional[Expression]:
        assert self._current_token is not None

        prefix_parse_fn = self._prefix_parse_fns.get(self._current_token.type)

        if not prefix_parse_fn:
            message = f'No se encontro ninguna funcion para parsear {self._current_token.literal}'
            self._errors.append(message)
            return None

        print(f"Parsing prefix expression with token: {self._current_token.literal}")
        left_expression = prefix_parse_fn()

        assert self._peek_token is not None
        while not self._peek_token.type == TokenType.SEMICOLON and precedence < self._peek_precedence():
            infix_parse_fn = self._infix_parse_fns.get(self._peek_token.type)
            print(f"Current infix parse function: {infix_parse_fn.__str__()} for token: {self._peek_token.literal}")

            if infix_parse_fn is None:
                break

            self._next_token()
            assert left_expression is not None
            left_expression = infix_parse_fn(left_expression)

        return left_expression

    def _parse_expression_statement(self) -> Optional[ExpressionStatement]:
        assert self._current_token is not None
        expression_statement = ExpressionStatement(token=self._current_token)
        expression_statement.expression = self._parse_Expression(Precedence.LOWEST)

        # if expression_statement.expression is None:
        #     print(f"Error: Se encontró una expresión None en {self._current_token}")
        # else:
        #     print(f"Expresión analizada correctamente: {expression_statement.expression}")

        assert self._peek_token is not None
        if self._peek_token.type == TokenType.SEMICOLON:
            self._next_token()

        return expression_statement
    
    def _parese_identifier(self) -> Identifier:
        assert self._current_token is not None
        return Identifier(token=self._current_token, value=self._current_token.literal)        
    
    def _parse_if(self) -> Optional[If]:
        assert self._current_token is not None
        if_expression = If(token=self._current_token)

        if not self._expected_token(TokenType.LPAREN):
            return None

        self._next_token()

        if_expression.condition = self._parse_expression(Precedence.LOWEST)

        if not self._expected_token(TokenType.RPAREN):
            return None

        if not self._expected_token(TokenType.LBRAKET):
            return None

        if_expression.consequence = self._parse_block()

        assert self._peek_token is not None
        if self._peek_token.token_type == TokenType.ELSE:
            self._next_token()

            if not self._expected_token(TokenType.LBRACE):
                return None

            if_expression.alternative = self._parse_block()

        return if_expression
    def _parse_infix_expression(self, left: Expression) -> Infix:
        assert self._current_token is not None
        infix = Infix(token=self._current_token,
                      operator=self._current_token.literal,
                      left=left)

        precedence = self._peek_precedence()

        self._next_token()

        infix.right = self._parse_Expression(precedence)
        if infix.right is None:
            self._errors.append(f"Se esperaba una expresión a la derecha del operador {self._current_token.literal}")
            print(f"Error: Se esperaba una expresión a la derecha del operador {self._current_token.literal}")

        return infix
    
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
        
    def _parse_string_literal(self) -> Expression:
        assert self._current_token is not None
        return StringLiteral(token=self._current_token,
                             value=self._current_token.literal)
    
    def _peek_precedence(self) -> Precedence:
        assert self._peek_token is not None
        try:
            return PRECEDENCES[self._peek_token.type]
        except KeyError:
            return Precedence.LOWEST

    def _parse_return_statement(self) -> ReturnStatement:
        statement = ReturnStatement(token=self._current_token)
        print(f"El valor de self._current_token es {self._current_token}")
        self._next_token()
        statement.return_value = self._parse_Expression(Precedence.LOWEST)
        print(f"El valor de statement.return_value es {statement.return_value}")
        if self._peek_token.type == TokenType.SEMICOLON:
            self._next_token()        
        return statement

    def _peek_error(self, token_type: TokenType) -> None:
        assert self._peek_token is not None
        self._errors.append(f'expected next token to be {token_type}, got {self._peek_token.type} instead')
    
    def _register_infix_fns(self) -> infix_parse_fns:
        return {
            TokenType.PLUS: self._parse_infix_expression,
            TokenType.MINUS: self._parse_infix_expression,            
            TokenType.DIVISION: self._parse_infix_expression,
            TokenType.MULTIPLICATION: self._parse_infix_expression,
            TokenType.EQUAL: self._parse_infix_expression,
            TokenType.NOT_EQUAL: self._parse_infix_expression,
            TokenType.LT: self._parse_infix_expression,
            TokenType.GT: self._parse_infix_expression,
            TokenType.LPAREN: self._parse_call,
        }

    def _register_prefix_fns(self) -> infix_parse_fns:
        return {
            TokenType.FALSE: self._parse_boolean,
            TokenType.FUNCTION: self._parse_function,
            TokenType.IDENT: self._parse_identifier,
            TokenType.CONDITIONAL: self._parse_if,
            TokenType.INT: self._parse_integer,
            TokenType.LPAREN: self._parse_grouped_expression,            
            TokenType.NEGATION: self._parse_prefix_expression,
            TokenType.TRUE: self._parse_boolean,
            TokenType.STRING: self._parse_string_literal
        }
    
    def __str__(self) -> str:
        return f'Parser: current_token={self._current_token}, peek_token={self._peek_token}'
