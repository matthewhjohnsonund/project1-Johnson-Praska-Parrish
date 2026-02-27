import tkinter as tk

gold = "#d4af37"

#Draw a light king with the king label
def draw_light_king(canvas, x1, y1, x2, y2):
    offset = 5
    canvas.create_oval(x1 + offset, y1 + offset, x2 + offset, y2 + offset, fill="#d7d7d7", outline="#bbbbbb", width=2, tags="piece")
    canvas.create_oval(x1, y1, x2, y2, fill="#f4f4f4", outline="#d0d0d0", width=2, tags="piece")
    canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text="King", fill=gold, font=("Arial", 11, "bold"), tags="piece")