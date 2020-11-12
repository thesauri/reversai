import asyncio
from bot_loader import get_bot
import importlib
import json
import reversi.bots
from reversi.reversi import human_vs_bot_session, human_vs_human_session, bot_vs_bot_session
import websockets
import config
import os

WEBSOCKET_PORT = 8008

def run_server(black, white):
    async def game_request_handler(websocket, path):
        if black == "human" and white == "human":
            print(f"Initializing human vs human session")
            await human_vs_human_session(websocket)
        elif black != "human" and white != "human":
            print("Initializing bot vs bot session")
            BlackBot = get_bot(black)
            WhiteBot = get_bot(white)
            await bot_vs_bot_session(
                websocket,
                BlackBot("black"),
                WhiteBot("white"),
                minimum_delay=0.1
            )
        else:
            print(f"Initializing human vs bot session")
            is_bot_black = black != "human"
            bot_name = black if is_bot_black else white
            Bot = get_bot(bot_name)
            await human_vs_bot_session(
                websocket,
                is_bot_black,
                Bot("black" if is_bot_black else "white"),
                minimum_delay=0.1
            )
    address = os.getenv('REACT_APP_IP') if os.getenv('REACT_APP_IP') else 'localhost'
    game_server = websockets.serve(
        game_request_handler,
        address,
        WEBSOCKET_PORT
    )

    print(f"Running reversi server on {address}:{WEBSOCKET_PORT}")
    asyncio.get_event_loop().run_until_complete(game_server)
    asyncio.get_event_loop().run_forever()