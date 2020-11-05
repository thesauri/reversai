import random
from ..logic import is_valid_move, move

class Oth3lloGrindr2000:
    """
    Sample Reversibot

    This drunken bot places discs randomly.

    Required properties: name, author 
    Required methods: get_move
    """
    def __init__(self, color):
        # Initialize your bot here
        self.name = "0th3ll0GRINDR2000"
        self.author = "wotlol u sammoa"
        self.color = color
        pass

    def get_move(self, board):
        """
        board: The game board as a row-column array of "black", "white", or "", i.e. the cell board[3][4] refers to row three and column 4. The rows and columns are indexed from 0 (valid values 0-7).

        Returns: The position to place the disc as a tuple (row_index, column_index), i.e. (7, 2) for row 7 and column 2. Note that the position *has* to be valid (otherwise the game server will throw an error). Use the is_valid_move from reversi/logic to test whether a move is valid or not.
        """
        while True:
            row_index = random.randint(0, 7)
            column_index = random.randint(0, 7)
            position = (row_index, column_index)
            if is_valid_move(board, self.color, position):
                return position

