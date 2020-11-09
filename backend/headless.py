import asyncio
from bot_loader import get_bot
from reversi.reversi import bot_vs_bot_session

def run_headless_game(black, white):
    async def game_session():
        print("Initializing headless bot vs bot session")
        BlackBot = get_bot(black)
        WhiteBot = get_bot(white)
        await bot_vs_bot_session(
            None,
            BlackBot("black"),
            WhiteBot("white"),
            minimum_delay=0,
            headless=True
        )

    asyncio.get_event_loop().run_until_complete(game_session())
