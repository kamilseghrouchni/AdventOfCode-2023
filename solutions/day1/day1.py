import re
from functools import reduce
from pathlib import Path
from typing import List

import typer

from params import Day1, ReadParams


def my_add(a:int, b:int) -> int:
    """reduce function for summing all digits

    Args:
        a (int): _description_
        b (int): _description_

    Returns:
        int: _description_
    """
    return   a + b
    

def get_digit(extracted:str) -> str: 
    return Day1.NUMBERS_MAP[extracted] if extracted in Day1.NUMBERS_MAP.keys() else extracted 

def find_digit_pair(line:str) -> List[int]:
    """Find digit pairs for part 1

    Args:
        line (str): text entry

    Returns:
        List[int]: list of pairs digits
    """
    # join dictionnary of digits in letters
    digit_letters= '|'.join(map(re.escape, Day1.NUMBERS_MAP.keys()))

    # create regex for first and last digits
    reg_first_digit = digit_letters +'|\d'
    reg_last_digit = '(?=(' +digit_letters +'|\d))'

    # extract digits
    extract_first_digits = re.search(reg_first_digit, line).group()
    extract_last_digits = re.findall(reg_last_digit, line)[-1]

    # convert extracted digits if needed
    first_digit = get_digit(extract_first_digits)
    last_digit= get_digit(extract_last_digits)

    return int(first_digit+last_digit) 



def main():

    data_path = Path(ReadParams.PATH)
    puzzle_data = data_path/"day1"/ReadParams.PUZZLE

    with open(puzzle_data,"r") as calib: 

        # extract calibration document lines
        lines = calib.readlines()
        # extracted digit pair
        extracted = [find_digit_pair(line)  for line in lines]
        # sum all digits 
        result = reduce(my_add, extracted)

    print(result)


if __name__ == "__main__":
    typer.run(main)
