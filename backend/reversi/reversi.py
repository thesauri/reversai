import asyncio
from .logic import move, default_game_board, is_valid_move
from .helpers import print_board
import json

async def bot_vs_bot_session(websocket, black_bot, white_bot):
    board = default_game_board()
    turn = "black"

    while True:
        await __send_game_state(websocket, board, turn)

        print(f"{turn}'s turn to play")
        bot = black_bot if turn == "black" else white_bot
        position = bot.get_move(board)
        new_board = move(board, turn, position)
        __raise_exception_on_invalid_move(new_board)
        board = new_board
        turn = __next_turn(turn)

        await asyncio.sleep(1.5)


async def human_vs_bot_session(websocket, is_bot_first, bot):
    board = default_game_board()
    turn = "black"

    if is_bot_first:
        position = bot.get_move(board)
        new_board = move(board, turn, position)
        __raise_exception_on_invalid_move(new_board)
        board = new_board
        turn = __next_turn(turn)

    while True:
        # Human playing
        await __send_game_state(websocket, board, turn)
        print("Sent game board, waiting for move from human")

        action = await websocket.recv()
        action = json.loads(action)

        position = (action["rowIndex"], action["columnIndex"])
        new_board = move(board, turn, position)

        if new_board == None:
            print("Invalid move, ignoring")
            continue

        board = new_board
        turn = __next_turn(turn)
        print(f"Valid move, bot's turn next")
        await __send_game_state(websocket, board, turn)
        await asyncio.sleep(2)

        # Bot playing
        position = bot.get_move(board)
        new_board = move(board, turn, position)
        __raise_exception_on_invalid_move(new_board)
        board = new_board
        turn = __next_turn(turn)


async def human_vs_human_session(websocket):
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
        turn = __next_turn(turn)
        print(f"Valid move, {turn}'s turn next")


async def __send_game_state(websocket, board, next_turn):
    game_state = json.dumps({
        "board": board,
        "turn": next_turn
    })
    await websocket.send(game_state)

def __raise_exception_on_invalid_move(new_board):
    if new_board == None:
        raise ValueError("Invalid move from bot, BYE!")


def __next_turn(current_turn):
    return "black" if current_turn == "white" else "white"

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