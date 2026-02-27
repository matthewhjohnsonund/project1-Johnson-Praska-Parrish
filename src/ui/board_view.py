from dataclasses import dataclass
import tkinter as tk

from assets.board.square_dark import draw_dark_square
from assets.board.square_light import draw_light_square
from engine.initial_state import board_size

border_color = "#4b2e12"

@dataclass(frozen=True)
class BoardTheme:
    square_size: int = 72
    border_thickness: int = 12

#Calculate total canvas size from theme
def board_pixel_size(theme):
    return board_size * theme.square_size + theme.border_thickness * 2

#Draw board border and all squares
def draw_board(canvas, theme):
    canvas.delete("board")

    canvas_span = board_pixel_size(theme)
    edge = theme.border_thickness
    tile = theme.square_size

    canvas.create_rectangle(0, 0, canvas_span,canvas_span, fill=border_color, outline=border_color, tags="board",)

    for row in range(board_size):
        for col in range(board_size):
            x1 = edge + col * tile
            y1 = edge + row * tile
            x2 = x1 + tile
            y2 = y1 + tile

            if (row + col) % 2 == 0:
                draw_dark_square(canvas, x1, y1, x2, y2)
            else:
                draw_light_square(canvas, x1, y1, x2, y2)