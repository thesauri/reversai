from arguments import get_arguments
from headless import run_headless_game
from server import run_server

args = get_arguments()

if args.headless:
    if args.white == "human" or args.black == "human":
        print("ERROR: Only bots can play in headless mode")
        exit(1)
    run_headless_game(args.black, args.white)
else:
    run_server(args.black, args.white)
