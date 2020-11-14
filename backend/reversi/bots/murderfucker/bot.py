import random
from ...logic import is_valid_move, move, playable_moves, has_game_ended, calculate_score
import time
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
        self.name = "Murderfucker"
        self.author = "killmaster200 & Bob"
        self.color = color
        self.turns = ["black", "white"]

    def get_move(self, board):
        """
        Called by the game to get a move based on the given game board

        Tip: The game expects the move to be valid. To check move validity, use is_valid_move(board, self.color, (row_index, column_index)).

        board: The game board as a row-column array of "black", "white", or "", i.e. the cell board[3][4] refers to row three and column 4. The rows and columns are indexed from 0 (valid values 0-7).

        Returns: The position to place the disc on as a tuple (row_index, column_index), i.e. (7, 2) for row 7 and column 2. Note that the position *has* to be valid (otherwise the game server will throw an error). Use the is_valid_move from reversi/logic to test whether a move is valid or not.
        """
        turn = 1 
        if self.color == "black":
            turn = 0
            #print(self.traverse_game_tree(board, turn = 0, level = 1, max_level = 2))
            #print(self.traverse_game_tree(board, turn = 1, level = 1, max_level = 2))

        scores = []
        playable = playable_moves(board, self.turns[turn])

        for candidate_move in playable:
            if candidate_move == (0, 0) or candidate_move == (0, 7) or candidate_move == (7, 0) or candidate_move == (7, 7):
                return candidate_move 

        start_time = time.time()
        for candidate_move in playable:
            score = 0
            next_board = move(board, self.turns[turn], candidate_move)
            score += self.traverse_game_tree(next_board, abs(turn - 1), level = 1, start_time = start_time,  max_level = 4)
            #score += self.traverse_game_tree_MCE(next_board, abs(turn - 1), level = 1, start_time = start_time, max_level = 3)

            #print("Score of move {} is: {}".format(candidate_move, score))
            scores.append(score)

        return playable[scores.index(max(scores))]
        

    # ADD ADDITIONAL CLASS METHODS AS NEEDED
    def traverse_game_tree(self, board, turn, level, start_time, max_level = 3):
        #print("Current turn is {}: {}".format(self.turns[turn], turn))
        if level >= max_level or time.time() - start_time > 4.5:
            scores = calculate_score(board)
            if self.color == "black":
                return scores.black - scores.white 
            else:
                return scores.white - scores.black

        playable = playable_moves(board, self.turns[turn])
        #move_scores = {}
        tot_score = 0

        for candidate_move in playable:
            next_board = move(board, self.turns[turn], candidate_move)
            tot_score += self.traverse_game_tree(next_board, abs(turn - 1), random.randint(level+1, level+2), max_level)
            #print("Total_score is: {}".format(tot_score))

        return tot_score

    def traverse_game_tree_MCE(self, board, turn, level, start_time, max_level = 3):
        #print("Current turn is {}: {}".format(self.turns[turn], turn))
        if level == max_level or time.time() - start_time > 4.5:
            score = self.calculate_score_MCE(board, turn)
            return score

        playable = playable_moves(board, self.turns[turn])
        #move_scores = {}
        tot_score = 0

        for candidate_move in playable:
            next_board = move(board, self.turns[turn], candidate_move)
            tot_score += self.traverse_game_tree_MCE(next_board, abs(turn - 1), level+1, start_time, max_level)
            #print("Total_score is: {}".format(tot_score))

        return tot_score

    def calculate_score_MCE(self, board, turn):
        edge_pieces = 0
        corner_pieces = 0

        playable = len(playable_moves(board, self.turns[turn]))

        for (i, j) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
            if board[i][j] == self.turns[turn]:
                corner_pieces += 1
        
        for i in [0, 7]:
            for j in range(1, 7):
                #print(board[i][j])
                if board[i][j] == self.turns[turn]:
                    edge_pieces += 1

        for j in [0, 7]:
            for i in range(1, 7):
                if board[i][j] == self.turns[turn]:
                    edge_pieces += 1

        if board[0][1] == self.turns[turn] and board[0][0] != self.turns[turn]:
            edge_pieces = 0
        if board[1][0] == self.turns[turn] and board[0][0] != self.turns[turn]:
            edge_pieces = 0
        if board[0][6] == self.turns[turn] and board[0][7] != self.turns[turn]:
            edge_pieces = 0
        if board[1][7] == self.turns[turn] and board[0][7] != self.turns[turn]:
            edge_pieces = 0
        if board[6][0] == self.turns[turn] and board[7][0] != self.turns[turn]:
            edge_pieces = 0
        if board[7][1] == self.turns[turn] and board[7][0] != self.turns[turn]:
            edge_pieces = 0
        if board[7][6] == self.turns[turn] and board[7][7] != self.turns[turn]:
            edge_pieces = 0
        if board[6][7] == self.turns[turn] and board[7][7] != self.turns[turn]:
            edge_pieces = 0

        if self.turns[turn] == self.color:
            return playable + 1.5 * corner_pieces + 0.5 * edge_pieces
        else:
            return -(playable + 1.5 * corner_pieces + 0.5 * edge_pieces)



