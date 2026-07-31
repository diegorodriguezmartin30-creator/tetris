# Tetris (Python + Pygame)

Clon completo y ligero de Tetris, hecho en un único archivo (`main.py`),
sin imágenes ni sonidos externos: todo se dibuja con primitivas de Pygame.
Pensado para consumir muy pocos recursos y funcionar bien incluso en
equipos antiguos con Windows 10 / 11.

## Requisitos

- Python 3.9 o superior
- Pygame (ver `requirements.txt`)

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecutar el juego

```bash
python main.py
```

## Controles

| Tecla                  | Acción                          |
|-------------------------|----------------------------------|
| ← / →                   | Mover pieza izquierda / derecha |
| ↓                        | Soft drop (bajar más rápido)    |
| Espacio                 | Hard drop (caída instantánea)   |
| Z                       | Girar en sentido antihorario    |
| X o ↑                   | Girar en sentido horario        |
| + / -                   | Aumentar / disminuir velocidad  |
| RePág / AvPág           | Alternativa a + / - para velocidad |
| P                       | Pausar / reanudar                |
| R                       | Reiniciar partida                |
| Esc                     | Salir                            |

> **Nota sobre las teclas de velocidad:** en la especificación original se
> proponían dos alternativas equivalentes: `+ / -` o `↑ / ↓`. Como `↑` ya
> está asignada a "girar horario" en la sección de controles, se optó por
> `+ / -` como control principal de velocidad para evitar el conflicto,
> añadiendo `RePág / AvPág` como alternativa sin ambigüedad.

## Funcionalidades implementadas

- Las 7 piezas oficiales (I, O, T, S, Z, J, L) con sus colores clásicos.
- Rotación con "wall kicks" simples (evita que la pieza se bloquee al
  girar junto a paredes u otras piezas).
- Movimiento izquierda/derecha con auto-repetición (DAS) al mantener pulsado.
- Caída automática, soft drop y hard drop.
- Detección de colisiones y fijado de piezas.
- Eliminación de líneas completas con puntuación tipo "guideline"
  (100 / 300 / 500 / 800 puntos × nivel, según 1, 2, 3 o 4 líneas).
- Sistema de nivel: sube cada 10 líneas eliminadas y acelera la caída.
- Velocidad de caída ajustable en cualquier momento (multiplicador
  independiente del nivel), mostrada en pantalla en todo momento.
- Generación aleatoria equilibrada mediante el sistema "bolsa de 7"
  (7-bag): las 7 piezas aparecen una vez antes de repetirse.
- Vista previa de la siguiente pieza.
- Pausa, reinicio y pantalla de fin de partida.
- Bucle de juego limitado a 60 FPS.

## Optimización

- Sin dependencias más allá de Pygame.
- Sin imágenes ni sonidos: todo el dibujo usa `pygame.draw` y texto con
  `pygame.font`.
- Estructuras de datos simples (listas de listas) para el tablero.
- Un único archivo Python, fácil de leer, mantener y distribuir.

## Generar un ejecutable único (.exe) para Windows

Para producir un `.exe` ligero (sin consola, sin archivos adicionales),
usa [PyInstaller](https://pyinstaller.org/) **en un Windows** (PyInstaller
genera ejecutables para el sistema operativo en el que se ejecuta):

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

El ejecutable resultante quedará en la carpeta `dist/main.exe`.

Recomendaciones para que el `.exe` sea lo más pequeño posible:

- Usa un entorno virtual limpio con **solo** `pygame` instalado antes de
  empaquetar (`python -m venv venv`, actívalo e instala únicamente
  `requirements.txt`). Cuantas menos librerías tenga el entorno, más
  pequeño será el ejecutable, ya que PyInstaller empaqueta todo lo que
  encuentra instalado.
- Opcionalmente, comprime el resultado con
  [UPX](https://upx.github.io/) añadiendo `--upx-dir <ruta_a_upx>` al
  comando de PyInstaller.
- Puedes renombrar el ejecutable final, por ejemplo:
  ```bash
  pyinstaller --onefile --windowed --name Tetris main.py
  ```
  El resultado será `dist/Tetris.exe`.

Compatibilidad: probado para funcionar en Windows 10 y Windows 11
(requiere tener instalado el runtime de Visual C++ que ya incluye
Windows de forma nativa en versiones recientes).

## Estructura del proyecto

```
main.py            # Código completo del juego
requirements.txt   # Dependencia única: pygame
README.md          # Este archivo
```
