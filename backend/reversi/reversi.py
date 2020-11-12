import asyncio
from collections import namedtuple
from copy import deepcopy
from .logic import move, default_game_board, is_valid_move, playable_moves, calculate_score, has_game_ended
from .helpers import print_board
import json

PreviousAction = namedtuple("PreviousAction", "old_board turn position")

async def bot_vs_bot_session(websocket, black_bot, white_bot, minimum_delay=3, headless=False):
    board = default_game_board()
    turn = "black"
    previous_action = None
    await __send_game_state(websocket, board, turn, black_bot=black_bot, white_bot=white_bot, headless=headless)
    await asyncio.sleep(minimum_delay)

    while True:
        print(f"{turn}'s turn to play")
        bot = black_bot if turn == "black" else white_bot
        position = bot.get_move(board)
        new_board = move(board, turn, position)
        __raise_exception_on_invalid_move(new_board)

        previous_action = PreviousAction(board, turn, position)
        board = new_board
        turn = __next_turn(board, turn)
        is_win = has_game_ended(board)

        await __send_game_state(
            websocket,
            board,
            turn,
            black_bot=black_bot,
            white_bot=white_bot,
            previous_action=previous_action,
            headless=headless
        )

        if is_win:
            break
        await asyncio.sleep(minimum_delay)

    print("Game over!")
    await __send_win_state(websocket, board, turn, previous_action, headless=headless)
    score = calculate_score(board)
    return score

async def human_vs_bot_session(websocket, is_bot_first, bot, minimum_delay=3):
    board = default_game_board()
    turn = "black"
    previous_action = None

    await __send_game_state(websocket,
        board,
        turn,
        black_bot=bot if is_bot_first else None,
        white_bot=None if is_bot_first else bot,
    )

    if is_bot_first:
        await asyncio.sleep(minimum_delay)
        position = bot.get_move(board)
        new_board = move(board, turn, position)
        __raise_exception_on_invalid_move(new_board)

        previous_action = PreviousAction(board, turn, position)
        board = new_board
        turn = __next_turn(board, turn)

        await __send_game_state(websocket,
            board,
            turn,
            black_bot=bot if is_bot_first else None,
            white_bot=None if is_bot_first else bot,
        )


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
        turn = __next_turn(board, turn)

        is_win = has_game_ended(board)
        if is_win:
            break

        print(f"Valid move, bot's turn next")
        await asyncio.sleep(minimum_delay)

        # Bot playing
        position = bot.get_move(board)
        new_board = move(board, turn, position)
        __raise_exception_on_invalid_move(new_board)

        previous_action = PreviousAction(board, turn, position)
        board = new_board
        turn = __next_turn(board, turn)
        is_win = has_game_ended(board)

        if is_win:
            break


        await __send_game_state(websocket,
            board,
            turn,
            black_bot=bot if is_bot_first else None,
            white_bot=None if is_bot_first else bot,
        )

    print("Game over!")
    await __send_win_state(websocket, board, turn, previous_action)


async def human_vs_human_session(websocket):
    board = default_game_board()
    turn = "black"
    previous_action = None
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
        turn = __next_turn(board, turn)
        is_win = has_game_ended(board)

        if is_win:
            break

        await __send_game_state(websocket, board, turn, previous_action=previous_action)
        print(f"Valid move, {turn}'s turn next")

    print("Game over!")
    await __send_win_state(websocket, board, turn, previous_action)


async def __send_game_state(websocket, board, next_turn, black_bot=None, white_bot=None, previous_action=None, headless=False):
    game_state = {
        "newBoard": board,
        "turn": next_turn
    }
    if previous_action != None:
        intermediate_board = deepcopy(previous_action.old_board)
        intermediate_board[previous_action.position[0]][previous_action.position[1]] = previous_action.turn
        game_state["intermediateBoard"] = intermediate_board
        game_state["latestPosition"] = previous_action.position
    if black_bot != None:
        game_state["black"] = {
            "name": black_bot.name,
            "author": black_bot.author
        }
    if white_bot != None:
        game_state["white"] = {
            "name": white_bot.name,
            "author": white_bot.author
        }

    if headless:
        print_board(board)
    else:
        stringified_game_state = json.dumps(game_state)
        await websocket.send(stringified_game_state)

async def __send_win_state(websocket, board, turn, previous_action, headless=False):
    intermediate_board = deepcopy(previous_action.old_board)
    intermediate_board[previous_action.position[0]][previous_action.position[1]] = previous_action.turn

    score = calculate_score(board)
    winner = "black" if score.black > score.white else ("tie" if score.black == score.white else "white")

    win_state = {
        "intermediateBoard": intermediate_board,
        "newBoard": board,
        "turn": turn,
        "winner": winner
    }

    if headless:
        print(f"The winner is: {winner}")
    else:
        stringified_win_state = json.dumps(win_state)
        await websocket.send(stringified_win_state)


def __raise_exception_on_invalid_move(new_board):
    if new_board == None:
        raise ValueError("Invalid move from bot, BYE!")


def __next_turn(board, current_turn):
    next_turn = "black" if current_turn == "white" else "white"
    if len(playable_moves(board, next_turn)) > 0:
        return next_turn
    else:
        return current_turn

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