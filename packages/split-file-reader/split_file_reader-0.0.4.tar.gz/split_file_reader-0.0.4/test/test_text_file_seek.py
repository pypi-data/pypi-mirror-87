import hashlib
import os
import random

import pytest

from split_file_reader import SplitFileReader
"""
    The `forward_only` tests are forward-only.  Stream-like.
    
    CAREFUL:  These tests are against an ASCII-only text file, meaning that every character is exactly one byte.
    Take care to wrap text files in a TextIOWrapper for proper decoding, see test_textio_wrapper.py  
"""

filepath_original = "./test/files/plaintext/Adventures_In_Wonderland.txt"

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


def trace(s, *args, **kwargs):
    # print(s, *args, **kwargs)
    pass


def test_forward_only_tell():
    hasher = hashlib.md5()
    expected_tell = 0
    sfr = SplitFileReader([filepath_original])

    next_read_size = random.randrange(100, 200)
    expected_tell += next_read_size
    block = sfr.read(next_read_size)
    # trace("Tell: {}  Calculated: {}".format(sfr.tell(), expected_tell))
    assert sfr.tell() == expected_tell

    while block:
        # trace(str(block, encoding="utf-8"))
        hasher.update(block)

        next_read_size = random.randrange(1000, 20000)
        expected_tell += next_read_size
        block = sfr.read(next_read_size)
        if expected_tell > expected_size:
            expected_tell = expected_size
        # trace("Tell: {}  Calculated: {}".format(sfr.tell(), expected_tell))
        assert sfr.tell() == expected_tell
    actual = hasher.hexdigest().lower()
    trace(actual)
    trace(expected_hash)
    assert actual == expected_hash


def test_compound_forward_only_tell():
    hasher = hashlib.md5()
    expected_tell = 0
    sfr = SplitFileReader(filepaths)

    next_read_size = random.randrange(100, 200)
    expected_tell += next_read_size
    block = sfr.read(next_read_size)
    # trace("Tell: {}  Calculated: {}".format(sfr.tell(), expected_tell))
    assert sfr.tell() == expected_tell

    while block:
        # trace(str(block, encoding="utf-8"))
        hasher.update(block)

        next_read_size = random.randrange(1000, 20000)
        expected_tell += next_read_size
        block = sfr.read(next_read_size)
        if expected_tell > expected_size:
            expected_tell = expected_size
        # trace("Tell: {}  Calculated: {}".format(sfr.tell(), expected_tell))
        assert sfr.tell() == expected_tell
    actual = hasher.hexdigest().lower()
    trace(actual)
    trace(expected_hash)
    assert actual == expected_hash


def test_forward_alternate_seek_from_one_and_read():
    trace(test_forward_alternate_seek_from_one_and_read.__name__)
    expected_tell = 0
    sfr_normal = SplitFileReader(filepaths.copy())
    sfr_seeker = SplitFileReader(filepaths.copy())

    next_read_size = random.randrange(10, 20)
    expected_tell += next_read_size
    block_normal = sfr_normal.read(next_read_size)
    # Even though not used, read must happen to keep them in sync.
    block_seeker = sfr_seeker.read(next_read_size)
    # trace("Tell: {}  Calculated: {}".format(sfr.tell(), expected_tell))
    # xxd.print_xxd_dump_symmetric(*(block_seeker, block_normal))
    assert sfr_normal.tell() == expected_tell
    assert sfr_seeker.tell() == expected_tell

    iter_count = 0

    while block_normal:
        iter_count += 1
        trace("Iterate: {}".format(iter_count))

        next_read_size = random.randrange(10, 20)
        expected_tell += next_read_size

        # normal always reads.
        block_normal = sfr_normal.read(next_read_size)
        if not iter_count % 2:
            trace("block_seeker is reading")
            # Alternate reads.
            block_seeker = sfr_seeker.read(next_read_size)
            if not block_normal == block_seeker:
                # for (x, y) in zip(xxd.xxd_dump(block_normal), xxd.xxd_dump(block_seeker)):
                #     trace("{} : {}".format(x, y))
                # xxd.print_xxd_dump_symmetric(*(block_seeker, block_normal))
                assert block_normal == block_seeker
        else:
            trace("block_seeker is skipping")
            # Alternate seeks.
            sfr_seeker.seek(next_read_size, 1)
        if expected_tell > expected_size:
            expected_tell = expected_size
        assert sfr_normal.tell() == expected_tell
        assert sfr_seeker.tell() == expected_tell
    assert sfr_normal.tell() == expected_tell
    assert sfr_seeker.tell() == expected_tell
    assert expected_tell == expected_size


def test_forward_alternate_seek_from_zero_and_read():
    expected_tell = 0
    sfr_normal = SplitFileReader(filepaths)
    sfr_seeker = SplitFileReader(filepaths)

    next_read_size = random.randrange(100, 200)
    expected_tell += next_read_size
    block_normal = sfr_normal.read(next_read_size)
    sfr_seeker.seek(expected_tell, 0)
    # trace("Tell: {}  Calculated: {}".format(sfr.tell(), expected_tell))
    assert sfr_normal.tell() == expected_tell
    assert sfr_seeker.tell() == expected_tell

    iter_count = 0

    while block_normal:
        iter_count += 1
        next_read_size = random.randrange(1000, 20000)
        expected_tell += next_read_size
        block_normal = sfr_normal.read(next_read_size)
        if not iter_count % 2:
            block_seeker = sfr_seeker.read(next_read_size)
            assert block_normal == block_seeker
        else:
            sfr_seeker.seek(expected_tell, 0)
        if expected_tell > expected_size:
            expected_tell = expected_size
        assert sfr_normal.tell() == expected_tell
        assert sfr_seeker.tell() == expected_tell
    assert sfr_normal.tell() == expected_tell
    assert sfr_seeker.tell() == expected_tell
    assert expected_tell == expected_size


def test_forward_alternate_seek_from_two_and_read():
    expected_tell = 0
    sfr_normal = SplitFileReader(filepaths)
    sfr_seeker = SplitFileReader(filepaths)

    next_read_size = random.randrange(100, 200)
    expected_tell += next_read_size
    block_normal = sfr_normal.read(next_read_size)
    sfr_seeker.seek(-(expected_size - expected_tell), 2)
    trace("Reader Tell: {}  Seeker Tell: {}  Calculated: {}".format(
        sfr_normal.tell(), sfr_seeker.tell(), expected_tell))
    assert sfr_normal.tell() == expected_tell
    assert sfr_seeker.tell() == expected_tell

    iter_count = 0

    while block_normal:
        iter_count += 1
        trace("Iterate: {}".format(iter_count))
        next_read_size = random.randrange(1000, 20000)
        expected_tell += next_read_size
        block_normal = sfr_normal.read(next_read_size)
        # Test alternating read and seek, to ensure they stay in sync.
        if not iter_count % 2:
            block_seeker = sfr_seeker.read(next_read_size)
            assert block_normal == block_seeker
        else:
            sfr_seeker.seek(-(expected_size - expected_tell), 2)
        if expected_tell > expected_size:
            expected_tell = expected_size

        if sfr_seeker.tell() > expected_tell:
            trace("Its okay to go off the end.  Check if we did.")
            trace("Expected Tell:", expected_tell, "Seeker Tell:", sfr_seeker.tell())
        assert sfr_normal.tell() == expected_tell
        assert sfr_seeker.tell() == expected_tell
    assert sfr_normal.tell() == expected_tell
    assert sfr_seeker.tell() == expected_tell
    assert expected_tell == expected_size


if __name__ == "__main__":
    os.chdir('..')
    test_forward_only_tell()
    test_compound_forward_only_tell()
    test_forward_alternate_seek_from_one_and_read()
    test_forward_alternate_seek_from_zero_and_read()
    test_forward_alternate_seek_from_two_and_read()
