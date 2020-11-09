import argparse

def get_arguments():
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
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--generate_tournament", type=str)
    args = parser.parse_args()
    return args