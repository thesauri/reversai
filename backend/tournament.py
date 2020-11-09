from bot_loader import get_bot
import itertools
import json
import random

def generate_tournament(configuration_file):
    configuration = json.load(open(configuration_file, "r"))
    __verify_configuration(configuration)

    matches = {
        'teams': configuration['teams'],
        'groups': configuration['groups']
    }
    for group_index, group in enumerate(configuration['groups']):
        match_order = __randomized_match_order(group)
        matches[group_index] = match_order

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