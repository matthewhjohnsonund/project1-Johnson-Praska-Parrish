import tkinter as tk

light_yellow = "#e7d09a"

#Draw one light board square
def draw_light_square(canvas, x1, y1, x2, y2):
    canvas.create_rectangle(x1, y1, x2, y2, fill=light_yellow, outline=light_yellow, tags="board")