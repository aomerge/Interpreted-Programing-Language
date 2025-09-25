# Importa su TokenType real
from src.config.token_1 import TokenType  # ajuste el import a su proyecto

# Solo palabras clave/booleanos; NO operadores aquí
KEYWORDS = {
    "let": TokenType.LET,
    "function": TokenType.FUNCTION,
    "return": TokenType.RETURN,
    "if": TokenType.CONDITIONAL,
    "while": TokenType.LOOP,
    "for": TokenType.LOOP,
    "class": TokenType.CLASS,
    "public": TokenType.PUBLIC,
    "protected": TokenType.PROTECTED,
    "private": TokenType.PRIVATE,
    "static": TokenType.STATIC,
    "abstract": TokenType.ABSTRACT,
    "extends": TokenType.EXTENDS,
    "in": TokenType.IN,
    "const": TokenType.CONST,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "self": TokenType.SELF,
    "super": TokenType.SUPER,
    "namespaces": TokenType.NAMESPACES,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "href": TokenType.STRING,  # si en su lenguaje 'href' es palabra reservada
}

def lookup_ident(literal: str) -> TokenType:
    return KEYWORDS.get(literal, TokenType.IDENT)
