import re
from functools import reduce
from itertools import chain
from pathlib import Path
from typing import Dict, List

import typer

from params import Day2, ReadParams


def set_validity(set: str) -> bool:
    """check if set is valid

    Args:
        set (str): set in game

    Returns:
        bool: result of comparison with threshold
    """
    color = re.findall(r"\b[a-zA-Z]+\b", set)[0]
    number = int(re.findall("\d+", set)[0])
    return Day2.GAME_CONSTRAINTS[color] >= number


def game_parser(games: str) -> List[str]:
    """Parse game into list of sets

    Args:
        games (str): multiple sets

    Returns:
        List[str]: sets comma separated
    """
    # get draws
    _, draws = games.split(":")
    # split draws
    draws_list = draws.split(";")
    # get sets
    return list(chain(*[set.split(",") for set in draws_list]))


def game_validity(game: str) -> List[bool]:
    """check if validity of game across colors

    Args:
        game (str): multiple draws

    Returns:
        List[bool]: indicator for validity of each set
    """
    sets = game_parser(game)
    validity = [set_validity(set) for set in sets]
    return all(validity)


def myreduce(a, b):
    return a * b


def minimum_game_multiplicity(game: str) -> List[int]:
    """Compute minimum game combination product

    Args:
        game (str): sets list

    Returns:
        List[int]: product of minimum for all sets
    """
    # initialize color dict
    game_dict = dict(zip(Day2.GAME_CONSTRAINTS.keys(), [0] * 3))
    # parse game into sets
    sets = game_parser(game)
    for set in sets:
        for color in Day2.GAME_CONSTRAINTS.keys():
            # extract number for color
            number = int(re.findall("\d+", set)[0])
            # check minimum
            if color in set and game_dict[color] < number:
                game_dict[color] = number

    return reduce(myreduce, game_dict.values())


def main():
    # read data
    data_path = Path(ReadParams.PATH)
    puzzle_data = data_path / "day2" / ReadParams.PUZZLE

    with open(puzzle_data, "r") as cube:
        # extract calibration document lines
        games = cube.readlines()

        # get id of valid games
        sum_ids = sum([id + 1 for id, game in enumerate(games) if game_validity(game)])

        # get sum of product of minimum
        prod_values = sum([minimum_game_multiplicity(game) for game in games])

    print(sum_ids)
    print(prod_values)


if __name__ == "__main__":
    typer.run(main)
