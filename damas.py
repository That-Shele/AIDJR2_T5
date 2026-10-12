"""Punto de entrada del juego de damas."""

from checkers import Ficha, InteligenciaArtificial, Position, Tablero
from checkers.pygame_ui import Juego

__all__ = ["Ficha", "InteligenciaArtificial", "Juego", "Position", "Tablero"]


if __name__ == "__main__":
    Juego().ejecutar()
