import asyncio
from reversi.bots.oth3ll0grindr2000 import Oth3lloGrindr2000
from reversi.reversi import human_vs_bot_session
import json
import websockets

WEBSOCKET_PORT = 8008

async def game_request_handler(websocket, path):
    print(f"Initializing game session")
    await human_vs_bot_session(websocket, True, Oth3lloGrindr2000("black"))

game_server = websockets.serve(
    game_request_handler,
    "localhost",
    WEBSOCKET_PORT
)

print(f"Running reversi server on port {WEBSOCKET_PORT}")
asyncio.get_event_loop().run_until_complete(game_server)
asyncio.get_event_loop().run_forever()
