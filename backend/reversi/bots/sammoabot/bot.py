import random
from ...logic import is_valid_move, move, playable_moves, has_game_ended, calculate_score
from copy import deepcopy
import time
import random
import pickle

SAVE_MOVES = False
FILENAME = 'precalc_moves.pickle'
board_weights = [
    [1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, 1.0],
    [0.0, 0.0, 0.1, 0.1, 0.1, 0.1, 0.0, 0.0],
    [0.7, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.7],
    [0.5, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.5],
    [0.5, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.5],
    [0.7, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.7],
    [0.0, 0.0, 0.1, 0.1, 0.1, 0.1, 0.0, 0.0],
    [1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, 1.0],
]

corners = [(0,0), (0,7), (7,0), (7,7)]

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

def get_symmetries(board):
    board = deepcopy(board)
    symmetries = {
    }
    for i in range(1,4):
        temp = board
        for _ in range(i):
            temp = list(zip(*temp[::-1]))
        symmetries[f'rotation{i}'] = temp
    symmetries['horizontal_mirror'] = board[::-1]
    symmetries['vertical_mirror'] = [r[::-1] for r in board]
    return symmetries

def reverse_symmetry(position, symmetry):
    normal_board =  [[(i, j) for j in range(8)] for i in range(8)]
    altered_board = None
    if 'rotation' in symmetry:
        temp = normal_board
        for _ in range(int(symmetry[-1])):
            temp = list(zip(*temp[::-1]))
        altered_board = temp
    elif symmetry == 'horizontal_mirror':
        altered_board = normal_board[::-1]
    elif symmetry == 'vertical_mirror':
        altered_board = [r[::-1] for r in board]
    return altered_board[position[0]][position[1]]

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
        self.name = "sammoabot"
        self.author = "Samuel"
        self.color = color
        self.opponent = 'white' if color == 'black' else 'black'
        self.searched_boards = {'white': {}, 'black': {}}
        self.board_lookups = 0

    def load_moves(self):
        try:
            with open(FILENAME, 'rb') as f:
                searched_boards = pickle.load(f)
            return searched_boards
        except:
            return {'white': {}, 'black': {}} 

    def get_move(self, board):
        """
        Called by the game to get a move based on the given game board

        Tip: The game expects the move to be valid. To check move validity, use is_valid_move(board, self.color, (row_index, column_index)).

        board: The game board as a row-column array of "black", "white", or "", i.e. the cell board[3][4] refers to row three and column 4. The rows and columns are indexed from 0 (valid values 0-7).

        Returns: The position to place the disc on as a tuple (row_index, column_index), i.e. (7, 2) for row 7 and column 2. Note that the position *has* to be valid (otherwise the game server will throw an error). Use the is_valid_move from reversi/logic to test whether a move is valid or not.
        """
        the_move = self.minimax_search(board)
        if not the_move:
            the_move = playable_moves(board, self.color)[0]

        if SAVE_MOVES:
            with open(FILENAME, 'wb') as f:
                pickle.dump(self.searched_boards, f)

        return the_move
        
    # Number of moves available to player vs moves available to opponent
    def mobility(self, board):
        return len(playable_moves(board, self.color)) / (len(playable_moves(board, self.opponent)) + 1)

    def disc_difference(self, board):
        score = calculate_score(board)
        if self.color == 'white':
            return score.white / (score.black + 1)
        else:
            return score.black / (score.white + 1)

    def evaluate(self, board, position):
        if has_game_ended(board):
            winner = get_winner(board)
            if winner == self.color:
                return float('inf')
            elif winner == self.opponent:
                return float('-inf')
            else:
                return 0

        score = calculate_score(board)
        placed_discs = score.white + score.black
        weights = {
            'disc_difference': placed_discs / 64 if placed_discs < 50 else 1,
            'mobility': 1 - placed_discs / 64 if placed_discs < 50 else 0,
            # Penalize certain positions
            'position': board_weights[position[0]][position[1]],
        }
        #return weights['position']
        return weights['position'] * (
            weights['disc_difference'] * self.disc_difference(board) +
            weights['mobility'] * self.mobility(board)
        )

    def minimax_search(self, board):
        def minimax(depth, board, pos, a, b, current_player):
            if time.time() - start_time > 4.6:
                value = self.evaluate(board, pos)
                return value, None

            if str(board) in self.searched_boards[current_player]:
                self.board_lookups += 1
                return self.searched_boards[current_player][str(board)]

            symmetries = get_symmetries(board)
            for symmetry, altered_board in symmetries.items():
                if str(altered_board) in self.searched_boards[current_player]:
                    self.board_lookups += 1
                    value, altered_position = self.searched_boards[current_player][str(altered_board)]
                    return value, reverse_symmetry(altered_position)

            if has_game_ended(board) or depth == 0:
                value = self.evaluate(board, pos)
                return value, None
            
            if current_player == self.color:
                best_value = float('-inf')
                best_position = None
                
                moves = playable_moves(board, current_player)
                random.shuffle(moves)
                for position in moves:
                    new_board = move(board, current_player, position)
                    value, _ = minimax(depth - 1, new_board, position, a, b, self.opponent)
                    if value > best_value:
                        if depth == max_depth:
                            if len(moves) == 1 or not board_weights[position[0]][position[1]] == 0:
                                best_value = value
                                best_position = position
                    a = max(best_value, a)
                    self.searched_boards[current_player][str(board)] = (best_value, best_position)
                    if a >= b:
                        break
                
                if depth == max_depth:
                    score = calculate_score(board)
                    placed_discs = score.white + score.black
                    if placed_discs < 59:
                        for corner in corners:
                            if corner in moves:
                                best_position = corner

                return best_value, best_position

            else:
                best_value = float('inf')
                best_position = None

                moves = playable_moves(board, current_player)
                random.shuffle(moves)
                for position in moves:
                    new_board = move(board, current_player, position)
                    value, _ = minimax(depth - 1, new_board, position, a, b, self.color)
                    if value < best_value:
                        best_value = value
                        best_position = position
                    b = min(best_value, b)
                    self.searched_boards[current_player][str(board)] = (best_value, best_position)
                    if a >= b:
                        break
                return best_value, best_position 
        max_depth = 4

        start_time = time.time()
        best_value, best_position = minimax(max_depth, board, None, float('-inf'), float('inf'), self.color)
        if not best_position or not is_valid_move(board, self.color, best_position):
            if best_position and not is_valid_move(board, self.color, best_position):
                print('Not valid move played')
                print(best_position)
            else:
                print('could not find position')
            best_value = float('-inf')
            for position in playable_moves(board, self.color):
                value = self.evaluate(move(board, self.color, position), position)
                if value > best_value:
                    best_value = value
                    best_position = position
        
        return best_position

        