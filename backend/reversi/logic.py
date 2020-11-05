from copy import copy, deepcopy

def default_game_board():
    board = list(map(lambda x: 8 * [""], 8 * [""]))
    board[3][3] = "white"
    board[4][3] = "black"
    board[3][4] = "black"
    board[4][4] = "white"
    return board


def is_valid_move(board, turn, position):
    """
    Test whether a game move is valid

    board: The game board as a row-column array of "black", "white", or ""

    turn: "black" or "white"

    position: Position as (row_index, column_index)

    Returns: True or False
    """
    is_valid = move(board, turn, position) != None
    return is_valid

def move(board, turn, position):
    """
    Issue a game move

    board: The game board as a row-column array of "black", "white", or ""

    turn: "black" or "white"

    position: Position as (row_index, column_index)

    Returns: A copy of the new game board. None if the move was invalid."""
    board = deepcopy(board)

    is_out_of_bounds = \
        (position[0] > 7 or position[1] > 7) or \
        (position[0] < 0 or position[1] < 0)

    if is_out_of_bounds or board[position[0]][position[1]] != "":
        return None

    board[position[0]][position[1]] = turn

    directions = [
        [1, 0],     # South
        [1, -1],    # South west
        [0, -1],    # West
        [-1, -1],   # North west
        [-1, 0],    # North
        [-1, 1],    # North east
        [0, 1],     # East
        [1, 1]      # South east
    ]
    cells_to_flip = []
    for direction in directions:
        new_cells_to_flip = __cells_to_flip_in_direction(board, position, direction)
        cells_to_flip.extend(new_cells_to_flip)

    if len(cells_to_flip) == 0:
        return None

    for row_index, column_index in cells_to_flip:
        board[row_index][column_index] = turn

    return board

def __cells_to_flip_in_direction(board, cell, direction):
    """
    cell: (row_index, column_index) of the originating cell

    board: The game board as a row-column array of "black", "white", or ""

    direction: (delta_row, delta_column) with (1, 0) being down, (-1, 0) being up, and (0, 1) being right

    Returns: A list of array indices to flip"""
    originating_color = board[cell[0]][cell[1]]
    if originating_color == "":
        raise ValueError("The originating cell was empty, should have been white or black")

    cells_to_flip = []
    position = (cell[0] + direction[0], cell[1] + direction[1])
    while True:
        is_out_of_bounds_or_blank = \
            (position[0] > 7 or position[1] > 7) or \
            (position[0] < 0 or position[1] < 0) or \
            (board[position[0]][position[1]] == "")
        if is_out_of_bounds_or_blank:
            cells_to_flip.clear()
            break

        position_content = board[position[0]][position[1]]
        is_matching_color = position_content == originating_color
        if is_matching_color:
            break

        cells_to_flip.append(copy(position))
        position = (position[0] + direction[0], position[1] + direction[1])

    return cells_to_flip
