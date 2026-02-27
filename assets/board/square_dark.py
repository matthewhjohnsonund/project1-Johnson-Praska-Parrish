import tkinter as tk

dark_yellow = "#b48b2a"

#Draw one dark board square
def draw_dark_square(canvas, x1, y1, x2, y2):
    canvas.create_rectangle(x1, y1, x2, y2, fill=dark_yellow, outline=dark_yellow, tags="board")