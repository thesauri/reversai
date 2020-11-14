import random
from ...logic import is_valid_move, move, playable_moves, has_game_ended, calculate_score

# Do NOT rename this class
class Bot:
    """
    Bot

    Bot description: Krister-Samuel is a sneaky bot that will try to win you

    Required properties: name, author 
    Required methods: get_move
    """
    def __init__(self, color):
        # Initialize your bot here
        # Name, author, and have to be set
        # Feel free to add your own instance variables
        self.name = "Krister-Samuel"
        self.author = "Vicrid"
        self.color = color

    def get_move(self, board):
        """
        Called by the game to get a move based on the given game board

        Tip: The game expects the move to be valid. To check move validity, use is_valid_move(board, self.color, (row_index, column_index)).

        board: The game board as a row-column array of "black", "white", or "", i.e. the cell board[3][4] refers to row three and column 4. The rows and columns are indexed from 0 (valid values 0-7).

        Returns: The position to place the disc on as a tuple (row_index, column_index), i.e. (7, 2) for row 7 and column 2. Note that the position *has* to be valid (otherwise the game server will throw an error). Use the is_valid_move from reversi/logic to test whether a move is valid or not.
        """
        # REMOVE THIS AND ADD YOUR OWN CODE HERE
        while True:
            moves=playable_moves(board,self.color)
            ascore=[]
            if self.color == 'black':
                anticolor='white'
            else:
                anticolor='black'

            for a in moves:
                ri=a[0]
                ci=a[1]
                pos=(ri,ci)
                aboard=move(board,self.color,pos)
                bmoves=playable_moves(aboard,anticolor)
                bscorevector=[0]
                for b in bmoves:
                    bri=b[0]
                    bci=b[1]
                    bpos=(bri,bci)
                    bboard=move(aboard,anticolor,bpos)
                    bscore=calculate_score(bboard)
                    bscorevector.append(bscore.black)
                score=calculate_score(aboard)
                ascorea=score.white-2*(max(bscorevector))
                ascore.append([ascorea,pos])
            ascore.sort(reverse=1)
            #row_index = random.randint(0, 7)
            #column_index = random.randint(0, 7)
            #position = (row_index, column_index)
            for b in ascore:
                if is_valid_move(board, self.color, b[1]):
                    return b[1]

    # ADD ADDITIONAL CLASS METHODS AS NEEDED
