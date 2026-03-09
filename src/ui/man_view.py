import tkinter as tk

from assets.pieces.king_dark import draw_dark_king
from assets.pieces.king_light import draw_light_king
from assets.pieces.man_dark import draw_dark_man
from assets.pieces.man_light import draw_light_man
from engine.initial_state import board_size

#draw all pieces and optional move and select highlights
def draw_pieces(canvas, board, theme, selected=None, jump_sources=None, move_targets=None):
    canvas.delete("piece")

    edge = theme.border_thickness
    tile = theme.square_size

    if move_targets:
        for (target_row, target_col) in move_targets:
            tx1 = edge + target_col * tile + 18
            ty1 = edge + target_row * tile + 18
            tx2 = edge + (target_col + 1) * tile - 18
            ty2 = edge + (target_row + 1) * tile - 18
            canvas.create_oval(tx1, ty1, tx2, ty2, fill="#6f9f5f", outline="#5f8c50", width=2, tags="piece")

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

    if jump_sources:
        for (jump_row, jump_col) in jump_sources:
            jump_x1 = edge + jump_col * tile + 4
            jump_y1 = edge + jump_row * tile + 4
            jump_x2 = edge + (jump_col + 1) * tile - 4
            jump_y2 = edge + (jump_row + 1) * tile - 4
            canvas.create_rectangle(jump_x1, jump_y1, jump_x2, jump_y2, outline="#d9534f", width=3, tags="piece")

    if selected is not None:
        selected_row, selected_col = selected
        selected_x1 = edge + selected_col * tile + 4
        selected_y1 = edge + selected_row * tile + 4
        selected_x2 = edge + (selected_col + 1) * tile - 4
        selected_y2 = edge + (selected_row + 1) * tile - 4
        canvas.create_rectangle(selected_x1, selected_y1, selected_x2, selected_y2, outline="#57b957", width=3, tags="piece")
