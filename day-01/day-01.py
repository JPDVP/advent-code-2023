import os
import sys
from collections import deque

script_directory = os.path.dirname(os.path.abspath(sys.argv[0]))
INPUT = os.path.join(script_directory, "input.txt")

SPELLED_NUMBERS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}


def get_partial_matches() -> set[str]:
    # create set with empty string
    set_possibilities = {""}
    for element in SPELLED_NUMBERS.keys():
        for n in range(1, len(element)):
            set_possibilities.add(element[:n])
            set_possibilities.add(element[-n:])
    return set_possibilities


def main():
    set_partial_matches = get_partial_matches()
    sum_calibration_values = 0
    with open(INPUT, mode="rt") as f:
        for line in f.readlines():
            left, right = 0, len(line) - 1
            first, last = 0, 0
            first_word, last_word = deque(), deque()
            while left < len(line):
                if line[left].isdigit():
                    first = line[left]
                    break
                else:
                    first_word.append(line[left])
                    if "".join(first_word) in SPELLED_NUMBERS:
                        first = SPELLED_NUMBERS["".join(first_word)]
                        break
                    while "".join(first_word) not in set_partial_matches:
                        first_word.popleft()
                left += 1
            while right >= 0:
                if line[right].isdigit():
                    last = line[right]
                    break
                else:
                    last_word.appendleft(line[right])
                    if "".join(last_word) in SPELLED_NUMBERS:
                        last = SPELLED_NUMBERS["".join(last_word)]
                        break
                    while "".join(last_word) not in set_partial_matches:
                        last_word.pop()
                right -= 1
            sum_calibration_values += int(first + last)
    print(sum_calibration_values)


if __name__ == "__main__":
    main()