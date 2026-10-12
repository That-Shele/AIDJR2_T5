"""Core de dominio y casos de uso para el juego de damas."""

from .application import InteligenciaArtificial
from .domain import Ficha, Move, MovesByOrigin, Position, Tablero

__all__ = [
    "Ficha",
    "InteligenciaArtificial",
    "Move",
    "MovesByOrigin",
    "Position",
    "Tablero",
]
