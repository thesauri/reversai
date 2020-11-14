import asyncio
from collections import namedtuple
from copy import deepcopy, copy
from datetime import datetime
from .logic import move, default_game_board, is_valid_move, playable_moves, calculate_score, has_game_ended
from .printing import print_board
import json
import websockets as ws

PreviousAction = namedtuple("PreviousAction", "old_board turn position")

async def bot_vs_bot_session(websockets, black_bot, white_bot, minimum_delay=3, headless=False):
    board = default_game_board()
    turn = "black"
    previous_action = None
    await __send_game_state(websockets, board, turn, black_bot=black_bot, white_bot=white_bot, headless=headless)
    await asyncio.sleep(minimum_delay)

    while True:
        print(f"{turn}'s turn to play")
        bot = black_bot if turn == "black" else white_bot
        (position, delta_time) = __get_move_with_delta_time(bot, board)
        print(f"Time taken: {delta_time} s")
        new_board = move(board, turn, position)
        __raise_exception_on_invalid_move(new_board)

        previous_action = PreviousAction(board, turn, position)
        board = new_board
        turn = __next_turn(board, turn)
        is_win = has_game_ended(board)

        await __send_game_state(
            websockets,
            board,
            turn,
            black_bot=black_bot,
            white_bot=white_bot,
            previous_action=previous_action,
            headless=headless,
            delta_time=delta_time
        )

        if is_win:
            break
        await asyncio.sleep(minimum_delay)

    print("Game over!")
    await __send_win_state(websockets, board, turn, previous_action, headless=headless)
    score = calculate_score(board)
    return score

async def human_vs_bot_session(websocket, is_bot_first, bot, minimum_delay=3):
    board = default_game_board()
    turn = "black"
    previous_action = None

    await __send_game_state(
        websocket,
        board,
        turn,
        black_bot=bot if is_bot_first else None,
        white_bot=None if is_bot_first else bot,
    )

    if is_bot_first:
        await asyncio.sleep(minimum_delay)
        (position, delta_time) = __get_move_with_delta_time(bot, board)
        print(f"Time taken: {delta_time} s")
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
            delta_time=delta_time,
            previous_action=None
        )


    while True:
        # Human playing
        print("Waiting for human move")
        time_before = datetime.now()
        action = await websocket.recv()
        action = json.loads(action)
        time_after = datetime.now()
        delta_time = __delta_time_in_seconds(time_before, time_after)

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

        await __send_game_state(websocket,
            board,
            turn,
            black_bot=bot if is_bot_first else None,
            white_bot=None if is_bot_first else bot,
            previous_action=previous_action,
            delta_time=delta_time
        )

        print(f"Valid move, bot's turn next")
        await asyncio.sleep(minimum_delay)

        # Bot playing
        (position, delta_time) = __get_move_with_delta_time(bot, board)
        print(f"Time taken: {delta_time} s")
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
            delta_time=delta_time,
            previous_action=previous_action
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

        time_before = datetime.now()
        action = await websocket.recv()
        action = json.loads(action)
        time_after = datetime.now()
        delta_time = __delta_time_in_seconds(time_before, time_after)

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

        await __send_game_state(websocket, board, turn, previous_action=previous_action, delta_time=delta_time)
        print(f"Valid move, {turn}'s turn next")

    print("Game over!")
    await __send_win_state(websocket, board, turn, previous_action)


async def __send_game_state(websockets, board, next_turn, black_bot=None, white_bot=None, previous_action=None, delta_time=None, headless=False):
    game_state = {
        "newBoard": board,
        "turn": next_turn,
        "score": calculate_score(board)
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
    if delta_time != None:
        game_state["deltaTime"] = delta_time

    if headless:
        print_board(board)
    else:
        stringified_game_state = json.dumps(game_state)
        if isinstance(websockets, list):
            for websocket in websockets:
                try:
                    await websocket.send(stringified_game_state)
                except ws.exceptions.ConnectionClosedError:
                    pass
        else:
            await websockets.send(stringified_game_state)

def __get_move_with_delta_time(bot, board):
    time_before = datetime.now()
    position = bot.get_move(board)
    time_after = datetime.now()
    delta_time = __delta_time_in_seconds(time_before, time_after)
    MoveWithTime = namedtuple("MoveWithTime", "position delta_time")
    return MoveWithTime(position, delta_time)

def __delta_time_in_seconds(time_before, time_after):
    return (time_after - time_before).seconds + round((time_after - time_before).microseconds / 1000000, 2)

async def __send_win_state(websockets, board, turn, previous_action, headless=False):
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
        if isinstance(websockets, list):
            for websocket in websockets:
                try:
                    await websocket.send(stringified_win_state)
                except ws.exceptions.ConnectionClosedError:
                    pass
        else:
            await websockets.send(stringified_game_state)


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