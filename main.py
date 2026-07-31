# -*- coding: utf-8 -*-
"""
TETRIS - Clon completo en Python + Pygame
==========================================
Un unico archivo, sin recursos externos (sin imagenes ni sonidos),
todo dibujado con primitivas de Pygame para mantener el ejecutable
lo mas ligero posible y funcionar bien incluso en equipos antiguos.

Controles
---------
    Flecha Izquierda .... mover pieza a la izquierda
    Flecha Derecha ...... mover pieza a la derecha
    Flecha Abajo ........ soft drop (bajar mas rapido)
    Espacio ............. hard drop (caida instantanea)
    Z ................... girar antihorario
    X o Flecha Arriba ... girar horario
    + / - ............... aumentar / disminuir la velocidad de caida
    P ................... pausa
    R ................... reiniciar partida
    Esc ................. salir

Nota sobre teclas de velocidad
-------------------------------
El enunciado ofrecia dos alternativas para controlar la velocidad:
"+ / -" o bien "Flecha Arriba / Flecha Abajo". Como Flecha Arriba ya
esta asignada a "girar horario" (segun la seccion de controles), se
ha resuelto el conflicto usando "+ / -" como control principal de
velocidad. Como alternativa sin conflicto se anaden tambien las
teclas RePag (aumentar) y AvPag (disminuir).
"""

import pygame
import random
import sys

# ----------------------------------------------------------------------
# CONFIGURACION GENERAL
# ----------------------------------------------------------------------
CELL_SIZE = 28                       # tamano de cada celda del tablero (px)
BOARD_COLS = 10                      # columnas del tablero
BOARD_ROWS = 20                      # filas del tablero

BOARD_MARGIN_X = 20                  # margen izquierdo del tablero
BOARD_MARGIN_Y = 20                  # margen superior del tablero

SIDEBAR_GAP = 24                     # separacion entre tablero y panel lateral
SIDEBAR_WIDTH = 190                  # ancho del panel lateral

WINDOW_WIDTH = BOARD_MARGIN_X + BOARD_COLS * CELL_SIZE + SIDEBAR_GAP + SIDEBAR_WIDTH + BOARD_MARGIN_X
WINDOW_HEIGHT = BOARD_MARGIN_Y + BOARD_ROWS * CELL_SIZE + BOARD_MARGIN_Y

FPS = 60

# Velocidad de caida (fall interval) en milisegundos, segun nivel.
BASE_FALL_INTERVAL_MS = 800          # velocidad de caida en el nivel 1
MIN_FALL_INTERVAL_MS = 60            # limite inferior para no ir mas rapido que esto
LEVEL_SPEEDUP_MS = 60                # cuanto se reduce el intervalo por cada nivel

# Multiplicador de velocidad manual (controlado con +/-)
SPEED_STEP = 0.1
SPEED_MIN = 0.2
SPEED_MAX = 3.0

LINES_PER_LEVEL = 10                 # lineas necesarias para subir de nivel

SOFT_DROP_FACTOR = 12                # cuanto mas rapido cae con soft drop

DAS_DELAY_MS = 170                   # retardo inicial antes de repetir movimiento (DAS)
DAS_REPEAT_MS = 45                   # velocidad de repeticion tras el retardo

# ----------------------------------------------------------------------
# COLORES
# ----------------------------------------------------------------------
COLOR_BG = (18, 18, 24)
COLOR_BOARD_BG = (10, 10, 14)
COLOR_GRID = (40, 40, 50)
COLOR_BORDER = (90, 90, 110)
COLOR_TEXT = (230, 230, 235)
COLOR_TEXT_DIM = (150, 150, 165)
COLOR_PANEL_BG = (24, 24, 32)
COLOR_PAUSED = (250, 210, 60)
COLOR_GAMEOVER = (240, 70, 70)

# Colores clasicos de las 7 piezas
PIECE_COLORS = {
    "I": (0, 240, 240),
    "O": (240, 240, 0),
    "T": (160, 0, 240),
    "S": (0, 240, 0),
    "Z": (240, 0, 0),
    "J": (0, 0, 240),
    "L": (240, 160, 0),
}

# ----------------------------------------------------------------------
# DEFINICION DE PIEZAS (sistema tipo SRS, caja de 4x4)
# Cada pieza tiene 4 estados de rotacion. Cada estado es una lista de
# coordenadas (columna, fila) dentro de una caja de 4x4.
# ----------------------------------------------------------------------
SHAPES = {
    "I": [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(0, 2), (1, 2), (2, 2), (3, 2)],
        [(1, 0), (1, 1), (1, 2), (1, 3)],
    ],
    "O": [
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (2, 1)],
    ],
    "T": [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "S": [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
        [(1, 1), (2, 1), (0, 2), (1, 2)],
        [(0, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "Z": [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 2)],
        [(1, 0), (0, 1), (1, 1), (0, 2)],
    ],
    "J": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    "L": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
}

PIECE_NAMES = list(SHAPES.keys())

# Desplazamientos de "wall kick" simples: se prueban en orden al rotar,
# para permitir rotar cerca de las paredes u otras piezas sin bloquearse.
WALL_KICKS = [(0, 0), (-1, 0), (1, 0), (-2, 0), (2, 0), (0, -1)]


# ----------------------------------------------------------------------
# GENERADOR DE PIEZAS: sistema "bolsa de 7" (7-bag)
# Garantiza que las 7 piezas aparezcan una vez antes de repetirse,
# evitando rachas largas de la misma pieza o de piezas repetidas.
# ----------------------------------------------------------------------
class SevenBag:
    def __init__(self):
        self._bag = []

    def _refill(self):
        self._bag = PIECE_NAMES.copy()
        random.shuffle(self._bag)

    def next(self):
        if not self._bag:
            self._refill()
        return self._bag.pop()


# ----------------------------------------------------------------------
# CLASE PIEZA ACTIVA
# ----------------------------------------------------------------------
class Piece:
    def __init__(self, name):
        self.name = name
        self.rotation = 0
        # Posicion de la esquina superior izquierda de la caja 4x4
        # dentro del tablero (en celdas). Se centra horizontalmente.
        self.x = 3
        self.y = 0
        self.color = PIECE_COLORS[name]

    def cells(self, rotation=None, x=None, y=None):
        """Devuelve las celdas (columna, fila) absolutas del tablero
        que ocupa la pieza para una rotacion/posicion dadas."""
        rotation = self.rotation if rotation is None else rotation
        x = self.x if x is None else x
        y = self.y if y is None else y
        shape = SHAPES[self.name][rotation % 4]
        return [(x + cx, y + cy) for cx, cy in shape]


# ----------------------------------------------------------------------
# CLASE PRINCIPAL DEL JUEGO
# ----------------------------------------------------------------------
class Tetris:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tetris")
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.font_big = pygame.font.SysFont("consolas", 26, bold=True)
        self.font = pygame.font.SysFont("consolas", 20, bold=True)
        self.font_small = pygame.font.SysFont("consolas", 16)

        self.reset()

    # ------------------------------------------------------------------
    def reset(self):
        """Inicializa (o reinicia) el estado completo de la partida."""
        self.board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        self.bag = SevenBag()

        self.current = Piece(self.bag.next())
        self.next_name = self.bag.next()

        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.speed_multiplier = 1.0

        self.fall_timer_ms = 0.0
        self.paused = False
        self.game_over = False

        self.move_left_held = False
        self.move_right_held = False
        self.das_timer_ms = 0.0
        self.das_active = False

        self.soft_drop_held = False

    # ------------------------------------------------------------------
    def current_fall_interval(self):
        """Calcula el intervalo de caida (ms) segun nivel y velocidad manual."""
        base = BASE_FALL_INTERVAL_MS - (self.level - 1) * LEVEL_SPEEDUP_MS
        base = max(base, MIN_FALL_INTERVAL_MS)
        interval = base / self.speed_multiplier
        if self.soft_drop_held:
            interval /= SOFT_DROP_FACTOR
        return max(interval, 15)

    # ------------------------------------------------------------------
    def valid_position(self, rotation=None, x=None, y=None):
        """Comprueba si la pieza actual, en la rotacion/posicion dadas,
        cabe en el tablero sin salirse ni chocar con bloques fijos."""
        for cx, cy in self.current.cells(rotation, x, y):
            if cx < 0 or cx >= BOARD_COLS:
                return False
            if cy >= BOARD_ROWS:
                return False
            if cy >= 0 and self.board[cy][cx] is not None:
                return False
        return True

    # ------------------------------------------------------------------
    def try_move(self, dx, dy):
        new_x = self.current.x + dx
        new_y = self.current.y + dy
        if self.valid_position(x=new_x, y=new_y):
            self.current.x = new_x
            self.current.y = new_y
            return True
        return False

    # ------------------------------------------------------------------
    def try_rotate(self, direction):
        """direction: +1 horario, -1 antihorario. Aplica wall kicks simples."""
        new_rotation = (self.current.rotation + direction) % 4
        for kx, ky in WALL_KICKS:
            if self.valid_position(rotation=new_rotation,
                                    x=self.current.x + kx,
                                    y=self.current.y + ky):
                self.current.rotation = new_rotation
                self.current.x += kx
                self.current.y += ky
                return True
        return False

    # ------------------------------------------------------------------
    def hard_drop(self):
        distance = 0
        while self.try_move(0, 1):
            distance += 1
        self.score += distance * 2  # bonus por hard drop
        self.lock_piece()

    # ------------------------------------------------------------------
    def lock_piece(self):
        """Fija la pieza actual en el tablero y genera la siguiente."""
        for cx, cy in self.current.cells():
            if cy < 0:
                # La pieza quedo bloqueada por encima del tablero visible: fin del juego
                self.game_over = True
                return
            self.board[cy][cx] = self.current.color

        self.clear_lines()

        self.current = Piece(self.next_name)
        self.next_name = self.bag.next()

        if not self.valid_position():
            self.game_over = True

    # ------------------------------------------------------------------
    def clear_lines(self):
        full_rows = [r for r in range(BOARD_ROWS) if all(self.board[r][c] is not None for c in range(BOARD_COLS))]
        n = len(full_rows)
        if n == 0:
            return

        for r in full_rows:
            del self.board[r]
            self.board.insert(0, [None for _ in range(BOARD_COLS)])

        self.lines_cleared += n

        # Puntuacion clasica estilo guideline (por nivel)
        points_table = {1: 100, 2: 300, 3: 500, 4: 800}
        self.score += points_table.get(n, 800) * self.level

        new_level = 1 + self.lines_cleared // LINES_PER_LEVEL
        if new_level != self.level:
            self.level = new_level

    # ------------------------------------------------------------------
    def change_speed(self, delta):
        self.speed_multiplier = round(min(SPEED_MAX, max(SPEED_MIN, self.speed_multiplier + delta)), 1)

    # ------------------------------------------------------------------
    # BUCLE DE EVENTOS / ENTRADA
    # ------------------------------------------------------------------
    def handle_keydown(self, key):
        if key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit(0)

        if key == pygame.K_r:
            self.reset()
            return

        if key == pygame.K_p:
            if not self.game_over:
                self.paused = not self.paused
            return

        if self.paused or self.game_over:
            return

        if key == pygame.K_LEFT:
            self.try_move(-1, 0)
            self.move_left_held = True
            self.das_timer_ms = 0.0
            self.das_active = False
        elif key == pygame.K_RIGHT:
            self.try_move(1, 0)
            self.move_right_held = True
            self.das_timer_ms = 0.0
            self.das_active = False
        elif key == pygame.K_DOWN:
            self.soft_drop_held = True
        elif key == pygame.K_SPACE:
            self.hard_drop()
        elif key == pygame.K_z:
            self.try_rotate(-1)
        elif key in (pygame.K_x, pygame.K_UP):
            self.try_rotate(1)
        elif key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS, pygame.K_PAGEUP):
            self.change_speed(SPEED_STEP)
        elif key in (pygame.K_MINUS, pygame.K_KP_MINUS, pygame.K_PAGEDOWN):
            self.change_speed(-SPEED_STEP)

    # ------------------------------------------------------------------
    def handle_keyup(self, key):
        if key == pygame.K_LEFT:
            self.move_left_held = False
            self.das_active = False
        elif key == pygame.K_RIGHT:
            self.move_right_held = False
            self.das_active = False
        elif key == pygame.K_DOWN:
            self.soft_drop_held = False

    # ------------------------------------------------------------------
    def update(self, dt_ms):
        if self.paused or self.game_over:
            return

        # Auto-repeticion de movimiento horizontal (DAS)
        if self.move_left_held or self.move_right_held:
            self.das_timer_ms += dt_ms
            threshold = DAS_DELAY_MS if not self.das_active else DAS_REPEAT_MS
            if self.das_timer_ms >= threshold:
                self.das_timer_ms = 0.0
                self.das_active = True
                if self.move_left_held:
                    self.try_move(-1, 0)
                elif self.move_right_held:
                    self.try_move(1, 0)

        # Caida automatica
        self.fall_timer_ms += dt_ms
        interval = self.current_fall_interval()
        if self.fall_timer_ms >= interval:
            self.fall_timer_ms = 0.0
            if not self.try_move(0, 1):
                self.lock_piece()

    # ------------------------------------------------------------------
    # DIBUJO
    # ------------------------------------------------------------------
    def board_pixel_rect(self):
        w = BOARD_COLS * CELL_SIZE
        h = BOARD_ROWS * CELL_SIZE
        return pygame.Rect(BOARD_MARGIN_X, BOARD_MARGIN_Y, w, h)

    def draw_cell(self, col, row, color):
        rect = self.board_pixel_rect()
        px = rect.x + col * CELL_SIZE
        py = rect.y + row * CELL_SIZE
        pygame.draw.rect(self.screen, color, (px, py, CELL_SIZE, CELL_SIZE))
        # pequeno borde interior para dar efecto de bloque
        pygame.draw.rect(self.screen, COLOR_BOARD_BG, (px, py, CELL_SIZE, CELL_SIZE), 1)
        highlight = tuple(min(255, c + 45) for c in color)
        pygame.draw.line(self.screen, highlight, (px + 1, py + 1), (px + CELL_SIZE - 2, py + 1), 2)

    def draw_board(self):
        rect = self.board_pixel_rect()
        pygame.draw.rect(self.screen, COLOR_BOARD_BG, rect)

        # rejilla
        for c in range(BOARD_COLS + 1):
            x = rect.x + c * CELL_SIZE
            pygame.draw.line(self.screen, COLOR_GRID, (x, rect.y), (x, rect.y + rect.height))
        for r in range(BOARD_ROWS + 1):
            y = rect.y + r * CELL_SIZE
            pygame.draw.line(self.screen, COLOR_GRID, (rect.x, y), (rect.x + rect.width, y))

        # bloques fijos
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                color = self.board[r][c]
                if color is not None:
                    self.draw_cell(c, r, color)

        # pieza actual
        if not self.game_over:
            for cx, cy in self.current.cells():
                if cy >= 0:
                    self.draw_cell(cx, cy, self.current.color)

        pygame.draw.rect(self.screen, COLOR_BORDER, rect, 2)

    def draw_mini_piece(self, name, ox, oy, cell=18):
        """Dibuja una vista previa pequena y centrada de una pieza."""
        shape = SHAPES[name][0]
        color = PIECE_COLORS[name]
        min_x = min(p[0] for p in shape)
        max_x = max(p[0] for p in shape)
        min_y = min(p[1] for p in shape)
        max_y = max(p[1] for p in shape)
        w = (max_x - min_x + 1) * cell
        h = (max_y - min_y + 1) * cell
        start_x = ox - w // 2
        start_y = oy - h // 2
        for px, py in shape:
            x = start_x + (px - min_x) * cell
            y = start_y + (py - min_y) * cell
            pygame.draw.rect(self.screen, color, (x, y, cell, cell))
            pygame.draw.rect(self.screen, COLOR_PANEL_BG, (x, y, cell, cell), 1)

    def draw_text(self, text, x, y, font=None, color=COLOR_TEXT):
        font = font or self.font
        surf = font.render(text, True, color)
        self.screen.blit(surf, (x, y))
        return surf.get_height()

    def draw_sidebar(self):
        board_rect = self.board_pixel_rect()
        panel_x = board_rect.right + SIDEBAR_GAP
        panel_y = BOARD_MARGIN_Y
        panel_w = SIDEBAR_WIDTH
        panel_h = BOARD_ROWS * CELL_SIZE
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

        pygame.draw.rect(self.screen, COLOR_PANEL_BG, panel_rect, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_BORDER, panel_rect, 2, border_radius=8)

        pad = 16
        y = panel_y + pad

        y += self.draw_text("TETRIS", panel_x + pad, y, self.font_big) + 18

        y += self.draw_text("Puntuacion", panel_x + pad, y, self.font_small, COLOR_TEXT_DIM) + 2
        y += self.draw_text(str(self.score), panel_x + pad, y, self.font) + 14

        y += self.draw_text("Lineas", panel_x + pad, y, self.font_small, COLOR_TEXT_DIM) + 2
        y += self.draw_text(str(self.lines_cleared), panel_x + pad, y, self.font) + 14

        y += self.draw_text("Nivel", panel_x + pad, y, self.font_small, COLOR_TEXT_DIM) + 2
        y += self.draw_text(str(self.level), panel_x + pad, y, self.font) + 14

        y += self.draw_text("Velocidad", panel_x + pad, y, self.font_small, COLOR_TEXT_DIM) + 2
        y += self.draw_text("x{:.1f}".format(self.speed_multiplier), panel_x + pad, y, self.font) + 20

        y += self.draw_text("Siguiente", panel_x + pad, y, self.font_small, COLOR_TEXT_DIM) + 6
        preview_box = pygame.Rect(panel_x + pad, y, panel_w - pad * 2, 70)
        pygame.draw.rect(self.screen, COLOR_BOARD_BG, preview_box, border_radius=6)
        pygame.draw.rect(self.screen, COLOR_GRID, preview_box, 1, border_radius=6)
        self.draw_mini_piece(self.next_name, preview_box.centerx, preview_box.centery)
        y += preview_box.height + 20

        y += self.draw_text("Controles", panel_x + pad, y, self.font_small, COLOR_TEXT_DIM) + 4
        controls = [
            "<- ->  mover",
            "abajo  soft drop",
            "espacio hard drop",
            "Z / X  girar",
            "+ / -  velocidad",
            "P  pausa   R  reinicio",
        ]
        for line in controls:
            y += self.draw_text(line, panel_x + pad, y, self.font_small, COLOR_TEXT_DIM) + 4

    def draw_overlay(self, text, color):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        surf = self.font_big.render(text, True, color)
        rect = surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(surf, rect)
        sub = self.font_small.render("Pulsa R para reiniciar", True, COLOR_TEXT)
        sub_rect = sub.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 34))
        self.screen.blit(sub, sub_rect)

    def draw(self):
        self.screen.fill(COLOR_BG)
        self.draw_board()
        self.draw_sidebar()

        if self.paused and not self.game_over:
            self.draw_overlay("PAUSA", COLOR_PAUSED)
        elif self.game_over:
            self.draw_overlay("FIN DE PARTIDA", COLOR_GAMEOVER)

        pygame.display.flip()

    # ------------------------------------------------------------------
    # BUCLE PRINCIPAL
    # ------------------------------------------------------------------
    def run(self):
        while True:
            dt_ms = self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.handle_keyup(event.key)

            self.update(dt_ms)
            self.draw()


# ----------------------------------------------------------------------
# PUNTO DE ENTRADA
# ----------------------------------------------------------------------
if __name__ == "__main__":
    game = Tetris()
    game.run()
