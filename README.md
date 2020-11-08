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
6. In a new terminal session, navigate to the `frontend` directory
7. Run `yarn`

## Running
1. In the `backend` directory, run `python main.py --black human --white human`
    - This initializes a human vs. human session
    - To use a bot, change *human* to the file name of the bot (without the `.py` extension)
        - E.g. `--black oth3ll0grindr2000` to run the sample bot
2. In a separate terminal session, navigate to the `frontend` directory and run `yarn start`
3. The game should now be playable in the browser at http://localhost:3000.

## Creating your own bot
Bots are located in the `backend/reversi/bots/` directory.

1. Copy the sample bot `oth3ll0grindr2000.py` and place the copy in the `bots` directory.
2. Name the file with the name of your bot
3. Write your bot in this file by implementing the `get_move` method.

## Bot submission
1. On your computer, commit the bot and push it to your forked repository
2. In the [reversai](https://github.com/thesauri/reversai) repository, create a pull request from your forked repository
3. Once approved, this adds your bot to the main repository
