"""
Módulo AST modular.

Este módulo contiene todas las definiciones de nodos del AST organizadas
en submódulos especializados.
"""

# Importar clases base
from .astNode import ASTNode, Statement, Expression, Program

# Importar expresiones
from .expression import (
    Identifier, Integer, Prefix, Infix, Boolean,
    If, Function, Call, StringLiteral
)

# Importar declaraciones
from .statement import (
    LetStatement, ReturnStatement, ExpressionStatement, Block
)

# Exportar todas las clases para compatibilidad
__all__ = [
    # Clases base
    'ASTNode', 'Statement', 'Expression', 'Program',
    
    # Expresiones
    'Identifier', 'Integer', 'Prefix', 'Infix', 'Boolean',
    'If', 'Function', 'Call', 'StringLiteral',
    
    # Declaraciones
    'LetStatement', 'ReturnStatement', 'ExpressionStatement', 'Block'
]