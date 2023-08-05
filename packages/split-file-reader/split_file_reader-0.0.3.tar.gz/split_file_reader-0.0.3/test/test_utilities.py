import hashlib
import io
import os
import random

# The XXD utility is a python module that replicates the Linux `xxd` hexdump utility.  It is included for debug
# display purposes only.  All lines referencing it may be removed without affecting the tests.
# import xxd
import pytest

from split_file_reader import SplitFileReader
"""
    The `forward_only` tests are forward-only.  Stream-like.  
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


def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def test_validate_files_argument():
    sfr = SplitFileReader([filepath_original], validate_all_readable=True)
    assert sfr.tell() == 0
    sfr.read(52)
    sfr.test_all_readable()
    assert sfr.tell() == 52
    sfr.close()


def test_tostr():
    sfr = SplitFileReader(filepaths, validate_all_readable=True)
    strung = str(sfr)
    sfr.read(1)
    sfr.seek(55000)
    strung = str(sfr)
    split = strung.split(' ')
    assert strung[0] == '<'
    assert strung[-1] == '>'
    assert split[3] == '55000,'
    fileno = split[6].split(',')[0]
    assert is_integer(fileno)
    assert split[-1] == '13114>'

    sfr.seek(0)
    sfr.read(1)
    strung = str(sfr)
    sfr.close()


def test_unsupported():
    with SplitFileReader(filepaths) as sfr:
        with pytest.raises(io.UnsupportedOperation):
            sfr.readline()
        with pytest.raises(io.UnsupportedOperation):
            sfr.readlines()
        with pytest.raises(io.UnsupportedOperation):
            sfr.write(b"Hello")
        with pytest.raises(io.UnsupportedOperation):
            sfr.truncate()


if __name__ == "__main__":
    os.chdir('..')
    test_validate_files_argument()
    test_tostr()
    test_unsupported()
