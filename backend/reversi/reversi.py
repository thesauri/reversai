from .logic import move, default_game_board, is_valid_move
from .helpers import print_board
import json

async def game_session(websocket, path):
    board = default_game_board()
    turn = "black"

    while True:
        await __send_game_state(websocket, board, turn)
        print("Sent game board, waiting for move")
        action = await websocket.recv()
        action = json.loads(action)

        position = (action["rowIndex"], action["columnIndex"])
        new_board = move(board, turn, position)

        if new_board == None:
            print("Invalid move, ignoring")
            continue

        board = new_board
        turn = "black" if turn == "white" else "white"
        print(f"Valid move, {turn}'s turn next")


async def __send_game_state(websocket, board, next_turn):
    game_state = json.dumps({
        "board": board,
        "turn": next_turn
    })
    await websocket.send(game_state)


def test_game():
    board = default_game_board()
    turn = "black"

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
    return board