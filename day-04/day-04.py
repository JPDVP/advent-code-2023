import os
import sys
from typing import Iterable
import re

script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
INPUT = os.path.join(script_directory, "input.txt")

# REGEX PATTERNS
REGEX_PATTERN_CARD = re.compile(r"^Card +(\d+):(.+) \|(.+)")
REGEX_PATTERN_NUMBERS = re.compile(r" +(\d+)")


def parse_input(lines: Iterable[str]) -> list[tuple[int, list[int], list[int]]]:
    list_cards = []
    for line in lines:
        card, str_winning_numbers, str_numbers = REGEX_PATTERN_CARD.match(line).groups()
        winning_numbers = list(map(lambda s: int(s), REGEX_PATTERN_NUMBERS.findall(str_winning_numbers)))
        numbers = list(map(lambda s: int(s), REGEX_PATTERN_NUMBERS.findall(str_numbers)))
        list_cards.append((int(card), winning_numbers, numbers))
    return list_cards


def part1(cards: list[tuple[int, list[int], list[int]]]) -> int:
    sum_cards = 0
    for _, winning_numbers, numbers in cards:
        winning_set = set(winning_numbers)
        numbers_set = set(numbers)
        matches = winning_set.intersection(numbers_set)
        if matches:
            sum_cards += 2 ** (len(matches) - 1)
    return sum_cards


def part2(cards: list[tuple[int, list[int], list[int]]]) -> int:
    card_win_list = [1] * len(cards)

    for n, (_, winning_numbers, numbers) in reversed(list(enumerate(cards))):
        winning_set = set(winning_numbers)
        numbers_set = set(numbers)
        matches = winning_set.intersection(numbers_set)
        if matches:
            card_win_list[n] += sum(card_win_list[n + m + 1] for m in range(len(matches)))
    return sum(card_win_list)


def common() -> list[tuple[int, list[int], list[int]]]:
    cards = parse_input(open(INPUT, mode="rt").readlines())
    return cards


if __name__ == "__main__":
    input_data = common()
    print(f"Part 1: {part1(input_data)}")
    print(f"Part 2: {part2(input_data)}")
