import asyncio
from bot_loader import get_bot
import datetime
import itertools
import json
import os.path
import random
from reversi.reversi import bot_vs_bot_session

def play_tournament(matches_file, history_file_path):
    matches = json.load(open(matches_file, "r"))
    history = History(history_file_path)

    async def play_games():
        for group_index, group in matches['group_matches'].items():
            for match_index, match in enumerate(group):
                black_team = match[0]
                black_bot_name = matches['teams'][black_team]
                white_team = match[1]
                white_bot_name = matches['teams'][white_team]

                print(f"Group {group_index} match {match_index}: black {black_team} ({black_bot_name}) vs white: {white_team} ({white_bot_name})")
                score = await __play_tournament_game(black_bot_name, white_bot_name)
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

    asyncio.get_event_loop().run_until_complete(play_games())

async def __play_tournament_game(black_bot_name, white_bot_name):
    BlackBot = get_bot(black_bot_name)
    WhiteBot = get_bot(white_bot_name)
    score = await bot_vs_bot_session(
        None,
        BlackBot("black"),
        WhiteBot("white"),
        minimum_delay=0,
        headless=True
    )
    return score

def generate_tournament(configuration_file):
    configuration = json.load(open(configuration_file, "r"))
    __verify_configuration(configuration)

    matches = {
        'teams': configuration['teams'],
        'groups': configuration['groups'],
        'group_matches': {}
    }
    for group_index, group in enumerate(configuration['groups']):
        match_order = __randomized_match_order(group)
        matches['group_matches'][group_index] = match_order

    print(json.dumps(matches))

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
