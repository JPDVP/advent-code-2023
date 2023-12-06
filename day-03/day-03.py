import os
import sys
from typing import Iterable
from functools import reduce


script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
INPUT = os.path.join(script_directory, "input.txt")


def parse_char(char: str) -> int:
    """
    :param char:
    :return:
        0 for non-symbols / numbers
        1 for symbols (other than *)
        2 for gears (*)
        3 for numbers
    """
    if char.isdigit():
        return 3
    elif char == "*":
        return 2
    elif char == ".":
        return 0
    else:
        return 1


# read matrix
def parse_matrix(lines: Iterable[str]) -> tuple[
    list[list[int]],
    list[tuple[int, tuple[int, int, int]]],
    list[tuple[int, int]]
]:
    symbols = []
    numbers: list[tuple[int, tuple[int, int, int]]] = []
    gears: list[tuple[int, int]] = []
    for row, line in enumerate(lines):
        symbol_line = []
        str_number = ""
        for column, char in enumerate(line.rstrip("\n")):
            parsed_char = parse_char(char)
            symbol_line.append(parsed_char)
            if parsed_char == 3:
                if not str_number:
                    start = column
                str_number += char
            elif str_number:
                end = column - 1
                numbers.append((int(str_number), (row, start, end)))
                str_number = ""
            if parsed_char == 2:
                gears.append((row, column))
        if str_number:
            end = column - 1
            numbers.append((int(str_number), (row, start, end)))
        symbols.append(symbol_line)
    return symbols, numbers, gears


def check_adjacent_symbol(matrix: list[list[int]], row: int, start: int, end: int) -> bool:
    left_column = max(0, start-1)
    right_column = min(end+1, len(matrix[0])-1)

    # check top row
    if row > 0:
        for col in range(left_column, right_column+1):
            if matrix[row-1][col] in (1, 2):
                return True
    # check bottom row
    if row < len(matrix)-1:
        for col in range(left_column, right_column+1):
            if matrix[row+1][col] in (1, 2):
                return True
    # check left
    if matrix[row][left_column] in (1, 2):
        return True
    # check right
    if matrix[row][right_column] in (1, 2):
        return True
    # if no early return, return False
    return False


def check_adjacent_numbers(position: tuple[int, int], number_position: tuple[int, int, int]) -> bool:
    row, column = position
    n_row, n_start, n_end = number_position

    return abs(row - n_row) <= 1 and column in range(n_start - 1, n_end + 2)


def part1(matrix: list[list[int]], numbers: list[tuple[int, tuple[int, int, int]]]) -> int:
    sum_numbers = 0
    for number, (row, start, end) in numbers:
        if check_adjacent_symbol(matrix, row, start, end):
            sum_numbers += number
    return sum_numbers


def part2(numbers: list[tuple[int, tuple[int, int, int]]], gears: list[tuple[int, int]]) -> int:
    sum_gear = 0
    for gear_position in gears:
        numbers_to_multiply = [
            number
            for number, number_position
            in numbers
            if check_adjacent_numbers(gear_position, number_position)
        ]
        if len(numbers_to_multiply) > 1:
            sum_gear += reduce(lambda x, y: x * y, numbers_to_multiply)
    return sum_gear


def common():
    matrix, numbers, gears = parse_matrix(open(INPUT, mode="rt").readlines())
    return matrix, numbers, gears


if __name__ == "__main__":
    input_matrix, input_numbers, input_gears = common()
    print(f"Part 1: {part1(input_matrix, input_numbers)}")
    print(f"Part 2: {part2(input_numbers, input_gears)}")
