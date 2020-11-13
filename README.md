# ReversAI
Environment to develop bots for [Reversi](https://en.wikipedia.org/wiki/Reversi).

## Structure
Bots are implemented in Python.

The environment is split into two parts: (1) a backend containing the bots and game logic and (2) a browser frontend for interacting with a Reversi game session.

## Requirements
- [Git](https://git-scm.com)
- Python 3.8.5 and [virtualenv](https://virtualenv.pypa.io/en/latest/)
- [Node 14.15.0](https://nodejs.org/en/) and [yarn](https://yarnpkg.com/getting-started/install)

## Setup
1. Fork this repository (using the *Fork* button in the upper right corner)
2. Clone the repository to your computer
    1. Click the *Code* button
    2. Copy the URL to your clipboard
    3. Run `git clone <pasted url>`
3. In a terminal, navigate to the `backend` directory
4. Run `virtualenv venv`
5. Run `source venv/bin/activate`
6. Run `pip install -r requirements.txt`
7. If you want to add some other packages, contact the organizers
8. In a new terminal session, navigate to the `frontend` directory
9. Run `yarn`

## Running
1. In the `backend` directory, run `python main.py --black human --white human`
    - This initializes a human vs. human session
    - To use a bot, change *human* to the file name of the bot (without the `.py` extension)
        - E.g. `--black oth3ll0grindr2000` to run the sample bot
2. In a separate terminal session, navigate to the `frontend` directory and run `yarn start`
3. The game should now be playable in the browser at http://localhost:3000.

Games can also be run headless without the browser by adding the `--headless` flag to the Python command. This is useful for testing a bot quickly, e.g. against the sample random bot. It is only available for bot vs bot matches.

## Creating your own bot
Bots are located as `<bot_name>/bot.py` entries of the `backend/reversi/bots/` directory.

1. Copy the sample bot folder `oth3ll0grindr2000` and place the copy in the `bots` directory.
2. Rename the directory to the name of your bot
3. Write your bot in the `<bot_name>/bot.py` file by implementing the `get_move` method.

Note: **Maximum of 5 seconds of execution time per move allowed**. This is a soft limit, i.e. the bot won't be killed after this time, but execution time is measured and the bot will be disqualified if it takes significantly more time than this. Execution time can be seen both in both the frontend and the Python backend as `Time taken: 0.0 s` log statements.

## Bot helper functions
Helper functions for game logic have been implemented and we encourage you to use these in in your bot. For instance, you may want to call `is_valid_move` to ensure that a move is valid before returning it or `move` to see what the resulting board state is if you call a certain move. All the function calls are non-mutating, in other words you can safely call `move` without it affecting the actual game state.

The functions are implemented in `reversi.logic`, but have been imported to the sample bot (i.e., you can use them directly without any imports).

The following functions are available:

### is_valid_move
```def is_valid_move(board, turn, position):
    """
    Test whether a game move is valid

    board: The game board as a row-column array of "black", "white", or ""

    turn: "black" or "white"

    position: Position as (row_index, column_index)

    Returns: True or False
    """
```

### move
```def move(board, turn, position):
    """
    Issue a game move

    board: The game board as a row-column array of "black", "white", or ""

    turn: "black" or "white"

    position: Position as (row_index, column_index)

    Returns: A copy of the new game board. None if the move was invalid.""
```

### playable_moves
```def playable_moves(board, turn):
    """
    Get a list of playable moves for a given board and turn

    board: The game board

    turn: The player whose turn it is (black or white)

    Returns: A list of playable moves, e.g. [(5,3), (2,2), (0,1)]
    """
```

### has_game_ended
```def has_game_ended(board):
    """
    Checks whether the game has ended. A game has ended if neither black nor white can play.

    board: The game board

    Returns: True or False
    """
```

### calculate_score
```def calculate_score(board):
    """
    Calculate the score for a given board

    board: The board

    Returns: The scores as a named tuple, e.g. Score(black: 5, white: 10). Access the scores with score = calculate_score(board), then score.black and score.white.
    """
```

## Bot submission
1. On your computer, commit the bot and push it to your forked repository
2. In the [reversai](https://github.com/thesauri/reversai) repository, create a pull request from your forked repository
3. Once approved, this adds your bot to the main repository
