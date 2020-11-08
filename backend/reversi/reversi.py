import asyncio
from collections import namedtuple
from copy import deepcopy
from .logic import move, default_game_board, is_valid_move
from .helpers import print_board
import json

PreviousAction = namedtuple("PreviousAction", "old_board turn position")

async def bot_vs_bot_session(websocket, black_bot, white_bot):
    board = default_game_board()
    turn = "black"
    await __send_game_state(websocket, board, turn)
    await asyncio.sleep(3)


    while True:
        print(f"{turn}'s turn to play")
        bot = black_bot if turn == "black" else white_bot
        position = bot.get_move(board)
        new_board = move(board, turn, position)
        __raise_exception_on_invalid_move(new_board)

        previous_action = PreviousAction(board, turn, position)
        board = new_board
        turn = __next_turn(turn)

        await __send_game_state(websocket, board, turn, previous_action=previous_action)
        await asyncio.sleep(3)


async def human_vs_bot_session(websocket, is_bot_first, bot):
    board = default_game_board()
    turn = "black"

    await __send_game_state(websocket, board, turn)

    if is_bot_first:
        await asyncio.sleep(3)
        position = bot.get_move(board)
        new_board = move(board, turn, position)
        __raise_exception_on_invalid_move(new_board)

        previous_action = PreviousAction(board, turn, position)
        board = new_board
        turn = __next_turn(turn)

        await __send_game_state(websocket, board, turn, previous_action=previous_action)

    while True:
        # Human playing
        print("Waiting for human move")
        action = await websocket.recv()
        action = json.loads(action)

        position = (action["rowIndex"], action["columnIndex"])
        new_board = move(board, turn, position)

        if new_board == None:
            print("Invalid move, ignoring")
            continue

        previous_action = PreviousAction(board, turn, position)
        board = new_board
        turn = __next_turn(turn)
        print(f"Valid move, bot's turn next")
        await __send_game_state(websocket, board, turn, previous_action=previous_action)
        await asyncio.sleep(3)

        # Bot playing
        position = bot.get_move(board)
        new_board = move(board, turn, position)
        __raise_exception_on_invalid_move(new_board)

        previous_action = PreviousAction(board, turn, position)
        board = new_board
        turn = __next_turn(turn)
        await __send_game_state(websocket, board, turn, previous_action=previous_action)


async def human_vs_human_session(websocket):
    board = default_game_board()
    turn = "black"
    await __send_game_state(websocket, board, turn)

    while True:
        print("Sent game board, waiting for move")

        action = await websocket.recv()
        action = json.loads(action)

        position = (action["rowIndex"], action["columnIndex"])
        new_board = move(board, turn, position)

        if new_board == None:
            print("Invalid move, ignoring")
            continue

        previous_action = PreviousAction(board, turn, position)
        board = new_board
        turn = __next_turn(turn)
        await __send_game_state(websocket, board, turn, previous_action=previous_action)
        print(f"Valid move, {turn}'s turn next")


async def __send_game_state(websocket, board, next_turn, previous_action=None):
    game_state = {
        "newBoard": board,
        "turn": next_turn
    }
    if previous_action != None:
        intermediate_board = deepcopy(previous_action.old_board)
        intermediate_board[previous_action.position[0]][previous_action.position[1]] = previous_action.turn
        game_state["intermediateBoard"] = intermediate_board

    stringified_game_state = json.dumps(game_state)
    await websocket.send(stringified_game_state)

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