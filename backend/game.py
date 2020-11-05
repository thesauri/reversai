from game_logic import move, default_game_board, is_valid_move
from helpers import print_board

def play_game():
    board = default_game_board()
    turn = "black"

    print()
    board = move(board, turn, (2, 3))
    print_board(board)

    turn = "white"
    board = move(board, turn, (5, 3))
    print_board(board)

    turn = "black"
    board = move(board, turn, (1, 3))
    print_board(board)

    turn = "white"
    board = move(board, turn, (0, 3))
    print_board(board)
