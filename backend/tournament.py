import asyncio
from bot_loader import get_bot
import datetime
import itertools
import json
import os.path
import random
from reversi.reversi import bot_vs_bot_session
import websockets

WEBSOCKET_PORT = 8008

def play_tournament(matches_file, history_file_path):
    matches = json.load(open(matches_file, "r"))
    history = History(history_file_path)
    black_team = None
    white_team = None
    connected_websockets = set()

    async def websocket_request_handler(websocket, path):
        connected_websockets.add(websocket)
        print("Websocket connection!")
        try:
            await __send_tournament_state(websocket, history.history, matches["groups"], black_team, white_team)
            async for message in websocket:
                print(message)
        finally:
            connected.remove(websocket)
            print("Websocket disconnected")

    async def play_games():
        for match_index, match in enumerate(matches['matches']):
            group_index = match["group"]
            black_team = match["players"][0]
            black_bot_name = matches['teams'][black_team]
            white_team = match["players"][1]
            white_bot_name = matches['teams'][white_team]

            for websocket in connected_websockets:
                print("Broadcasting tournament state")
                await __send_tournament_state(websocket, history.history, matches["groups"], black_team, white_team)

            print(f"Group {group_index} match {match_index}: black {black_team} ({black_bot_name}) vs white: {white_team} ({white_bot_name})")
            score = await __play_tournament_game(list(connected_websockets), black_bot_name, white_bot_name)
            game = {
                "black": {
                    "name": black_team,
                    "score": score.black
                },
                "white": {
                    "name": white_team,
                    "score": score.white
                }
            }
            history.add_game(game)
            for websocket in connected_websockets:
                print("Broadcasting tournament state")
                await __send_tournament_state(websocket, history.history, matches["groups"], black_team, white_team)

    address = os.getenv('REACT_APP_IP') if os.getenv('REACT_APP_IP') else 'localhost'
    game_server = websockets.serve(
        websocket_request_handler,
        address,
        WEBSOCKET_PORT
    )
    asyncio.get_event_loop().run_until_complete(game_server)
    asyncio.get_event_loop().run_until_complete(play_games())

async def __play_tournament_game(websockets, black_bot_name, white_bot_name):
    BlackBot = get_bot(black_bot_name)
    WhiteBot = get_bot(white_bot_name)
    score = await bot_vs_bot_session(
        websockets,
        BlackBot("black"),
        WhiteBot("white"),
        minimum_delay=0.5
    )
    return score

def generate_tournament(configuration_file):
    configuration = json.load(open(configuration_file, "r"))
    __verify_configuration(configuration)

    group_matches = {}

    for group_index, group in enumerate(configuration['groups']):
        match_order = __randomized_match_order(group)
        group_matches[group_index] = match_order

    matches = []
    for i in range(0, len(group_matches[0])):
        for group_index in group_matches.keys():
            match = {
                "group": group_index,
                "players": group_matches[group_index][i]
            }
            matches.append(match)

    match_configuration = {
        'teams': configuration['teams'],
        'groups': configuration['groups'],
        'matches': matches
    }

    print(json.dumps(match_configuration))

async def __send_tournament_state(websocket, match_history, groups, black_team, white_team):
    tournament_state = {
        "matchHistory": match_history,
        "groups": groups,
        "blackTeam": black_team,
        "whiteTeam": white_team
    }
    try:
        await websocket.send(json.dumps(tournament_state))
    except websockets.exceptions.ConnectionClosedError:
        pass


def __verify_configuration(configuration):
    def verify_bot_existance(configuration):
        for team_name, bot_name in configuration['teams'].items():
            try:
                get_bot(bot_name)
            except:
                raise ValueError(f"Team {team_name} has an invalid bot: {bot_name}")

    def verify_groups(configuration):
        for group in configuration['groups']:
            for team in group:
                if team not in configuration['teams']:
                    raise ValueError(f"Invalid team {team} in group {group}: does not exist")

    verify_bot_existance(configuration)
    verify_groups(configuration)

def __randomized_match_order(group):
    all_pairs = itertools.combinations(group, 2)
    randomized_start_order = list(map(
        lambda x: (x[0], x[1]) if random.randint(0, 2) == 0 else (x[1], x[0]),
        all_pairs
    ))
    random.shuffle(randomized_start_order)
    return randomized_start_order

class History(object):
    def __init__(self, history_file_path):
        if os.path.exists(history_file_path):
            file = open(history_file_path, "r")
            self.history = json.load(file)
            file.close()
        else:
            self.history = []
        self.history_file_path = history_file_path

    def add_game(self, game):
        game["timestamp"] = datetime.datetime.now().isoformat()
        self.history.append(game)
        file = open(self.history_file_path, "w")
        file.write(json.dumps(self.history))
        file.close()
