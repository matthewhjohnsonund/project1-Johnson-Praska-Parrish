import tkinter as tk

from assets.pieces.king_dark import draw_dark_king
from assets.pieces.king_light import draw_light_king
from assets.pieces.man_dark import draw_dark_man
from assets.pieces.man_light import draw_light_man
from engine.initial_state import board_size

#Draw all pieces and optional selection
def draw_pieces(canvas, board, theme, selected=None):
    canvas.delete("piece")

    edge = theme.border_thickness
    tile = theme.square_size

    for row in range(board_size):
        for col in range(board_size):
            piece = board[row][col]
            if piece is None:
                continue

            x1 = edge + col * tile + 8
            y1 = edge + row * tile + 8
            x2 = edge + (col + 1) * tile - 8
            y2 = edge + (row + 1) * tile - 8

            if piece == "dark_man":
                draw_dark_man(canvas, x1, y1, x2, y2)
            elif piece == "light_man":
                draw_light_man(canvas, x1, y1, x2, y2)
            elif piece == "dark_king":
                draw_dark_king(canvas, x1, y1, x2, y2)
            elif piece == "light_king":
                draw_light_king(canvas, x1, y1, x2, y2)

    if selected is not None:
        row, col = selected
        sx1 = edge + col * tile + 4
        sy1 = edge + row * tile + 4
        sx2 = edge + (col + 1) * tile - 4
        sy2 = edge + (row + 1) * tile - 4
        canvas.create_rectangle(sx1, sy1, sx2, sy2, outline="#e8d17a", width=3, tags="piece",)