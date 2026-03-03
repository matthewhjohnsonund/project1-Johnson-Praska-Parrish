from pathlib import Path
import sys
import tkinter as tk

#Keep this project root when running
repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from engine.actions import apply_move, validate_move, has_jump_from, any_jump_for_side
from engine.turn import side_to_move, switch_turn, piece_belongs_to_side
from engine.initial_state import create_initial_board
from ui.board_view import BoardTheme, board_pixel_size, draw_board
from ui.man_view import draw_pieces

class CheckersApp:
    #Set up state and ui elements
    def __init__(self, root):
        self.root = root
        self.root.title("Checkers")
        self.theme = BoardTheme()
        self.board = create_initial_board()
        self.selected = None
        self.forced_continuation = False # When True, the player must continue jumping with the selected piece

        size = board_pixel_size(self.theme)

        # Title and subtitle labels above the board
        self.title_label = tk.Label(root, text="", font=(None, 14))
        self.title_label.pack(padx=12, pady=(6, 0))
        self.subtitle_label = tk.Label(root, text="", font=(None, 10))
        self.subtitle_label.pack(padx=12, pady=(0, 6))

        self.canvas = tk.Canvas(root, width=size, height=size, highlightthickness=0)
        self.canvas.pack(padx=12, pady=(0, 6))
        self.canvas.bind("<Button-1>", self.on_click)
        self.redraw()

    #Redraw board and pieces
    def redraw(self):
        draw_board(self.canvas, self.theme)
        # Compute jumpable piece locations for current side when appropriate
        jump_sources = None
        current = side_to_move()
        if not self.forced_continuation and any_jump_for_side(self.board, current):
            # Collect all pieces for current side that can jump
            jump_sources = []
            for r in range(len(self.board)):
                for c in range(len(self.board[r])):
                    if self.board[r][c] is None:
                        continue
                    if self.board[r][c].split("_")[0] != current:
                        continue
                    if has_jump_from(self.board, (r, c)):
                        jump_sources.append((r, c))
        elif self.forced_continuation and self.selected is not None:
            jump_sources = [self.selected]

        draw_pieces(self.canvas, self.board, self.theme, selected=self.selected, jump_sources=jump_sources)
        # Update turn/title labels
        side = side_to_move()
        title = "Dark side's turn!" if side == "dark" else "Light side's turn!"
        # Subtitle hints
        if self.forced_continuation:
            subtitle = "Must finish available jump move(s) to end turn."
        elif any_jump_for_side(self.board, side):
            subtitle = "Must make available jump move(s)."
        else:
            subtitle = ""

        self.title_label.config(text=title)
        self.subtitle_label.config(text=subtitle)

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

        # Selecting a piece, must belong to side to move
        if self.selected is None:
            if clicked_piece is None:
                return
            if not piece_belongs_to_side(clicked_piece, side_to_move()):
                return
            # If any jump exists for this side, force selecting a jumping piece
            if any_jump_for_side(self.board, side_to_move()) and not has_jump_from(self.board, (row, col)):
                return
            self.selected = picked_tile
            self.redraw()
            return

        if picked_tile == self.selected:
            # Allow unselect only when not forced to continue jumping
            if self.forced_continuation:
                return
            self.selected = None
            self.redraw()
            return

        if clicked_piece is not None:
            # If forced to continue jumping, disallow changing selection
            if self.forced_continuation:
                return
            # Switch selection only if piece belongs to current side
            if piece_belongs_to_side(clicked_piece, side_to_move()):
                self.selected = picked_tile
                self.redraw()
            return

        move_check = validate_move(self.board, self.selected, picked_tile)
        if not move_check["legal"]:
            return

        # When forced continuation is active, only allow capture (jump) moves
        if self.forced_continuation and move_check.get("captured") is None:
            return

        # If a jump is available at start of turn, force jump move and disallow non-jump moves
        if not self.forced_continuation and any_jump_for_side(self.board, side_to_move()) and move_check.get("captured") is None:
            return

        validation = apply_move(self.board, self.selected, picked_tile)

        # If a capture happened and another jump is available from destination, keep selection
        if validation.get("captured") and has_jump_from(self.board, picked_tile):
            self.selected = picked_tile
            self.forced_continuation = True
        else:
            self.selected = None
            # Clear forced continuation when turn ends
            self.forced_continuation = False
            switch_turn()

        self.redraw()

if __name__ == "__main__":
    app_root = tk.Tk()
    CheckersApp(app_root)
    app_root.mainloop()