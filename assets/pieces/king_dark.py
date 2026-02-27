import tkinter as tk

gold = "#d4af37"

#Draw a dark king with the king label
def draw_dark_king(canvas, x1, y1, x2, y2):
    offset = 5
    canvas.create_oval(x1 + offset, y1 + offset, x2 + offset, y2 + offset, fill="#0e0e0e", outline="#262626", width=2, tags="piece")
    canvas.create_oval(x1, y1, x2, y2, fill="#000000", outline="#303030", width=2, tags="piece")
    canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="King", fill=gold, font=("Arial", 11, "bold"), tags="piece")