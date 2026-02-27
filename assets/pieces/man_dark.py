import tkinter as tk

dark_man = "#000000"

#Draw a dark man checker piece
def draw_dark_man(canvas, x1, y1, x2, y2):
    canvas.create_oval(x1, y1, x2, y2, fill=dark_man, outline="#1f1f1f", width=2, tags="piece")