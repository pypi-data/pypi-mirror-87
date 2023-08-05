import os

from split_file_reader import SplitFileReader
from io import TextIOWrapper

filepath_alice = "./test/files/plaintext/Adventures_In_Wonderland.txt"
filepaths_alice = [
    "./test/files/plaintext/Adventures_In_Wonderland.txt.000",
    "./test/files/plaintext/Adventures_In_Wonderland.txt.001",
    "./test/files/plaintext/Adventures_In_Wonderland.txt.002",
    "./test/files/plaintext/Adventures_In_Wonderland.txt.003",
    "./test/files/plaintext/Adventures_In_Wonderland.txt.004",
    "./test/files/plaintext/Adventures_In_Wonderland.txt.005",
    "./test/files/plaintext/Adventures_In_Wonderland.txt.006",
    "./test/files/plaintext/Adventures_In_Wonderland.txt.007",
    "./test/files/plaintext/Adventures_In_Wonderland.txt.008",
    "./test/files/plaintext/Adventures_In_Wonderland.txt.009",
    "./test/files/plaintext/Adventures_In_Wonderland.txt.010",
    "./test/files/plaintext/Adventures_In_Wonderland.txt.011",
]

filepath_blns = "./test/files/plaintext/blns.txt"

# Lots of splits.  17 splits seems to ensure that at least a few multi-byte characters are split mid-character,
# split -d -n 17 -a3 blns.txt blns.txt.

filepaths_blns = [
    "./test/files/plaintext/blns.txt.000",
    "./test/files/plaintext/blns.txt.001",
    "./test/files/plaintext/blns.txt.002",
    "./test/files/plaintext/blns.txt.003",
    "./test/files/plaintext/blns.txt.004",
    "./test/files/plaintext/blns.txt.005",
    "./test/files/plaintext/blns.txt.006",
    "./test/files/plaintext/blns.txt.007",
    "./test/files/plaintext/blns.txt.008",
    "./test/files/plaintext/blns.txt.009",
    "./test/files/plaintext/blns.txt.010",
    "./test/files/plaintext/blns.txt.011",
    "./test/files/plaintext/blns.txt.012",
    "./test/files/plaintext/blns.txt.013",
    "./test/files/plaintext/blns.txt.014",
    "./test/files/plaintext/blns.txt.015",
    "./test/files/plaintext/blns.txt.016"
]


def test_symmetric_alice():
    with SplitFileReader(filepaths_alice) as sfr,\
            TextIOWrapper(sfr) as tiow,\
            open(filepath_alice, 'r') as base:
        for x, y in zip(tiow, base):
            assert x == y


def test_symmetric_blns():
    with SplitFileReader(filepaths_blns) as sfr,\
            TextIOWrapper(sfr, encoding="utf-8") as tiow,\
            open(filepath_blns, 'r', encoding="utf-8") as base:
        for x, y in zip(tiow, base):
            # print(x.strip())
            assert x == y
            # Look at each _character_, not _byte_.
            for char_x, char_y in zip(x, y):
                assert char_x == char_y


if __name__ == "__main__":
    os.chdir('..')
    test_symmetric_alice()
    test_symmetric_blns()
