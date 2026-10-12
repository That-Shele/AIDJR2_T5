"""Entidades y reglas puras del juego de damas."""

from copy import deepcopy
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

BOARD_DIMENSION = 8
Position = Tuple[int, int]
Move = Tuple[Position, Optional[Position]]
MovesByOrigin = Dict[Position, List[Move]]


@dataclass
class Ficha:
    """Una ficha perteneciente a un jugador."""

    jugador: int
    coronada: bool = False


class Tablero:
    """Contiene el estado y las reglas, sin depender de la interfaz gráfica."""

    def __init__(self) -> None:
        self.casillas: List[List[Optional[Ficha]]] = [
            [None for _ in range(BOARD_DIMENSION)] for _ in range(BOARD_DIMENSION)
        ]
        self.reiniciar()

    def reiniciar(self) -> None:
        """Crea la posicion inicial de una partida."""
        for fila in range(BOARD_DIMENSION):
            for columna in range(BOARD_DIMENSION):
                self.casillas[fila][columna] = None

        for fila in range(3):
            for columna in range(BOARD_DIMENSION):
                if self.es_jugable((fila, columna)):
                    self.casillas[fila][columna] = Ficha(2)

        for fila in range(5, BOARD_DIMENSION):
            for columna in range(BOARD_DIMENSION):
                if self.es_jugable((fila, columna)):
                    self.casillas[fila][columna] = Ficha(1)

    def clonar(self) -> "Tablero":
        """Crea una copia independiente para analizar jugadas de la IA."""
        copia = Tablero.__new__(Tablero)
        copia.casillas = deepcopy(self.casillas)
        return copia

    @staticmethod
    def es_jugable(posicion: Position) -> bool:
        fila, columna = posicion
        return (fila + columna) % 2 == 1

    @staticmethod
    def dentro(posicion: Position) -> bool:
        fila, columna = posicion
        return 0 <= fila < BOARD_DIMENSION and 0 <= columna < BOARD_DIMENSION

    def direcciones(self, ficha: Ficha) -> List[Tuple[int, int]]:
        """Devuelve las diagonales permitidas para mover/capturar."""
        if ficha.coronada:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        avance = -1 if ficha.jugador == 1 else 1
        return [(avance, -1), (avance, 1)]

    def movimientos_de_ficha(
        self, origen: Position, solo_capturas: bool = False
    ) -> List[Move]:
        """Lista destinos como (destino, ficha_capturada)."""
        ficha = self.casillas[origen[0]][origen[1]]
        if ficha is None:
            return []

        movimientos: List[Move] = []
        for df, dc in self.direcciones(ficha):
            intermedia = (origen[0] + df, origen[1] + dc)
            destino = (origen[0] + 2 * df, origen[1] + 2 * dc)

            if (
                self.dentro(destino)
                and self.dentro(intermedia)
                and self.casillas[intermedia[0]][intermedia[1]] is not None
                and self.casillas[intermedia[0]][intermedia[1]].jugador
                != ficha.jugador
                and self.casillas[destino[0]][destino[1]] is None
            ):
                movimientos.append((destino, intermedia))
            elif not solo_capturas and self.dentro(intermedia):
                if self.casillas[intermedia[0]][intermedia[1]] is None:
                    movimientos.append((intermedia, None))
        return movimientos

    def movimientos_legales(
        self, jugador: int, origen_fijo: Optional[Position] = None
    ) -> MovesByOrigin:
        """Devuelve movimientos legales, aplicando la captura obligatoria."""
        posiciones = [origen_fijo] if origen_fijo is not None else [
            (fila, columna)
            for fila in range(BOARD_DIMENSION)
            for columna in range(BOARD_DIMENSION)
            if self.casillas[fila][columna] is not None
            and self.casillas[fila][columna].jugador == jugador
        ]
        capturas: MovesByOrigin = {}
        for posicion in posiciones:
            if posicion is None:
                continue
            ficha = self.casillas[posicion[0]][posicion[1]]
            if ficha is not None and ficha.jugador == jugador:
                opciones = self.movimientos_de_ficha(posicion, solo_capturas=True)
                if opciones:
                    capturas[posicion] = opciones

        if capturas:
            return capturas

        if origen_fijo is not None:
            return {}
        normales: MovesByOrigin = {}
        for posicion in posiciones:
            if posicion is None:
                continue
            ficha = self.casillas[posicion[0]][posicion[1]]
            if ficha is not None and ficha.jugador == jugador:
                opciones = self.movimientos_de_ficha(posicion)
                if opciones:
                    normales[posicion] = opciones
        return normales

    def mover(
        self, origen: Position, destino: Position, capturada: Optional[Position]
    ) -> bool:
        """Ejecuta un movimiento ya validado y corona si corresponde."""
        ficha = self.casillas[origen[0]][origen[1]]
        if ficha is None or self.casillas[destino[0]][destino[1]] is not None:
            return False
        self.casillas[origen[0]][origen[1]] = None
        self.casillas[destino[0]][destino[1]] = ficha
        if capturada is not None:
            self.casillas[capturada[0]][capturada[1]] = None

        if (ficha.jugador == 1 and destino[0] == 0) or (
            ficha.jugador == 2 and destino[0] == BOARD_DIMENSION - 1
        ):
            ficha.coronada = True
        return True

    def tiene_fichas(self, jugador: int) -> bool:
        return any(
            ficha is not None and ficha.jugador == jugador
            for fila in self.casillas
            for ficha in fila
        )

    def ganador(self, jugador_actual: int) -> Optional[int]:
        """Indica el ganador cuando el jugador actual ya no puede continuar."""
        if not self.tiene_fichas(jugador_actual) or not self.movimientos_legales(jugador_actual):
            return 3 - jugador_actual
        return None
