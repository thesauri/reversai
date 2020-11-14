import random
from ...logic import is_valid_move, move, playable_moves, has_game_ended, calculate_score
import operator

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
        self.name = "0th3ll0GRINDR2000"
        self.author = "wotlol u sammoa"
        self.color = color

    def get_move(self, board):
        """
        Called by the game to get a move based on the given game board

        Tip: The game expects the move to be valid. To check move validity, use is_valid_move(board, self.color, (row_index, column_index)).

        board: The game board as a row-column array of "black", "white", or "", i.e. the cell board[3][4] refers to row three and column 4. The rows and columns are indexed from 0 (valid values 0-7).

        Returns: The position to place the disc on as a tuple (row_index, column_index), i.e. (7, 2) for row 7 and column 2. Note that the position *has* to be valid (otherwise the game server will throw an error). Use the is_valid_move from reversi/logic to test whether a move is valid or not.
        """
        # REMOVE THIS AND ADD YOUR OWN CODE HERE
        color_idx = 0 if self.color == "black" else 1
        op_color = "white" if self.color == "black" else "black"
        
        moves = playable_moves(board, self.color)
        move_boards = [(m, move(board, self.color, m)) for m in moves]

        scores = {}
        for (m, b) in move_boards:
            op_moves = playable_moves(b, op_color)

            op_move_boards = [(o_m, move(b, op_color, o_m)) for o_m in op_moves]
            move_scores = [calculate_score(m_b[1])[color_idx] for m_b in op_move_boards]
            if len(move_scores) == 0:
                return m
            scores[m] = float(sum(move_scores))/len(move_scores)

        return max(scores.items(), key=operator.itemgetter(1))[0]

    # ADD ADDITIONAL CLASS METHODS AS NEEDED
