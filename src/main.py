from pathlib import Path
import sys
import tkinter as tk

#Keep this project root when running
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from engine.actions import apply_move, validate_move
from engine.initial_state import create_initial_board
from ui.board_view import BoardTheme, board_pixel_size, draw_board
from ui.man_view import draw_pieces

class CheckersApp:
    #Set up state and ui elements
    def __init__(self, root):
        self.root = root
        self.root.title("King")
        self.theme = BoardTheme()
        self.board = create_initial_board()
        self.selected = None

        size = board_pixel_size(self.theme)
        self.canvas = tk.Canvas(root, width=size, height=size, highlightthickness=0)
        self.canvas.pack(padx=12, pady=(12, 6))

        tk.Label(root, anchor="w").pack(fill="x", padx=12, pady=(0, 12),)
        self.canvas.bind("<Button-1>", self.on_click)
        self.redraw()

    #Redraw board and pieces
    def redraw(self):
        draw_board(self.canvas, self.theme)
        draw_pieces(self.canvas, self.board, self.theme, selected=self.selected)

    #Convert pixel position to board square
    def _pixel_to_square(self, click_x, click_y):
        edge = self.theme.border_thickness
        tile = self.theme.square_size
        board_length = len(self.board)

        if click_x < edge or click_y < edge:
            return None

        row = (click_y - edge) // tile
        col = (click_x - edge) // tile

        if not (0 <= row < board_length and 0 <= col < board_length):
            return None
        return row, col

    #Handle click to select or move a piece
    def on_click(self, event):
        picked_tile = self._pixel_to_square(event.x, event.y)
        if picked_tile is None:
            return

        row, col = picked_tile
        clicked_piece = self.board[row][col]

        if self.selected is None:
            if clicked_piece is None:
                return
            self.selected = picked_tile
            self.redraw()
            return

        if picked_tile == self.selected:
            self.selected = None
            self.redraw()
            return

        if clicked_piece is not None:
            self.selected = picked_tile
            self.redraw()
            return

        move_check = validate_move(self.board, self.selected, picked_tile)
        if not move_check["legal"]:
            return

        apply_move(self.board, self.selected, picked_tile)
        self.selected = None
        self.redraw()

if __name__ == "__main__":
    app_root = tk.Tk()
    CheckersApp(app_root)
    app_root.mainloop()