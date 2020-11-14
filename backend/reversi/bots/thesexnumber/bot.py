import random
import math
import numpy as np
import time as timppat
from ...logic import is_valid_move, move, playable_moves, has_game_ended, calculate_score

# Do NOT rename this class


board_weights = np.array([
  [100, -20, 10, 5, 5, 10, -20, 100],
  [-20, -50, -2, -2, -2, -2, -50, -20],
  [10, -2, -1, -1, -1, -1, -2, 10],
  [5, -2, -1, -1, -1, -1, -2, 10],
  [5, -2, -1, -1, -1, -1, -2, 5],
  [10, -2, -1, -1, -1, -1, -2, 5],
  [-20, -50, -2, -2, -2, -2, -50, -20],
  [100, -20, 10, 5, 5, 10, -20, 100]
])

corners = np.array([
  (0,0),
  (0,7),
  (7,0),
  (7,7)
])


MAXTIME = 4.5

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
        self.name = "TheSexNumber"
        self.author = "H3mp and Beppu"
        self.color = color
        self.enemy_color = ""
        if color == "white":
          self.enemy_color = "black"
        else:
          self.enemy_color = "white"

    def count_discs(self, board, color=""):
      nblack = 0
      nwhite = 0
      for i in board:
        if i == "white":
          nwhite += 1
        elif i == "black":
          nblack +=1

      if color == "white":
        return nwhite
      elif color == "black":
        return nblack
      
      return nwhite + nblack

    def color_value(self, input):
      if input == self.color:
        return 1
      elif input == self.enemy_color:
        return -1
      return 0


    def utility_value(self, board):
      player_util = 0
      enemy_util = 0
      for i in range(0,7):
        for j in range(0,7):
          curr = board[i][j]
          if curr == self.color:
            player_util += board_weights[i][j] 
          elif curr == self.enemy_color:
            enemy_util += board_weights[i][j]
      return 100 * ((player_util - enemy_util) / (player_util + enemy_util))

    def corner_weights(self, board):
      player_corners = 0
      enemy_corners = 0
      for c in corners:
        corner = board[c[0]][c[1]]
        if corner == self.color:
          player_corners += 1
        elif corner == self.enemy_color:
          enemy_corners += 1

      value = 0
      if((player_corners + enemy_corners) != 0):
        value = 100 * (player_corners - enemy_corners) \
                / (player_corners + enemy_corners)
      return value

    def positional_weight(self, board):
      sum = 0
      for i in range(0,7):
        for j in range(0,7):
          sum += board_weights[i][j] * self.color_value(board[i][j])
      return sum

    def mobility_weight(self, board):
      player_moves = len(playable_moves(board, self.color))
      enemy_moves = len(playable_moves(board, self.enemy_color))
      value = 0
      if((player_moves + enemy_moves) != 0):
        value = 100 * (player_moves - enemy_moves) \
                / (player_moves + enemy_moves)
      return value

    def absolute(self, board):
      return self.count_discs(board,self.color) - self.count_discs(board, self.enemy_color)

    def calculate_board_weight(self, board, turn):
      u = random.uniform(0,1)
      cw = self.corner_weights(board)
      mw = self.mobility_weight(board)
      if u < 0.5:
        return cw + 0.5 * mw
      else:
        return mw + 0.5 * cw

    def minimax(self, board, depth, color, turn):
      children = playable_moves(board, color)
      if depth == 0 or len(children) == 0:
        return self.calculate_board_weight(board, turn), None
        
      best_move = children[0]
      # Maximizing player
      if color == self.color:
        value = -math.inf
        for child in children:
          new_board = move(board, color, child)
          ret = self.minimax(new_board, depth-1, self.enemy_color, turn+1)
          temp = ret[0]
          if temp > value:
            value = temp
            best_move = child
      else: # Minimizing player
        value = math.inf
        for child in children:
          new_board = move(board, color, child)
          ret = self.minimax(new_board, depth-1, self.color, turn+1)
          
          temp = ret[0]
          if temp < value:
            value = temp
            best_move = child

      return value, best_move


    def alphabeta(self, board, depth, alpha, beta, color, turn, starttime):
      children = playable_moves(board, color)
      curr_time = timppat.time()
      if depth == 0 or len(children) == 0 or (curr_time - starttime) > MAXTIME:
        return self.calculate_board_weight(board, turn), None
        
      best_move = children[0]
      # Maximizing player
      if color == self.color:
        value = -math.inf
        for child in children:
          new_board = move(board, color, child)
          ret = self.alphabeta(new_board, depth-1, alpha, beta, self.enemy_color, turn+1, starttime)
          
          temp = ret[0]
          if temp > value:
            value = temp
            best_move = child

          alpha = max(alpha, temp)
          if alpha >= beta:
            break

      else: # Minimizing player
        value = math.inf
        for child in children:
          new_board = move(board, color, child)
          ret = self.alphabeta(new_board, depth-1, alpha, beta, self.color, turn+1, starttime)
          
          temp = ret[0]
          if temp < value:
            value = temp
            best_move = child

          beta = min(beta, temp)
          if beta <= alpha:
            break

      return value, best_move

    def get_move(self, board):
        """
        Called by the game to get a move based on the given game board

        Tip: The game expects the move to be valid. To check move validity, use is_valid_move(board, self.color, (row_index, column_index)).

        board: The game board as a row-column array of "black", "white", or "", i.e. the cell board[3][4] refers to row three and column 4. The rows and columns are indexed from 0 (valid values 0-7).

        Returns: The position to place the disc on as a tuple (row_index, column_index), i.e. (7, 2) for row 7 and column 2. Note that the position *has* to be valid (otherwise the game server will throw an error). Use the is_valid_move from reversi/logic to test whether a move is valid or not.
        """
        
        
        starttime = timppat.time()
        current_turn = self.count_discs(board) - 4  + 1
        max_depth = 4 

        # REMOVE THIS AND ADD YOUR OWN CODE HERE
        ret = self.alphabeta(board, max_depth, -math.inf, math.inf, self.color, current_turn, starttime)
        #ret = self.minimax(board, max_depth, self.color, current_turn)
        best_move = ret[1]
        
    

        return best_move

    # ADD ADDITIONAL CLASS METHODS AS NEEDED