board_size = 8
dark_square = "dark"
light_square = "light"

#Check if a square is dark by coordinates
def is_dark_square(row, col):
    return (row + col) % 2 == 0

#Create starting board layout with men on dark squares
def create_initial_board():
    game_board = [[None for _ in range(board_size)] for _ in range(board_size)]

    for row in range(board_size):
        for col in range(board_size):
            if not is_dark_square(row, col):
                continue

            if row < 3:
                game_board[row][col] = "dark_man"
            elif row > 4:
                game_board[row][col] = "light_man"

    return game_board