import hashlib
import os
import random

from split_file_reader import SplitFileReader

filepaths = [
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
expected_hash = "7bf855f82dc4af7ee34d65b662bbc58e"
expected_size = 167544


def test_iter_simple():
    with SplitFileReader(filepaths) as sfr:
        split_hasher = hashlib.md5()
        for b in sfr:
            split_hasher.update(b)
        actual_hash = split_hasher.hexdigest().lower()
        assert actual_hash == expected_hash


def test_iter_larger():
    with SplitFileReader(filepaths) as sfr:
        split_hasher = hashlib.md5()
        next_read_size = 12
        sfr.set_iter_size(next_read_size)
        for b in sfr:
            split_hasher.update(b)
            # Last read can be short.
            if sfr.tell() != 167544:
                assert len(b) == next_read_size
                assert len(b) >= 10
            assert len(b) < 20
            next_read_size = random.randrange(10, 20)
            sfr.set_iter_size(next_read_size)
            # print(" ".join("{:02X}".format(x) for x in b))
        actual_hash = split_hasher.hexdigest().lower()
        assert actual_hash == expected_hash


if __name__ == "__main__":
    os.chdir('..')
    test_iter_simple()
    test_iter_larger()
