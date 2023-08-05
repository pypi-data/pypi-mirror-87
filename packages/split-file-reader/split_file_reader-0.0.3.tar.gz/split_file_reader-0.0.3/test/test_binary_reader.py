import os
import tarfile
import zipfile

from split_file_reader import SplitFileReader

tarfile_path = "./test/files/archives/files.tar"
zipfile_path = "./test/files/archives/files.zip"


def test_tar_validate():
    with tarfile.open(tarfile_path, 'r|') as tf:
        for tff in tf:
            print(tff)


def test_zip_validate():
    print(test_zip_validate)
    with zipfile.ZipFile(zipfile_path, 'r') as zf:
        for zff in zf.infolist():
            print(zff)
        assert zf.testzip() is None, "Baseline Zipfile is not valid."


def test_tar_simple_iter_read():
    print("test_tar_simple_iter_read")
    filepaths = [ tarfile_path ]
    sfr = SplitFileReader(filepaths, stream_only=True)
    with tarfile.open(fileobj=sfr, mode='r|') as tf:
        for tff in tf:
            print(tff)


def test_tar_compound_iter_read():
    print("test_tar_compound_simple_iter_read")
    filepaths = [
        "./test/files/archives/files.tar.000",
        "./test/files/archives/files.tar.001",
        "./test/files/archives/files.tar.002",
        "./test/files/archives/files.tar.003",
    ]
    sfr = SplitFileReader(filepaths, stream_only=True)
    with tarfile.open(fileobj=sfr, mode='r|') as tf:
        for tff in tf:
            print(tff)


if __name__ == "__main__":
    os.chdir('..')
    test_zip_validate()
    test_tar_validate()
    test_tar_simple_iter_read()
    test_tar_compound_iter_read()
