from arguments import get_arguments
from headless import run_headless_game
from server import run_server
from tournament import generate_tournament, play_tournament

args = get_arguments()

if args.headless:
    if args.white == "human" or args.black == "human":
        print("ERROR: Only bots can play in headless mode")
        exit(1)
    run_headless_game(args.black, args.white)
elif args.generate_tournament:
    generate_tournament(args.generate_tournament)
elif args.play_tournament:
    play_tournament(args.play_tournament[0], args.play_tournament[1])
else:
    run_server(args.black, args.white)
