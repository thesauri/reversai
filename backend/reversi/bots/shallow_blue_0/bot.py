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
        self.name = "Shallow Blue Beta"
        self.author = "Max Ulfves"
        self.color = color

    def moves(self, board):
        candidates = set()
        opCol = "white"
        for row in range(0, 7):
            for col in range(0,7):
                if board[row][col] == opCol:
                    #foreach surrounding tile
                    for rn in range(max(row - 1, 0), min(row + 2, 7)):
                        for cn in range(max(col - 1, 0), min(col + 2, 7)):
                            position = (rn, cn)
                            if board[rn][cn] == "" and is_valid_move(board, self.color, position) :
                                candidates.add( position )
        return candidates

    def get_move(self, board):
        """
        Called by the game to get a move based on the given game board

        Tip: The game expects the move to be valid. To check move validity, use is_valid_move(board, self.color, (row_index, column_index)).

        board: The game board as a row-column array of "black", "white", or "", i.e. the cell board[3][4] refers to row three and column 4. The rows and columns are indexed from 0 (valid values 0-7).

        Returns: The position to place the disc on as a tuple (row_index, column_index), i.e. (7, 2) for row 7 and column 2. Note that the position *has* to be valid (otherwise the game server will throw an error). Use the is_valid_move from reversi/logic to test whether a move is valid or not.
        """
        # REMOVE THIS AND ADD YOUR OWN CODE HERE

        candidates = playable_moves(board, self.color)
        
        bestCandidate = candidates[0]
        score = calculate_score(move(board, self.color, bestCandidate))

        for c in candidates:
            myScore = calculate_score(move(board, self.color, bestCandidate))
            if myScore > score:
                bestCandidate = c
                score = myScore

        return bestCandidate


    # ADD ADDITIONAL CLASS METHODS AS NEEDED
