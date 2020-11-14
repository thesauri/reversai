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
        self.name = "Shallow Blue 3"
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

            #print("num: " , numeric)
            if numeric < score:
                bestCandidate = c
                score = numeric
        

        #print("SCORE: " , score)
        return score
        
    
    def getEval(self, score):
        if self.color == "white":
            return score.white - score.black
        else: 
            return score.black - score.white

    def min(self, board, depth):
        candidates = playable_moves(board, self.opponent())

        if len(candidates) == 1:
            return candidates[0]

        def func(c):
            if depth == 0:            
                board1 = move(board, self.opponent(), c)
                
                ms = calculate_score(  board1   )
                score = self.getEval(ms)
                return score
            else:
                board1 = move(board, self.opponent(), c)   #AFTER MY MOVE

                if len(playable_moves(board1, self.color)) != 0:
                    board2 = move(board1, self.color, self.max( board1, depth - 1 )) #AFTER OPPONENTS MOVE
                    #/print("B1: ", board1)
                    #print("B2: ", board2)
                    score = self.getEval(calculate_score(board2))
                    return score
                else: 
                    return 0
        
        return min(candidates, key = func)


    def max(self, board, depth):
        candidates = playable_moves(board, self.color)

        


        if len(candidates) == 1:
            return candidates[0]

        def func(c):
            if depth == 0:
                score = self.getEval(calculate_score(  move(board, self.color, c)   ))
                return score
            else:
                
                board1 = move(board, self.color, c)   #AFTER MY MOVE
                if len(playable_moves(board1, self.opponent())) != 0:
                    board2 = move(board1, self.opponent(), self.min( board1, depth - 1 )) #AFTER OPPONENTS MOVE
                    
                    score = self.getEval(calculate_score(board2))
                    return score
                else: 
                    return 0

        #print(list(map( func, candidates)))
        return max(candidates, key = func)



    def get_move(self, board):
        """
        Called by the game to get a move based on the given game board

        Tip: The game expects the move to be valid. To check move validity, use is_valid_move(board, self.color, (row_index, column_index)).

        board: The game board as a row-column array of "black", "white", or "", i.e. the cell board[3][4] refers to row three and column 4. The rows and columns are indexed from 0 (valid values 0-7).

        Returns: The position to place the disc on as a tuple (row_index, column_index), i.e. (7, 2) for row 7 and column 2. Note that the position *has* to be valid (otherwise the game server will throw an error). Use the is_valid_move from reversi/logic to test whether a move is valid or not.
        """
        depth = 2
        nextMove = self.max(board, depth)

        eval = calculate_score(move(board, self.color, nextMove))
        #print(eval)
        #print("SCORE: ", self.getEval(eval))

        return nextMove

