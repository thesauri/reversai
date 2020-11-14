import random
from ...logic import is_valid_move, move, playable_moves, has_game_ended, calculate_score

# Do NOT rename this class
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
        self.name = "speedrun"
        self.author = "darra boi"
        self.color = color

    def get_move(self, board):
        """
        Called by the game to get a move based on the given game board

        Tip: The game expects the move to be valid. To check move validity, use is_valid_move(board, self.color, (row_index, column_index)).

        board: The game board as a row-column array of "black", "white", or "", i.e. the cell board[3][4] refers to row three and column 4. The rows and columns are indexed from 0 (valid values 0-7).

        Returns: The position to place the disc on as a tuple (row_index, column_index), i.e. (7, 2) for row 7 and column 2. Note that the position *has* to be valid (otherwise the game server will throw an error). Use the is_valid_move from reversi/logic to test whether a move is valid or not.
        """
        # REMOVE THIS AND ADD YOUR OWN CODE HERE
        moves = playable_moves(board, self.color)

        bueno = [(0,0), (0,7), (7,0), (7,7),(0,2), (2,0), (5,0), (0,5), (2,7),(7,2),(5,7),(7,5),(2,2),(2,5), (5,2), (5,5)]
        no_bueno = [(0,1), (1,0), (1,1), (6,7), (7,6), (6,6), (6,0), (6,1), (7,1),(0,6),(1,6),(1,7)]
        for c in bueno:
            if c in moves:
                return c
        ok = []
        for m in moves:
            if not m in no_bueno:
                ok.append(m)
        best = []
        for m in ok:
            if m[0] != 1 and m[1] != 1 and m[0] != 6 and m[1] != 6:
                best.append(m)
        if len(best) > 0:
            m = random.choice(best)
            return m
        if len(ok) > 0:
            m = random.choice(ok)
            return m
        if len(moves) > 0:
            return random.choice(moves)