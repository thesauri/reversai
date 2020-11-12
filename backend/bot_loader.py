import importlib

def get_bot(name):
    Bot = getattr(
        importlib.import_module(f"reversi.bots.{name}.bot"),
        "Bot"
    )
    return Bot