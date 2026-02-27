import tkinter as tk

light_man = "#f0f0f0"

#Draw a light man checker piece
def draw_light_man(canvas, x1, y1, x2, y2):
    canvas.create_oval(x1, y1, x2, y2, fill=light_man, outline="#c9c9c9", width=2, tags="piece")