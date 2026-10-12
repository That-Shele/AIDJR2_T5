# Damas

Juego de damas con interfaz grafica en Pygame. Permite jugar entre dos
personas o contra una inteligencia artificial con dificultad casual y experta.

## Requisitos y ejecucion en Windows

Se necesita Python y Pygame. 
Instala la dependencia una sola vez:

```powershell
py -m pip install -r requirements.txt
```

Luego, desde la carpeta del proyecto, ejecuta el juego directamente:

```powershell
py damas.py
```

Tambien puedes ejecutar `damas.py` desde VS Code; selecciona el Python en el
que instalaste Pygame. Si aparece `ModuleNotFoundError: No module named 'pygame'`,
instala Pygame con el mismo comando `py -m pip` y asegurate de usar ese mismo
interprete para ejecutar el juego.

## Controles y modos

- Selecciona una ficha y luego una casilla resaltada para moverla.
- La captura es obligatoria y las capturas multiples deben continuar con la
  misma ficha cuando haya otra captura disponible.
- El juego permite alternar entre dos jugadores y jugar contra la IA.
- La IA ofrece dificultad casual y experta.

## Estructura del proyecto

```text
damas.py                 Punto de entrada y exportaciones publicas
checkers/
  domain.py              Fichas, tablero, movimientos y reglas
  application.py         Seleccion y evaluacion de jugadas de la IA
  pygame_ui.py           Ventana, renderizado, eventos e interaccion
requirements.txt         Dependencias externas del juego
```

## Refactorizacion

El codigo esta separado en capas por responsabilidad. Asi las reglas del juego
no dependen de la ventana, la IA trabaja con las operaciones del dominio y la
interfaz se ocupa de presentar el estado y recibir las acciones del jugador.
La separacion mantiene las reglas del dominio independientes de la ventana y
reduce el impacto de cambios en una capa sobre las demas.

### 1. Dominio: estado y reglas sin dependencias graficas

`checkers/domain.py` define `Ficha`, `Position` y `Tablero`. El tablero calcula
los movimientos legales, aplica captura obligatoria, ejecuta movimientos y
determina coronaciones. No importa Pygame:

```python
if capturas:
    return capturas
```

Este fragmento es parte de `Tablero.movimientos_legales()`: el metodo busca
capturas antes de ofrecer movimientos normales. Tanto la interfaz como la
inteligencia artificial consultan la misma implementacion, evitando que cada
una aplique reglas distintas.

### 2. Aplicacion: la IA reutiliza el dominio

`checkers/application.py` contiene `InteligenciaArtificial`. En vez de
reimplementar los movimientos, obtiene candidatos del tablero y simula
jugadas sobre una copia independiente:

```python
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

prueba = tablero.clonar()
prueba.mover(origen, destino, capturada)
puntuacion = self.evaluar(prueba)
```

El ejemplo combina fragmentos del metodo `elegir()`: la dificultad casual
escoge entre las jugadas legales y la experta evalua posibles resultados y
respuestas del rival. En el analisis experto, `clonar()` evita modificar la
partida real mientras se analizan alternativas.

### 3. Interfaz: Pygame aislado en su propio modulo

`checkers/pygame_ui.py` contiene la ventana, el renderizado y el manejo de
eventos. Importa Pygame junto con las clases de aplicacion y dominio, mientras
que estas capas inferiores no dependen de la interfaz:

```python
import pygame

from .application import InteligenciaArtificial
from .domain import Ficha, Move, Position, Tablero
```

Esta direccion de dependencias mantiene la logica visual fuera de las reglas
del juego y reduce el acoplamiento entre los modulos.

### 4. Punto de entrada y dependencia explicita

`damas.py` mantiene un arranque pequeno y concentrado:

```python
if __name__ == "__main__":
    Juego().ejecutar()
```

Pygame se declara en `requirements.txt` en vez de depender de una instalacion
manual no documentada. Para facilitar la ejecucion directa solicitada, la
configuracion de VS Code no fija la ruta a un entorno virtual: el proyecto usa
el interprete que seleccione el usuario.


