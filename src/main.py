from pathlib import Path
import sys
import tkinter as tk

repo_root = Path(__file__).resolve().parent.parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from engine.actions import apply_move, validate_move, has_jump_from, any_jump_for_side
from engine.turn import side_to_move, switch_turn, piece_belongs_to_side, reset_turns
from engine.initial_state import create_initial_board
from ui.board_view import BoardTheme, board_pixel_size
from ui.board_view import draw_board
from ui.man_view import draw_pieces
from engine.actions import cpu_move, _terminal_test


class CheckersApp:
    #build screens and shared style
    def __init__(self, root):
        self.root = root
        self.root.title("Checkers")
        self.theme = BoardTheme()
        self.mode = None
        self.board = create_initial_board()
        self.selected = None
        self.game_over = False
        self.forced_continuation = False
        self.main_frame = None
        self.canvas = None
        self.title_label = None
        self.subtitle_label = None
        self.score_label = None
        self.home_button = None
        self.agent_turn_active = False
        self.agent_turn_token = 0
        self._configure_root()
        self.show_start_screen()

    #apply shared window styling
    def _configure_root(self):
        self.root.configure(bg="#4b2e12")
        self.root.resizable(False, False)

    #build reusable button styles for cohesive ui
    def _button_style(self, size="base"):
        styles = {
            "base": {
                "bg": "#b48b2a",
                "fg": "#1f1f1f",
                "activebackground": "#e7d09a",
                "activeforeground": "#1f1f1f",
                "relief": "flat",
                "cursor": "hand2",
                "font": ("Helvetica", 12, "bold"),
                "padx": 18,
                "pady": 10,
            },
            "hero": {
                "bg": "#b48b2a",
                "fg": "#1f1f1f",
                "activebackground": "#e7d09a",
                "activeforeground": "#1f1f1f",
                "relief": "flat",
                "cursor": "hand2",
                "font": ("Helvetica", 14, "bold"),
                "padx": 28,
                "pady": 12,
            },
            "small": {
                "bg": "#b48b2a",
                "fg": "#1f1f1f",
                "activebackground": "#e7d09a",
                "activeforeground": "#1f1f1f",
                "relief": "flat",
                "cursor": "hand2",
                "font": ("Helvetica", 10, "bold"),
                "padx": 12,
                "pady": 6,
            },
        }
        return styles[size]

    #build initial launch screen
    def show_start_screen(self):
        self._cancel_agent_turn()
        self._clear_main_frame()
        self.main_frame = tk.Frame(self.root, bg="#4b2e12", padx=24, pady=22)
        self.main_frame.pack()

        hero_card = tk.Frame(self.main_frame, bg="#5a3617", padx=26, pady=22)
        hero_card.pack()

        tk.Label(
            hero_card,
            text="classic checkers",
            bg="#5a3617",
            fg="#f4e6c3",
            font=("Helvetica", 26, "bold"),
        ).pack(pady=(4, 6))

        tk.Label(
            hero_card,
            text="simple rules • smart jumps • clean strategy",
            bg="#5a3617",
            fg="#e7d09a",
            font=("Helvetica", 12, "italic"),
        ).pack(pady=(0, 18))

        tk.Button(
            hero_card,
            text="Play",
            command=self.show_mode_screen,
            width=12,
            **self._button_style("hero"),
        ).pack(pady=(0, 6))

        tk.Label(
            hero_card,
            text="choose mode, then start your match",
            bg="#5a3617",
            fg="#e7d09a",
            font=("Helvetica", 10),
        ).pack(pady=(2, 0))

    #build mode selection screen
    def show_mode_screen(self):
        self._cancel_agent_turn()
        self._clear_main_frame()
        self.main_frame = tk.Frame(self.root, bg="#4b2e12", padx=24, pady=24)
        self.main_frame.pack()

        mode_card = tk.Frame(self.main_frame, bg="#5a3617", padx=24, pady=20)
        mode_card.pack()

        tk.Label(
            mode_card,
            text="choose a game mode",
            bg="#5a3617",
            fg="#f4e6c3",
            font=("Helvetica", 20, "bold"),
        ).pack(pady=(6, 6))

        tk.Label(
            mode_card,
            text="pick your style and jump in",
            bg="#5a3617",
            fg="#e7d09a",
            font=("Helvetica", 11),
        ).pack(pady=(0, 14))

        tk.Button(
            mode_card,
            text="1 Player (vs Agent)",
            command=lambda: self.start_game("1p"),
            width=24,
            **self._button_style("base"),
        ).pack(pady=8)

        tk.Button(
            mode_card,
            text="2 Player (Human vs Human)",
            command=lambda: self.start_game("2p"),
            width=24,
            **self._button_style("base"),
        ).pack(pady=8)

        tk.Button(
            mode_card,
            text="Back",
            command=self.show_start_screen,
            width=12,
            **self._button_style("small"),
        ).pack(pady=(10, 0))

    #initialize game state and board ui
    def start_game(self, mode):
        self._cancel_agent_turn()
        self.mode = mode
        self.board = create_initial_board()
        self.selected = None
        self.game_over = False
        self.forced_continuation = False
        reset_turns()
        self._clear_main_frame()

        size = board_pixel_size(self.theme)
        self.main_frame = tk.Frame(self.root, bg="#4b2e12", padx=12, pady=12)
        self.main_frame.pack()

        hud_frame = tk.Frame(self.main_frame, bg="#5a3617", padx=10, pady=8)
        hud_frame.pack(fill="x", pady=(0, 8))

        self.home_button = tk.Button(
            hud_frame,
            text="Home",
            command=self.show_start_screen,
            **self._button_style("small"),
        )

        self.score_label = tk.Label(
            hud_frame,
            text="",
            bg="#5a3617",
            fg="#f4e6c3",
            font=("Helvetica", 12, "bold"),
        )
        self.score_label.pack(pady=(0, 4))

        self.title_label = tk.Label(
            hud_frame,
            text="",
            bg="#5a3617",
            fg="#f4e6c3",
            font=("Helvetica", 16, "bold"),
        )
        self.title_label.pack(pady=(0, 2))

        self.subtitle_label = tk.Label(
            hud_frame,
            text="",
            bg="#5a3617",
            fg="#e7d09a",
            font=("Helvetica", 11),
        )
        self.subtitle_label.pack()

        self.canvas = tk.Canvas(
            self.main_frame,
            width=size,
            height=size,
            highlightthickness=0,
            bd=0,
            bg="#4b2e12",
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)
        self.redraw()

    #show home button after game completion
    def _show_home_button(self):
        if self.home_button is not None and not self.home_button.winfo_ismapped():
            self.home_button.pack(anchor="w", pady=(0, 4), before=self.score_label)

    #cancel queued agent callbacks and clear animation state
    def _cancel_agent_turn(self):
        self.agent_turn_active = False
        self.agent_turn_token += 1

    #remove current screen frame
    def _clear_main_frame(self):
        if self.main_frame is not None:
            self.main_frame.destroy()

    #redraw board, pieces, and status labels
    def redraw(self):
        draw_board(self.canvas, self.theme)
        jump_sources = None
        current = side_to_move()
        show_jump_hints = not (self.mode == "1p" and current == "dark")
        if show_jump_hints and not self.forced_continuation and any_jump_for_side(self.board, current):
            jump_sources = []
            for row in range(len(self.board)):
                for col in range(len(self.board[row])):
                    if self.board[row][col] is None:
                        continue
                    if self.board[row][col].split("_")[0] != current:
                        continue
                    if has_jump_from(self.board, (row, col)):
                        jump_sources.append((row, col))
        elif show_jump_hints and self.forced_continuation and self.selected is not None:
            jump_sources = [self.selected]

        move_targets = self._selected_destinations()
        draw_pieces(
            self.canvas,
            self.board,
            self.theme,
            selected=self.selected,
            jump_sources=jump_sources,
            move_targets=move_targets,
        )
        self._update_scoreboard()
        self._update_status_text()


    #compute valid destination squares for selected piece
    def _selected_destinations(self):
        if self.selected is None:
            return []

        targets = []
        current_side = side_to_move()
        must_jump = any_jump_for_side(self.board, current_side)

        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] is not None:
                    continue
                move_check = validate_move(self.board, self.selected, (row, col))
                if not move_check["legal"]:
                    continue
                if self.forced_continuation and move_check.get("captured") is None:
                    continue
                if not self.forced_continuation and must_jump and move_check.get("captured") is None:
                    continue
                targets.append((row, col))

        return targets

    #update score text based on current board pieces
    def _update_scoreboard(self):
        dark_score = 0
        light_score = 0
        for row in self.board:
            for piece in row:
                if piece is None:
                    continue
                if piece.startswith("dark"):
                    dark_score += 1
                else:
                    light_score += 1
        mode_text = "1P vs Agent" if self.mode == "1p" else "2P Local Match"
        self.score_label.config(text=f"{mode_text}   |   dark {dark_score}  •  light {light_score}")

    #update turn messaging and game-over state
    def _update_status_text(self):
        side = side_to_move()
        side_name = "Dark" if side == "dark" else "Light"
        is_terminal = _terminal_test(self.board, player="CPU" if side == "dark" else "HUMAN")
        if is_terminal:
            self.game_over = True
            winner = "Light" if side == "dark" else "Dark"
            self._show_home_button()
            self.title_label.config(text=f"game over • {winner} wins")
            self.subtitle_label.config(text="tap home to return to the main play screen")
            return

        self.title_label.config(text=f"{side_name} to move")
        if self.forced_continuation:
            self.subtitle_label.config(text="continue your jump chain to finish the turn")
        elif any_jump_for_side(self.board, side):
            self.subtitle_label.config(text="capture available: a jump is required")
        elif self.mode == "1p" and side == "dark":
            self.subtitle_label.config(text="agent is planning the next move...")
        elif self.mode == "2p":
            self.subtitle_label.config(text="pass the device after each turn")
        else:
            self.subtitle_label.config(text="select a piece to begin")

    #convert click coordinates to board row and column
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

    #handle human interactions with the board
    def on_click(self, event):
        if self.game_over:
            return
        if self.mode == "1p" and side_to_move() == "dark":
            return

        picked_tile = self._pixel_to_square(event.x, event.y)
        if picked_tile is None:
            return

        row, col = picked_tile
        clicked_piece = self.board[row][col]

        if self.selected is None:
            if clicked_piece is None:
                return
            if not piece_belongs_to_side(clicked_piece, side_to_move()):
                return
            if any_jump_for_side(self.board, side_to_move()) and not has_jump_from(self.board, (row, col)):
                return
            self.selected = picked_tile
            self.redraw()
            return

        if picked_tile == self.selected:
            if self.forced_continuation:
                return
            self.selected = None
            self.redraw()
            return

        if clicked_piece is not None:
            if self.forced_continuation:
                return
            if piece_belongs_to_side(clicked_piece, side_to_move()):
                self.selected = picked_tile
                self.redraw()
            return

        move_check = validate_move(self.board, self.selected, picked_tile)
        if not move_check["legal"]:
            return

        if self.forced_continuation and move_check.get("captured") is None:
            return

        if not self.forced_continuation and any_jump_for_side(self.board, side_to_move()) and move_check.get("captured") is None:
            return

        validation = apply_move(self.board, self.selected, picked_tile)

        if validation.get("captured") and has_jump_from(self.board, picked_tile):
            self.selected = picked_tile
            self.forced_continuation = True
        else:
            self.selected = None
            self.forced_continuation = False
            switch_turn()

        self.redraw()

        if self.mode == "1p" and not self.game_over and side_to_move() == "dark":
            self._run_agent_turn()

    #execute agent move sequence in single-player mode
    def _run_agent_turn(self):
        if self.agent_turn_active:
            return
        self.agent_turn_active = True
        self.agent_turn_token += 1
        current_token = self.agent_turn_token
        self.root.after(100, lambda: self._run_agent_step(current_token))

    #render each agent step with ui pacing for smoother movement
    def _run_agent_step(self, token):
        if token != self.agent_turn_token:
            return
        if self.game_over or side_to_move() != "dark":
            self.agent_turn_active = False
            return

        move, validation = cpu_move(self.board)
        self.redraw()
        self.root.update_idletasks()

        if validation["captured"] and has_jump_from(self.board, move[1]):
            self.root.after(220, lambda: self._run_agent_step(token))
            return

        switch_turn()
        self.agent_turn_active = False
        self.redraw()


if __name__ == "__main__":
    app_root = tk.Tk()
    CheckersApp(app_root)
    app_root.mainloop()