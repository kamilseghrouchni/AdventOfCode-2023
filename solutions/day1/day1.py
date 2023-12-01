from params import ReadParams, Day1Params
import typer
from pathlib import Path 
import re
from typing import List
from functools import reduce

def my_add(a:int, b:int) -> int:
    """reduce function for summing all digits

    Args:
        a (int): _description_
        b (int): _description_

    Returns:
        int: _description_
    """
    result = a + b
    # print(f"{a} + {b} = {result}")
    return  result

def get_digit(extracted:str) -> str: 
    return Day1Params.number_words[extracted] if extracted in Day1Params.number_words.keys() else extracted 

def find_digit_pair(line:str) -> List[int]:
    """Find digit pairs for part 1

    Args:
        line (str): text entry

    Returns:
        List[int]: list of pairs digits
    """
    # join dictionnary of digits in letters
    digit_letters= '|'.join(map(re.escape, Day1Params.number_words.keys()))

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

    data_path = Path(ReadParams.path)
    puzzle_data = data_path/"day1"/"puzzle.txt"

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
