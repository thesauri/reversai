from copy import copy

class Game:
    def __init__(self):
        self.turn = "black"
        self.board = list(map(lambda x: 8 * [""], 8 * [""]))
        self.board[3][3] = "white"
        self.board[4][3] = "black"
        self.board[3][4] = "black"
        self.board[4][4] = "white"

    def move(self, position):
        """
        Issue a game move

        position: Position as (row_index, column_index)

        Returns: A copy of the new game board. None if the move was invalid."""
        is_out_of_bounds = \
            (position[0] > 7 or position[1] > 7) or \
            (position[0] < 0 or position[1] < 0)

        if is_out_of_bounds or self.board[position[0]][position[1]] != "":
            return None

        self.board[position[0]][position[1]] = self.turn

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
            new_cells_to_flip = self.__cells_to_flip_in_direction(position, direction)
            cells_to_flip.extend(new_cells_to_flip)

        for row_index, column_index in cells_to_flip:
            self.board[row_index][column_index] = self.turn

        self.turn = "white" if self.turn == "black" else "black"

    def __cells_to_flip_in_direction(self, cell, direction):
        """
        cell: (row_index, column_index) of the originating cell

        direction: (delta_row, delta_column) with (1, 0) being down, (-1, 0) being up, and (0, 1) being right

        Returns: A list of array indices to flip"""
        originating_color = self.board[cell[0]][cell[1]]
        if originating_color == "":
            raise ValueError("The originating cell was empty, should have been white or black")

        cells_to_flip = []
        position = (cell[0] + direction[0], cell[1] + direction[1])
        while True:
            is_out_of_bounds_or_blank = \
                (position[0] > 7 or position[1] > 7) or \
                (position[0] < 0 or position[1] < 0) or \
                (self.board[position[0]][position[1]] == "")
            if is_out_of_bounds_or_blank:
                cells_to_flip.clear()
                break

            position_content = self.board[position[0]][position[1]]
            is_matching_color = position_content == originating_color
            if is_matching_color:
                break

            cells_to_flip.append(copy(position))
            position = (position[0] + direction[0], position[1] + direction[1])

        return cells_to_flip

    def print_board(self):
        # Print the board
        for row_index, row in enumerate(self.board):
            print(f"{row_index} |", end="")
            for cell_content in row:
                print_styles = {
                    "black": "b ",
                    "white": "w ",
                    "": "- "
                }
                cell = print_styles[cell_content]
                print(cell, end="")
            print("|")
        # Print the bottom column indices (0 to 7)
        print("   ", end="")
        for column_index, _ in enumerate(self.board):
            print(f"{column_index} ", end="")
        print("")
