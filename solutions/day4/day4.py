import re
from pathlib import Path
from typing import List

import typer

from params import ReadParams


def parse_card(card: str) -> set[int]:
    """parse cards to get winning and played numbers

    Args:
        card (str): list of numbers

    Returns:
        set[int]: matched numbers
    """
    _, cards = card.split(":")
    winning, played = cards.split("|")
    winnig_set = set(re.findall(r"(\b\d+\b)", winning))
    played_set = set(re.findall(r"(\b\d+\b)", played))

    return winnig_set.intersection(played_set)


def compute_points(winning_combinations: set[int]) -> float:
    return 2 ** (len(winning_combinations) - 1) if len(winning_combinations) > 0 else 0


def compute_copies(intersections: list(set[int])) -> List[int]:
    """compute copies for each card
    This can clearly be improved with functional programing using recursive calls

    Args:
        intersections (list): cards matches

    Returns:
        List[int]: copies per cards
    """
    copies = [1] * len(intersections)
    for i, matches in enumerate(intersections):
        for _ in range(copies[i]):
            total_matches = len(matches)
            for j in range(total_matches):
                copies[i + j + 1] += 1
    return copies


def main():
    # read data
    data_path = Path(ReadParams.PATH)
    puzzle_data = data_path / "day4" / ReadParams.PUZZLE

    with open(puzzle_data, "r") as scratchcards:
        # extract calibration document lines
        cards = scratchcards.readlines()
        # parse scratchcards
        parsed_cards = list(map(parse_card, cards))
        # get points worth
        points_total = list(map(compute_points, parsed_cards))
        # get copies
        copies_total = compute_copies(parsed_cards)
        print(sum(points_total))
        print(sum(copies_total))


if __name__ == "__main__":
    typer.run(main)
