import random
from ...logic import is_valid_move, move, playable_moves, has_game_ended, calculate_score

# Helper functions
def get_winner(board):
    if has_game_ended(board):
        score = calculate_score(board)
        if score.black > score.white:
            return 'black'
        elif score.white > score.black:
            return 'white'
        else:
            return 'tie'

    return None

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
        self.opponent = 'white' if color == 'black' else 'black'

    def get_move(self, board):
        """
        Called by the game to get a move based on the given game board

        Tip: The game expects the move to be valid. To check move validity, use is_valid_move(board, self.color, (row_index, column_index)).

        board: The game board as a row-column array of "black", "white", or "", i.e. the cell board[3][4] refers to row three and column 4. The rows and columns are indexed from 0 (valid values 0-7).

        Returns: The position to place the disc on as a tuple (row_index, column_index), i.e. (7, 2) for row 7 and column 2. Note that the position *has* to be valid (otherwise the game server will throw an error). Use the is_valid_move from reversi/logic to test whether a move is valid or not.
        """
        # REMOVE THIS AND ADD YOUR OWN CODE HERE
        best_move = None
        best_score = float('-inf')
        for position in playable_moves(board, self.color):
            score = self.evaluate(move(board, self.color, position))
            if score > best_score:
                best_score = score
                best_move = position
        return best_move

    # Number of moves available to player vs moves available to opponent
    def mobility(self, board):
        return len(playable_moves(board, self.color)) - len(playable_moves(board, self.opponent))

    def disc_difference(self, board):
        score = calculate_score(board)
        if self.color == 'white':
            return score.white - score.black
        else:
            return score.black - score.white

    def evaluate(self, board):
        if has_game_ended(board):
            winner = get_winner(board)
            if winner == self.color:
                return float('inf')
            elif winner == self.opponent:
                return float('-inf')
            else:
                return 0

        return self.disc_difference(board) + self.mobility(board)


    

    # ADD ADDITIONAL CLASS METHODS AS NEEDED

