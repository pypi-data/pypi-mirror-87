import hashlib
import os
import random

from split_file_reader import SplitFileReader
"""
    The `forward_only` tests are forward-only.  Stream-like.  
"""

"""
$ cat Adventures_In_Wonderland.txt | md5sum
7bf855f82dc4af7ee34d65b662bbc58e *-

$ cat Adventures_In_Wonderland.txt.* | md5sum
7bf855f82dc4af7ee34d65b662bbc58e *-

$ md5sum *
7bf855f82dc4af7ee34d65b662bbc58e *Adventures_In_Wonderland.txt
99d9cc2ef43215aac8a74ccf2a8d308a *Adventures_In_Wonderland.txt.000
48e1eadb116a6964748c307f8d2bb059 *Adventures_In_Wonderland.txt.001
aef56a3ac176997891f807737725ca58 *Adventures_In_Wonderland.txt.002
fe970d16d8b5f053fa3f09fdba08d422 *Adventures_In_Wonderland.txt.003
eb7e73becdd965a6d5d063d841d02a1d *Adventures_In_Wonderland.txt.004
86a1967a846d11a3e9f50bd1c867b9b3 *Adventures_In_Wonderland.txt.005
4ee296d0f7dd03a704755a812cbe61df *Adventures_In_Wonderland.txt.006
6b138b0bcf7aaf4f592a053a2f485342 *Adventures_In_Wonderland.txt.007
e70fb50e8269fa8e14c988a678d56984 *Adventures_In_Wonderland.txt.008
8848c479069da54b2ba7f6101dfe0841 *Adventures_In_Wonderland.txt.009
4850771bea5b7fca21a98ae24dd381bf *Adventures_In_Wonderland.txt.010
200d31f53d701f9a80cb6dae2387f285 *Adventures_In_Wonderland.txt.011

"""

single_filepath = [
"./test/files/plaintext/Adventures_In_Wonderland.txt"
]

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


def test_forward_only_read():
    hasher = hashlib.md5()
    sfr = SplitFileReader(single_filepath)
    block = sfr.read(4096)
    while block:
        # print(str(block, encoding="utf-8"))
        hasher.update(block)
        block = sfr.read(4096)
    actual = hasher.hexdigest().lower()
    print(actual)
    print(expected_hash)
    assert actual == expected_hash


def test_forward_only_read_each():
    file_parts = [
        ("99d9cc2ef43215aac8a74ccf2a8d308a", "Adventures_In_Wonderland.txt.000"),
        ("48e1eadb116a6964748c307f8d2bb059", "Adventures_In_Wonderland.txt.001"),
        ("aef56a3ac176997891f807737725ca58", "Adventures_In_Wonderland.txt.002"),
        ("fe970d16d8b5f053fa3f09fdba08d422", "Adventures_In_Wonderland.txt.003"),
        ("eb7e73becdd965a6d5d063d841d02a1d", "Adventures_In_Wonderland.txt.004"),
        ("86a1967a846d11a3e9f50bd1c867b9b3", "Adventures_In_Wonderland.txt.005"),
        ("4ee296d0f7dd03a704755a812cbe61df", "Adventures_In_Wonderland.txt.006"),
        ("6b138b0bcf7aaf4f592a053a2f485342", "Adventures_In_Wonderland.txt.007"),
        ("e70fb50e8269fa8e14c988a678d56984", "Adventures_In_Wonderland.txt.008"),
        ("8848c479069da54b2ba7f6101dfe0841", "Adventures_In_Wonderland.txt.009"),
        ("4850771bea5b7fca21a98ae24dd381bf", "Adventures_In_Wonderland.txt.010"),
        ("200d31f53d701f9a80cb6dae2387f285", "Adventures_In_Wonderland.txt.011"),
    ]
    for file_part in file_parts:
        filehash, filepath = file_part

        hasher = hashlib.md5()
        sfr = SplitFileReader(["./test/files/plaintext/" + filepath])
        block = sfr.read(4096)
        while block:
            # print(str(block, encoding="utf-8"))
            hasher.update(block)
            block = sfr.read(4096)
        actual = hasher.hexdigest().lower()
        assert actual == filehash


def test_forward_only_iter_read():
    hasher = hashlib.md5()
    sfr = SplitFileReader(single_filepath, stream_only=True)
    for block in sfr:
        # print(str(block, encoding="utf-8"))
        hasher.update(block)
    actual = hasher.hexdigest().lower()
    print(actual)
    print(expected_hash)
    assert actual == expected_hash


def test_compound_forward_only_read():
    hasher = hashlib.md5()
    sfr = SplitFileReader(filepaths)
    block = sfr.read(4096)
    while block:
        # print(str(block, encoding="utf-8"))
        hasher.update(block)
        block = sfr.read(4096)
    actual = hasher.hexdigest().lower()
    print(actual)
    print(expected_hash)
    assert actual == expected_hash


def test_compound_forward_only_tell():
    hasher = hashlib.md5()
    expected_tell = 0
    sfr = SplitFileReader(filepaths)

    next_read_size = random.randrange(100, 200)
    expected_tell += next_read_size
    block = sfr.read(next_read_size)
    # print("Tell: {}  Calculated: {}".format(sfr.tell(), expected_tell))
    assert sfr.tell() == expected_tell

    while block:
        # print(str(block, encoding="utf-8"))
        hasher.update(block)

        next_read_size = random.randrange(1000, 20000)
        expected_tell += next_read_size
        block = sfr.read(next_read_size)
        if expected_tell > expected_size:
            expected_tell = expected_size
        # print("Tell: {}  Calculated: {}".format(sfr.tell(), expected_tell))
        assert sfr.tell() == expected_tell
    actual = hasher.hexdigest().lower()
    print(actual)
    print(expected_hash)
    assert actual == expected_hash


def test_compound_forward_only_iter_read():
    hasher = hashlib.md5()
    sfr = SplitFileReader(filepaths, stream_only=True)
    for block in sfr:
        # print(str(block, encoding="utf-8"))
        hasher.update(block)
    actual = hasher.hexdigest().lower()
    print(actual)
    print(expected_hash)
    print("tell", sfr.tell())
    assert actual == expected_hash


if __name__ == "__main__":
    os.chdir('..')
    test_forward_only_read()
    test_forward_only_read_each()
    test_forward_only_iter_read()
    test_compound_forward_only_read()
    test_compound_forward_only_tell()
    test_compound_forward_only_iter_read()
