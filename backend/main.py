import asyncio
from reversi.reversi import test_game
import json
import websockets

WEBSOCKET_PORT = 6666

async def game_request_handler(websocket, path):
    board = json.dumps(test_game())
    await websocket.send(board)

game_server = websockets.serve(
    game_request_handler,
    "localhost",
    WEBSOCKET_PORT
)

print(f"Running reversi server on port {WEBSOCKET_PORT}")
asyncio.get_event_loop().run_until_complete(game_server)
asyncio.get_event_loop().run_forever()
