import argparse
import asyncio
from reversi.bots.oth3ll0grindr2000 import Oth3lloGrindr2000
from reversi.reversi import human_vs_bot_session, human_vs_human_session, bot_vs_bot_session
import json
import websockets

WEBSOCKET_PORT = 8008

parser = argparse.ArgumentParser(description="Run a game of reversi")
parser.add_argument(
    "--black",
    "-b",
    type=str,
    choices=["bot", "human"],
    help="Bot or human as black",
    default="human"
)
parser.add_argument(
    "--white",
    "-w",
    type=str,
    choices=["bot", "human"],
    help="Bot or human as white",
    default="human"
)
args = parser.parse_args()

async def game_request_handler(websocket, path, black, white):
    if black == "human" and white == "human":
        print(f"Initializing human vs human session")
        await human_vs_human_session(websocket)
    if black == "bot" and white =="bot":
        print("Initializing bot vs bot session")
        await bot_vs_bot_session(
            websocket,
            Oth3lloGrindr2000("black"),
            Oth3lloGrindr2000("white")
        )
    else:
        print(f"Initializing human vs bot session")
        is_bot_black = black == "bot"
        await human_vs_bot_session(
            websocket,
            is_bot_black,
            Oth3lloGrindr2000("black" if is_bot_black else "white")
        )

game_server = websockets.serve(
    lambda websocket, path: game_request_handler(
        websocket,
        path,
        args.black,
        args.white
    ),
    "localhost",
    WEBSOCKET_PORT
)

print(f"Running reversi server on port {WEBSOCKET_PORT}")
asyncio.get_event_loop().run_until_complete(game_server)
asyncio.get_event_loop().run_forever()
