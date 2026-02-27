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