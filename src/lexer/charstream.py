from dataclasses import dataclass
from typing import Callable

_SENTINEL = ""  # Fin de archivo (EOF)

@dataclass
class SourcePos:
    """Representa la posición actual en el flujo de caracteres."""
    index: int = 0  # Índice global en la cadena
    line: int = 1   # Línea actual
    col: int = 0    # Columna actual

class CharStream:
    """
    Abstracción para la lectura de caracteres con seguimiento de posición.
    No interpreta tokens; solo entrega el carácter actual y permite mirar el siguiente.
    """
    def __init__(self, source: str) -> None:
        self._source = source or ""
        self._length = len(self._source)
        self._position = SourcePos()
        self._read_position = 0
        self._current_char = _SENTINEL
        self._initialize_stream()

    @property
    def current_char(self) -> str:
        """Devuelve el carácter actual."""
        return self._current_char

    @property
    def ch(self) -> str:
        """Alias para current_char para compatibilidad."""
        return self._current_char

    @property
    def peek_char(self) -> str:
        """Devuelve el siguiente carácter sin avanzar el flujo."""
        if self._read_position >= self._length:
            return _SENTINEL
        return self._source[self._read_position]

    def read_char(self) -> None:
        """Método público para avanzar al siguiente carácter."""
        self._read_next_char()

    def eof(self) -> bool:
        """Alias para is_eof para compatibilidad."""
        return self.is_eof()

    def _initialize_stream(self) -> None:
        """Inicializa el flujo leyendo el primer carácter."""
        self._read_next_char()

    def _read_next_char(self) -> None:
        """Lee el siguiente carácter y actualiza la posición."""
        if self._read_position >= self._length:
            self._current_char = _SENTINEL
        else:
            self._current_char = self._source[self._read_position]

        self._update_position()
        self._read_position += 1

    def _update_position(self) -> None:
        """Actualiza la posición global, línea y columna."""
        self._position.index = self._read_position
        if self._current_char == "\n":
            self._position.line += 1
            self._position.col = 0
        else:
            self._position.col += 1

    def is_eof(self) -> bool:
        """Indica si se alcanzó el final del flujo."""
        return self._current_char == _SENTINEL

    def skip_while(self, predicate: Callable[[str], bool]) -> None:
        """
        Avanza en el flujo mientras el carácter actual cumpla con el predicado.

        Args:
            predicate (Callable[[str], bool]): Función que evalúa el carácter actual.
        """
        while not self.is_eof() and predicate(self._current_char):
            self._read_next_char()
