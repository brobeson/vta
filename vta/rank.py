"""Figure out the best sequences."""

import os.path
from pprint import pprint


class Sequence:
    """Represent scores for a particular sequence."""

    def __init__(self, line):
        words = line.split()
        self.name = words[0]
        self.mdnet = float(words[1])
        self.famt = float(words[2])
        self.ava = float(words[3])
        self.vital = float(words[4])
        self.eco = float(words[5])

    def __lt__(self, other):
        return self.famt < other.famt

    def __str__(self):
        return self.name


def main():
    """The main script entry point"""
    with open(os.path.expanduser("~/Downloads/compText_OTB100_18.txt")) as f:
        lines = f.readlines()
    del lines[0]
    sequences = [Sequence(line) for line in lines]
    sequences = filter(_sequence_filter, sequences)
    for s in sequences:
        print(s)


def _sequence_filter(sequence):
    return (
        sequence.famt > sequence.mdnet
        and sequence.famt > sequence.ava
        and sequence.famt > sequence.vital
        and sequence.famt > sequence.eco
    )


if __name__ == "__main__":
    main()
