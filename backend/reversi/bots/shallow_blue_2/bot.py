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
        self.name = "Shallow Blue"
        self.author = "Max Ulfves"
        self.color = color

    def opponent(self):
        return "black" if self.color == "white" else "white"

    def evalScore(self, board):
        score =  calculate_score(board)
        
        #numeric = (score.black - score.white) if self.color == "white" else (score.white - score.black)

        candidates = playable_moves(board, self.opponent() )

        bestCandidate = False
        score = 10000000

        for c in candidates:
            myScore = calculate_score(move(board, self.opponent(), c))
            numeric = (myScore.black - myScore.white) if self.color == "black" else (myScore.white - myScore.black)

            print("num: " , numeric)
            if numeric < score:
                bestCandidate = c
                score = numeric
        

        print("SCORE: " , score)
        return score
        

    def get_move(self, board):
        """
        Called by the game to get a move based on the given game board

        Tip: The game expects the move to be valid. To check move validity, use is_valid_move(board, self.color, (row_index, column_index)).

        board: The game board as a row-column array of "black", "white", or "", i.e. the cell board[3][4] refers to row three and column 4. The rows and columns are indexed from 0 (valid values 0-7).

        Returns: The position to place the disc on as a tuple (row_index, column_index), i.e. (7, 2) for row 7 and column 2. Note that the position *has* to be valid (otherwise the game server will throw an error). Use the is_valid_move from reversi/logic to test whether a move is valid or not.
        """

        candidates = playable_moves(board, self.color)

        def func(c):
             return self.evalScore(move(board, self.color, c))

        return max(candidates, key =  func)

