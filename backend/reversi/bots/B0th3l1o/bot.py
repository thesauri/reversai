import time
from ...logic import is_valid_move, move, playable_moves, has_game_ended, calculate_score
from heapq import heappush, heappop
from typing import List

# Globals

corner_positions = [(0, 0), (0, 7), (7, 0), (7, 7)]
shell_positions = [(2, 2), (2, 3), (2, 4), (2, 5), (3, 2), (3, 5),
                   (4, 2), (4, 5), (5, 2), (5, 3), (5, 4), (5, 5)]
core_positions = [(3, 3), (3, 4), (4, 3), (4, 4)]
corner_value = 50
wall_value = 20
shell_value = 5
core_value = 10
other_value = 1
complexity = 10
max_time = 4.95


# Helper functions


def opposite_color(color: str) -> str:
    if color == "black":
        return "white"
    elif color == "white":
        return "black"
    else:
        return color


def is_corner(pos: (int, int)) -> bool:
    return pos in corner_positions


def is_wall(pos: (int, int)) -> bool:
    for i in range(1, 7):
        if ((pos == (0, i) or pos == (7, i) or
             pos == (i, 0) or pos == (i, 7))):
            return True
    return False


def is_core(pos: (int, int)) -> bool:
    return pos in core_positions


def is_shell(pos: (int, int)) -> bool:
    return pos in shell_positions


def evaluate_pos(pos: (int, int)) -> int:
    if is_corner(pos):
        return core_value
    elif is_wall(pos):
        return wall_value
    elif is_shell(pos):
        return shell_value
    elif is_core(pos):
        return core_value
    else:
        return other_value


def evaluate_board(board, color: str) -> int:
    total = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if board[i][j] == color:
                total -= evaluate_pos((i, j))
            elif board[i][j] == "":
                continue
            else:
                total += evaluate_pos((i, j))
    return total


class Bot:
    """
    Bot

    Bot description: This drunken bot places discs randomly.

    Required properties: name, author
    Required methods: get_move
    """

    def __init__(self, color):
        # Initialize your bot here
        # Name, author, and have to be set
        # Feel free to add your own instance variables
        self.name = "B0th3l1o"
        self.author = "TaTTe & Yann"
        self.color = color

    def get_move(self, board) -> (int, int):
        """
        Called by the game to get a move based on the given game board

        Tip: The game expects the move to be valid. To check move validity, use is_valid_move(board, self.color, (row_index, column_index)).

        board: The game board as a row-column array of "black", "white", or "", i.e. the cell board[3][4] refers to row three and column 4. The rows and columns are indexed from 0 (valid values 0-7).

        Returns: The position to place the disc on as a tuple (row_index, column_index), i.e. (7, 2) for row 7 and column 2. Note that the position *has* to be valid (otherwise the game server will throw an error). Use the is_valid_move from reversi/logic to test whether a move is valid or not.

        """

        start_time = time.time()

        priority_queue = []
        playable = playable_moves(board, self.color)
        length = len(playable)
        pm_frequencies = [0] * length

        """
        Priority Queue Items:
        [0] value: int
        [1] original_move: (int, int)
        [2] board: list[str][str]
        [3] color: str
        [4] complexity: int
        [5] index: int
        """

        i = 0
        for pm in playable:
            new_board = move(board, self.color, pm)
            heappush(priority_queue, (evaluate_board(
                new_board, self.color), pm, new_board, opposite_color(self.color), 0, i))
            i += 1

        while (priority_queue != [] and time.time() - start_time < max_time):
            current = heappop(priority_queue)
            pm_frequencies[current[5]] += 1
            for pm in playable_moves(current[2], current[3]):
                new_board = move(current[2], current[3], pm)
                heappush(priority_queue, (evaluate_board(new_board,
                         current[3]) + current[4], current[1], new_board,
                         opposite_color(current[3]), current[4] + complexity, current[5]))

        best_so_far = playable[0]
        max_so_far = pm_frequencies[0]

        for i in range(1, length):
            if pm_frequencies[i] > max_so_far:
                max_so_far = pm_frequencies[i]
                best_so_far = playable[i]
        return best_so_far
