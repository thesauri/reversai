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
        self.name = "Shallow Blue 4"
        self.author = "Max Ulfves"
        self.color = color

    def opponent(self):
        return "black" if self.color == "white" else "white"


        
    
    def getEval(self, score, board):
        ret = 0
        if self.color == "white":
            ret += score.white - score.black
        else: 
            ret += score.black - score.white
        
        cornerVal = 4

        if board[0][0] == self.color:
            ret += cornerVal
        if board[7][7] == self.color:
            ret += cornerVal
        if board[7][0] == self.color:
            ret += cornerVal
        if board[0][7] == self.color:
            ret += cornerVal
        
        if board[0][0] == self.opponent():
            ret -= cornerVal * 2
        if board[7][7] == self.opponent():
            ret -= cornerVal * 2
        if board[7][0] == self.opponent():
            ret -= cornerVal * 2
        if board[0][7] == self.opponent():
            ret -= cornerVal * 2
        

        return ret
        

    def getPriorited(self, candidates, board, color):
        
        candidatesW_val = map(lambda x: (
            x, 
            self.getEval(calculate_score(  move(board, color, x)  ), move(board, color, x) )
        ), candidates)

        n = min(5, len(candidates))

        candvalSort = sorted(candidatesW_val, key = lambda value: value[1])[:n]
        ret = list(map(lambda x: (
            x[0]
        ), candvalSort))
        #print("LEN: ", len(ret))
        
        return ret

    def min(self, board, depth):
        candidates = playable_moves(board, self.opponent())
        
        map(lambda x: (
            x, 
            self.getEval(calculate_score(  move(board, self.color, x)   ), move(board, self.color, x))
        ), candidates)
        
        if len(candidates) == 1:
            return candidates[0]
            
        def func(c):
            if depth == 0:
                board1 = move(board, self.opponent(), c)
                
                ms = calculate_score(  board1   )
                score = c[1]
                return score
            else:
                
                board1 = move(board, self.opponent(), c)   #AFTER MY MOVE

                if len(playable_moves(board1, self.color)) != 0:
                    board2 = move(board1, self.color, self.max( board1, depth - 1 )) #AFTER OPPONENTS MOVE
                    #/print("B1: ", board1)
                    #print("B2: ", board2)
                    score = self.getEval(calculate_score(board2), board)
                    return score
                else: 
                    return 0
        
        if depth == 0:
            return min(candidates, key = func)
        else : 
            return min(self.getPriorited(candidates, board, self.opponent()), key = func)


    def max(self, board, depth):
        candidates = playable_moves(board, self.color)

        map(lambda x: (
            x, 
            self.getEval(calculate_score(  move(board, self.color, x)   ), board)
        ), candidates)


        if len(candidates) == 1:
            return candidates[0]

        def func(c):
            if depth == 0:
                return c[1]
            else:
                
                board1 = move(board, self.color, c)   #AFTER MY MOVE
                if len(playable_moves(board1, self.opponent())) != 0:
                    board2 = move(board1, self.opponent(), self.min( board1, depth - 1 )) #AFTER OPPONENTS MOVE
                    
                    score = self.getEval(calculate_score(board2), board2)
                    return score
                else: 
                    return 0

        #print(list(map( func, candidates)))
        if depth == 0:
            return max(candidates, key = func)
        else:
            
            #cands = sorted(candidatesW_val, key = lambda value: value[1])[:n]
            return max(self.getPriorited(candidates, board, self.color), key = func)



    def get_move(self, board):
        """
        Called by the game to get a move based on the given game board

        Tip: The game expects the move to be valid. To check move validity, use is_valid_move(board, self.color, (row_index, column_index)).

        board: The game board as a row-column array of "black", "white", or "", i.e. the cell board[3][4] refers to row three and column 4. The rows and columns are indexed from 0 (valid values 0-7).

        Returns: The position to place the disc on as a tuple (row_index, column_index), i.e. (7, 2) for row 7 and column 2. Note that the position *has* to be valid (otherwise the game server will throw an error). Use the is_valid_move from reversi/logic to test whether a move is valid or not.
        """
        depth = 3
        nextMove = self.max(board, depth)

        #eval = calculate_score(move(board, self.color, nextMove))
        #print(eval)
        #print("SCORE: ", self.getEval(eval, move(board, self.color, nextMove)))

        return nextMove
