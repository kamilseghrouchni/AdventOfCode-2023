import re
from pathlib import Path
from typing import Dict, List, Tuple
from itertools import chain
import typer
import numpy as np
from params import ReadParams, Day3

def get_numbers (schematics :List[str]) -> Dict[str,int]:
    """Retreive all number from engine schematic with postion

    Args:
        schematics (List[str]): engine schematic

    Returns:
        Dict[str,int]: starts,stops and numbers from engine schematic
    """
    schematics_numbers = {"starts":[],"stops": [], "numbers": []}
    # iterate over engine schematics
    for line,scheme in enumerate(schematics): 
        # extract all numbers
        numbers = re.finditer(r"(\b\d+\b)",scheme)
        for match in numbers:
            schematics_numbers["starts"].append((line,match.span()[0]))
            schematics_numbers["stops"].append((line,match.span()[1]-1))
            schematics_numbers["numbers"].append(int(match.group()))
    return schematics_numbers

def get_symboles (schematics: List[str], part: int) -> List[Tuple[int,int]]:
    """Retreive all symboles from engine schematic with postion for corresponding part

    Args:
        schematics (List[str]): engine schematics
        part (int): problem part

    Returns:
        List[Tuple[int,int]]: _description_
    """
    schematics_symbols_pos=[]
    for line,scheme in enumerate(schematics):
        # extract symbols
        regex = Day3.REG_PART_1 if part == 1 else Day3.REG_PART_2
        symbols = re.finditer(regex,scheme) 
        schematics_symbols_pos += [(line,match.span()[0])for match in symbols]

    return schematics_symbols_pos

def possible_positions(position: Tuple[int,int]) -> List[int]: 
    """Compute all possible match position for a symbol

    Args:
        position (Tuple[int,int]): (y,x) axis of symbole

    Returns:
        List[int]: All neighboring positions
    """
    y_axis,x_axis = position
    possibilities= []
    neighbors = [-1,0,1]
    for i in neighbors:
        for j in neighbors:
            possibilities.append((y_axis+i,x_axis+j))
    return possibilities

def part_sum_engine_part_1(numbers: Dict[str,int],symbols: List[Tuple[int,int]]) -> int:
    """ Compute some of number matches

    Args:
        numbers (Dict[str,int]): numbers with positions
        symbols (List[Tuple[int,int]]): symboles positions

    Returns:
        int: sum of matches
    """
    positions = list(chain(*map(possible_positions,symbols)))
    starts_pos =  [numbers["starts"].index(pos) for pos in positions if pos in numbers["starts"] ]
    stops_pos =  [numbers["stops"].index(pos) for pos in positions if pos in numbers["stops"] ]
    matched_numbers = set(starts_pos+stops_pos)

    return sum ([numbers["numbers"][match] for match in matched_numbers])

def part_sum_engine_part_2(numbers: Dict[str,int],symbols: List[Tuple[int,int]]) -> int:
    """Compute matching gears

    Args:
        numbers (Dict[str,int]): numbers with positions
        symbols (List[Tuple[int,int]]): symboles positions

    Returns:
        int: _description_
    """
    symboles_positions = list(map(possible_positions,symbols))
    exact_matches = []
    for symboles in symboles_positions: 
        starts_pos =  [numbers["starts"].index(pos) for pos in symboles if pos in numbers["starts"] ]
        stops_pos =  [numbers["stops"].index(pos) for pos in symboles if pos in numbers["stops"] ]
        matched_numbers = set(starts_pos+stops_pos)
        if len(matched_numbers) == 2 :
            exact_matches.append(np.prod([numbers["numbers"][match] for match in matched_numbers]))

    return sum (exact_matches)


def main():
    # read data
    data_path = Path(ReadParams.PATH)
    puzzle_data = data_path / "day3" /ReadParams.PUZZLE

    with open(puzzle_data, "r") as schematics_engine:
        # extract calibration document lines
        schematics = schematics_engine.readlines()
        # get schematics number
        numbers = get_numbers(schematics)

        symbols_part_1=get_symboles(schematics,1)
        symbols_part_2=get_symboles(schematics,2)

        print(part_sum_engine_part_1 (numbers,symbols_part_1))
        print(part_sum_engine_part_2 (numbers,symbols_part_2))




if __name__ == "__main__":
    typer.run(main)
