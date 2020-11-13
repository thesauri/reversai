def print_board(board):
    # Print the board
    for row_index, row in enumerate(board):
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
    for column_index, _ in enumerate(board):
        print(f"{column_index} ", end="")
    print("")
