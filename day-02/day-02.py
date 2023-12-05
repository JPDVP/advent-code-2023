import os
import sys
import re

script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
INPUT = os.path.join(script_directory, "input.txt")

# REGEX PATTERNS
REGEX_PATTERN_GAME = re.compile(r"^Game (\d+):(.+)")
REGEX_PATTERN_DRAW = re.compile(r"([^;]+)")
REGEX_PATTERN_BALL = re.compile(r" (\d+) (\w+)(?:,)?")


PART1_MAX_RED = 12
PART1_MAX_GREEN = 13
PART1_MAX_BLUE = 14


def parse_input(line: str) -> tuple[int, list[tuple[int, int, int]]]:
    # returns: game id, (red, green, blue)
    game_id, game_data = REGEX_PATTERN_GAME.match(line).groups()
    list_draws = []
    for draw in REGEX_PATTERN_DRAW.findall(game_data):
        # initialize dictionary to 0
        draw_result = {"red": 0, "green": 0, "blue": 0}
        for n, color in REGEX_PATTERN_BALL.findall(draw):
            draw_result[color] = int(n)
        list_draws.append((draw_result["red"], draw_result["green"], draw_result["blue"]))
    return int(game_id), list_draws


def part1() -> int:
    with open(INPUT, mode="rt") as f:
        sum_game_id = 0
        for line in f.readlines():
            game_id, game_data = parse_input(line)
            valid_game = True
            for r, g, b in game_data:
                if r > PART1_MAX_RED or g > PART1_MAX_GREEN or b > PART1_MAX_BLUE:
                    valid_game = False
                    break
            if valid_game:
                sum_game_id += game_id
    return sum_game_id


def part2() -> int:
    with open(INPUT, mode="rt") as f:
        sum_power = 0
        for line in f.readlines():
            game_id, game_data = parse_input(line)
            max_r, max_g, max_b = 0, 0, 0
            for r, g, b in game_data:
                max_r = max(max_r, r)
                max_g = max(max_g, g)
                max_b = max(max_b, b)
            sum_power += max_r * max_g * max_b
    return sum_power


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
