class Game:
    def __init__(self):
        self.board = list(map(lambda x: 8 * [""], 8 * [""]))
        self.board[3][3] = "white"
        self.board[4][3] = "black"
        self.board[3][4] = "black"
        self.board[4][4] = "white"

    def print_board(self):
        # Print the board
        for row_index, row in enumerate(self.board):
            print(f"{row_index} |", end="")
            for cell_content in row:
                print_styles = {
                    "black": "b ",
                    "white": "w ",
                    "": "- "
                }
                cell = print_styles[cell_content]
                print(cell, end="")
            print("|")
        # Print the bottom column indices (0 to 7)
        print("   ", end="")
        for column_index, _ in enumerate(self.board):
            print(f"{column_index} ", end="")
        print("")
