current_side = "light"

def side_to_move():
	return current_side

def reset_turns():
	global current_side
	current_side = "light"

def switch_turn():
	global current_side
	current_side = "light" if current_side == "dark" else "dark"

def piece_belongs_to_side(piece, side):
	if piece is None:
		return False
	return piece.startswith(side + "_")