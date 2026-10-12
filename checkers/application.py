"""Casos de uso para tomar decisiones automáticas en una partida."""

import random
from typing import List, Optional, Tuple

from .domain import Position, Tablero


class InteligenciaArtificial:
    """Oponente sin red: casual es aleatorio y experto evalua varias jugadas."""

    def elegir(
        self,
        tablero: Tablero,
        dificultad: str,
        origen_fijo: Optional[Position] = None,
    ) -> Optional[Tuple[Position, Position]]:
        opciones = tablero.movimientos_legales(2, origen_fijo)
        candidatos = [
            (origen, destino, capturada)
            for origen, movimientos in opciones.items()
            for destino, capturada in movimientos
        ]
        if not candidatos:
            return None
        if dificultad == "casual":
            origen, destino, _ = random.choice(candidatos)
            return origen, destino

        puntuados: List[Tuple[float, Position, Position]] = []
        for origen, destino, capturada in candidatos:
            prueba = tablero.clonar()
            prueba.mover(origen, destino, capturada)
            puntuacion = self.evaluar(prueba)
            respuestas = prueba.movimientos_legales(1)
            if respuestas:
                peor_respuesta = float("inf")
                for respuesta_origen, movimientos in respuestas.items():
                    for respuesta_destino, respuesta_capturada in movimientos:
                        respuesta = prueba.clonar()
                        respuesta.mover(
                            respuesta_origen, respuesta_destino, respuesta_capturada
                        )
                        peor_respuesta = min(
                            peor_respuesta, self.evaluar(respuesta)
                        )
                puntuacion = puntuacion * 0.45 + peor_respuesta * 0.55
            if capturada is not None:
                puntuacion += 35
            ficha = prueba.casillas[destino[0]][destino[1]]
            if ficha is not None and ficha.coronada:
                puntuacion += 60
            puntuados.append((puntuacion + random.random() * 4, origen, destino))
        _, origen, destino = max(puntuados)
        return origen, destino

    def evaluar(self, tablero: Tablero) -> float:
        valor = 0.0
        for fila in range(8):
            for columna in range(8):
                ficha = tablero.casillas[fila][columna]
                if ficha is None:
                    continue
                base = 150 if ficha.coronada else 100
                avance = fila if ficha.jugador == 2 else 7 - fila
                centralidad = 4 - abs(3.5 - columna)
                valor += (base + avance * 3 + centralidad) * (1 if ficha.jugador == 2 else -1)
        valor += len(tablero.movimientos_legales(2)) * 2
        valor -= len(tablero.movimientos_legales(1)) * 2
        return valor
