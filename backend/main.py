import argparse
import asyncio
import importlib
import reversi.bots
from reversi.reversi import human_vs_bot_session, human_vs_human_session, bot_vs_bot_session
import json
import websockets

WEBSOCKET_PORT = 8008

parser = argparse.ArgumentParser(description="Run a game of reversi")
parser.add_argument(
    "--black",
    "-b",
    type=str,
    help="Black: human or bot_file_name (just the file name, no path bots/, no extension .py)",
    default="human"
)
parser.add_argument(
    "--white",
    "-w",
    type=str,
    help="White: human or bot_file_name.py (just the file name, no path bots/, no extension .py)",
    default="human"
)
args = parser.parse_args()

async def game_request_handler(websocket, path, black, white):
    if black == "human" and white == "human":
        print(f"Initializing human vs human session")
        await human_vs_human_session(websocket)
    if black != "human" and white != "human":
        print("Initializing bot vs bot session")
        BlackBot = getattr(
            importlib.import_module(f"reversi.bots.{black}"),
            "Bot"
        )
        WhiteBot = getattr(
            importlib.import_module(f"reversi.bots.{white}"),
            "Bot"
        )
        await bot_vs_bot_session(
            websocket,
            BlackBot("black"),
            WhiteBot("white")
        )
    else:
        print(f"Initializing human vs bot session")
        is_bot_black = black == "bot"
        bot_name = black if is_bot_black else white
        Bot = getattr(
            importlib.import_module(f"reversi.bots.{bot_name}"),
            "Bot"
        )
        await human_vs_bot_session(
            websocket,
            is_bot_black,
            Bot("black" if is_bot_black else "white")
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
