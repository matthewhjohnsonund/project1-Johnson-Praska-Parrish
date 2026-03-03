import math
import time
import copy

from engine.initial_state import board_size

#Check if row and col are inside board limits
def _in_bounds(row, col):
    return 0 <= row < board_size and 0 <= col < board_size

#Check if a piece is a king
def _is_king(piece):
    return piece.endswith("_king")

#Get side name from piece token
def _side(piece):
    return piece.split("_")[0]

#Get forward directions allowed for a piece
def _allowed_steps(piece):
    if _is_king(piece):
        return (-1, 1)
    if piece.startswith("dark"):
        return (1,)
    return (-1,)

#Make sure one move and return legal status and optional capture square
def validate_move(board, start, end):
    from_row, from_col = start
    to_row, to_col = end

    if not _in_bounds(from_row, from_col) or not _in_bounds(to_row, to_col):
        return {"legal": False, "reason": "King", "captured": None}

    piece = board[from_row][from_col]
    if piece is None:
        return {"legal": False, "reason": "King", "captured": None}

    if board[to_row][to_col] is not None:
        return {"legal": False, "reason": "King", "captured": None}

    row_offset = to_row - from_row
    col_offset = to_col - from_col

    if abs(col_offset) != abs(row_offset):
        return {"legal": False, "reason": "King", "captured": None}

    if abs(row_offset) not in (1, 2):
        return {"legal": False, "reason": "King", "captured": None}

    ok_steps = _allowed_steps(piece)

    if abs(row_offset) == 1:
        if row_offset not in ok_steps:
            return {"legal": False, "reason": "King", "captured": None}
        return {"legal": True, "reason": "", "captured": None}

    if row_offset // 2 not in ok_steps:
        return {"legal": False, "reason": "King", "captured": None}

    mid_row = (from_row + to_row) // 2
    mid_col = (from_col + to_col) // 2
    jumped_piece = board[mid_row][mid_col]

    if jumped_piece is None:
        return {"legal": False, "reason": "King", "captured": None}

    if _side(jumped_piece) == _side(piece):
        return {"legal": False, "reason": "King", "captured": None}

    return {"legal": True, "reason": "", "captured": (mid_row, mid_col)}

#Add a legal move and update board including capture and update
def apply_move(board, start, end):
    validation = validate_move(board, start, end)
    if not validation["legal"]:
        return validation

    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]

    board[start_row][start_col] = None
    board[end_row][end_col] = piece

    if validation["captured"]:
        cap_row, cap_col = validation["captured"]
        board[cap_row][cap_col] = None

    if piece == "dark_man" and end_row == board_size - 1:
        board[end_row][end_col] = "dark_king"
    elif piece == "light_man" and end_row == 0:
        board[end_row][end_col] = "light_king"

    return validation

# alpha beta cutoff search to determine best move for the cpu
def cpu_move(board):
    def max_value(state, alpha, beta, depth):
        if _terminal_test(state, "CPU") or depth == 5:
            return _utility(state, "CPU")
        v = -math.inf
        for move, validation in _game_actions(state, "CPU"):
            new_state = copy.deepcopy(state)
            apply_move(new_state, move[0], move[1])
            # If capture move is available after a capture move, do not increase depth and treat it as one state
            if validation["captured"] and has_jump_from(new_state, move[1]):
                v = max(v, max_value(new_state, alpha, beta, depth))
            else:
                v = max(v, min_value(new_state, alpha, beta, depth + 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if _terminal_test(state, "HUMAN") or depth == 5:
            return _utility(state, "CPU")
        v = math.inf
        for move, validation in _game_actions(state, "HUMAN"):
            new_state = copy.deepcopy(state)
            apply_move(new_state, move[0], move[1])
            if validation["captured"] and has_jump_from(new_state, move[1]):
                v = min(v, min_value(new_state, alpha, beta, depth))
            else:
                v = min(v, max_value(new_state, alpha, beta, depth + 1))

            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    best_score = -math.inf
    beta = math.inf
    best_action = None
    for move, validation in _game_actions(board, "CPU"):
        new_state = copy.deepcopy(board)
        apply_move(new_state, move[0], move[1])
        if validation["captured"] and has_jump_from(new_state, move[1]):
            v = max_value(new_state, best_score, beta, 1)
        else:
            v = min_value(new_state, best_score, beta, 1)
        if v > best_score:
            best_score = v
            best_action = move

    print("Best action:", best_action)
    time.sleep(1)
    return best_action, apply_move(board, best_action[0], best_action[1])

# Helper function to create valid actions for a player given the board
def _game_actions(board, player):
    piece_side = "light"
    if player == "CPU":
        piece_side = "dark"

    moves = []

    for row in range(board_size):
        for col in range(board_size):
            tile = board[row][col]
            if tile is None or _side(tile) != piece_side:
                continue
            for move, validation in _piece_moves(board, row, col):
                if validation["legal"]:
                    moves.append((move, validation))

    return moves


def _piece_moves(board, row, col):
    directions = _allowed_steps(board[row][col])
    moves = []
    # Only return capture moves for a piece
    if has_jump_from(board, (row, col)):
        for direction in directions:
            moves.append(((row, col), (row + (direction*2), col + 2)))
            moves.append(((row, col), (row + (direction*2), col - 2)))
    else:
        for direction in directions:
            moves.append(((row, col), (row + direction, col + 1)))
            moves.append(((row, col), (row + direction, col - 1)))

    for move in moves:
        validation = validate_move(board, move[0], move[1])
        yield move, validation

# Determines utility of given state for player
def _utility(board, player):
    num_light = 0
    num_dark = 0
    num_light_kings = 0
    num_dark_kings = 0

    for row in range(board_size):
        for col in range(board_size):
            tile = board[row][col]
            if tile is None:
                continue
            if _side(tile) == "light":
                num_light += 1
                if _is_king(tile):
                    num_light -= 1
                    num_light_kings += 1
            else:
                num_dark += 1
                if _is_king(tile):
                    num_dark -= 1
                    num_dark_kings += 1
    if player == "CPU":
        return ((5*num_dark) - (6*num_light)) + ((9*num_dark_kings) - (8*num_light_kings))
    else:
        return ((5*num_light) - (6*num_dark)) + ((9*num_light_kings) - (8*num_dark_kings))

def _terminal_test(board, player):
    return sum(1 for _ in _game_actions(board, player)) == 0

# Check if a piece at position has any capturing jumps
def has_jump_from(board, position):
    row, col = position
    piece = board[row][col]
    if piece is None:
        return False

    steps = _allowed_steps(piece)
    # Possible row offsets for jump are step*2 for each allowed step
    for rstep in steps:
        for cstep in (-1, 1):
            mid_row = row + rstep
            mid_col = col + cstep
            to_row = row + rstep * 2
            to_col = col + cstep * 2

            if not _in_bounds(mid_row, mid_col) or not _in_bounds(to_row, to_col):
                continue

            jumped = board[mid_row][mid_col]
            dest = board[to_row][to_col]
            if jumped is None or dest is not None:
                continue
            if _side(jumped) == _side(piece):
                continue
            return True

    return False


# Check if any piece belonging to a side has a jump
def any_jump_for_side(board, side):
    for r in range(len(board)):
        for c in range(len(board[r])):
            piece = board[r][c]
            if piece is None:
                continue
            if piece.split("_")[0] != side:
                continue
            if has_jump_from(board, (r, c)):
                return True
    return False