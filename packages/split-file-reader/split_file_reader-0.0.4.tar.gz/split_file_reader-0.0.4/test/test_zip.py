import hashlib
import os
import zipfile

from split_file_reader import SplitFileReader

"""
dd if=/dev/urandom of=random_payload_1.bin bs=1024 count=256
dd if=/dev/urandom of=random_payload_2.bin bs=1024 count=256
dd if=/dev/urandom of=random_payload_3.bin bs=1024 count=256
dd if=/dev/urandom of=random_payload_4.bin bs=1024 count=256
dd if=/dev/urandom of=random_payload_5.bin bs=1024 count=256
tar -cvzf files.tar random_payload_*
split -d -n3 -a3 files.zip files.zip.
"""

filepath_prefix = "./test/files/archives/"

zip_parted_filepaths = [
    "./test/files/archives/files.zip.000",
    "./test/files/archives/files.zip.001",
    "./test/files/archives/files.zip.002",
]

zip_filepath = "./test/files/archives/files.zip"

payload_files = [
    "random_payload_1.bin",
    "random_payload_2.bin",
    "random_payload_3.bin",
    "random_payload_4.bin",
    "random_payload_5.bin",
]


def test_simple_zip_archive_random_access():
    """
    Put the SplitFileReader around just the single complete zip file, not actual split names to traverse.
    Also do a traverse of the original zip archive to ensure the values match.
    Then pull the original names in, and check their values as well.
    :return:
    """
    sfr = SplitFileReader([zip_filepath], "rb")
    with zipfile.ZipFile(sfr, "r") as split_zf, zipfile.ZipFile(zip_filepath, "r") as original_zf:
        # This is a hack for IDE typehints.
        split_zf: zipfile.ZipFile = split_zf
        original_zf: zipfile.ZipFile = original_zf
        for payload_file in payload_files:
            split_zff = split_zf.open(payload_file)
            split_hasher = hashlib.md5()
            split_hasher.update(split_zff.read())
            split_zff_payload_actual_hash = split_hasher.hexdigest().lower()

            original_zff = original_zf.open(payload_file)
            original_hasher = hashlib.md5()
            original_hasher.update(original_zff.read())
            original_zff_payload_actual_hash = original_hasher.hexdigest().lower()

            with open(filepath_prefix + payload_file, "rb") as pf:
                split_hasher = hashlib.md5()
                split_hasher.update(pf.read())
                expected_hash = split_hasher.hexdigest().lower()

            assert expected_hash == split_zff_payload_actual_hash
            assert expected_hash == original_zff_payload_actual_hash
    sfr.close()


def test_zip_archive_random_access():
    sfr = SplitFileReader(zip_parted_filepaths, "rb")
    with zipfile.ZipFile(sfr, "r") as split_zf:
        # This is a hack for IDE typehints.
        split_zf: zipfile.ZipFile = split_zf
        for payload_file in payload_files:
            split_zff = split_zf.open(payload_file)
            split_hasher = hashlib.md5()
            split_hasher.update(split_zff.read())
            split_zff_payload_actual_hash = split_hasher.hexdigest().lower()

            with open(filepath_prefix + payload_file, "rb") as pf:
                split_hasher = hashlib.md5()
                split_hasher.update(pf.read())
                expected_hash = split_hasher.hexdigest().lower()

            assert expected_hash == split_zff_payload_actual_hash
    sfr.close()


def test_context_managed_zip_archive():
    with SplitFileReader(zip_parted_filepaths, "rb") as sfr:
        with zipfile.ZipFile(sfr, "r") as split_zf:
            # This is a hack for IDE typehints.
            split_zf: zipfile.ZipFile = split_zf
            for payload_file in payload_files:
                split_zff = split_zf.open(payload_file)
                split_hasher = hashlib.md5()
                split_hasher.update(split_zff.read())
                split_zff_payload_actual_hash = split_hasher.hexdigest().lower()

                with open(filepath_prefix + payload_file, "rb") as pf:
                    split_hasher = hashlib.md5()
                    split_hasher.update(pf.read())
                    expected_hash = split_hasher.hexdigest().lower()

                assert expected_hash == split_zff_payload_actual_hash
    try:
        sfr.seek(1)
    except IOError as e:
        assert True
    else:
        assert False, "Should have raised an IO Error for a seek on a closed file."


def test_class_open_zip_archive():
    sfr = SplitFileReader.open(zip_parted_filepaths, "rb")
    with zipfile.ZipFile(sfr, "r") as split_zf:
        # This is a hack for IDE typehints.
        split_zf: zipfile.ZipFile = split_zf
        for payload_file in payload_files:
            split_zff = split_zf.open(payload_file)
            split_hasher = hashlib.md5()
            split_hasher.update(split_zff.read())
            split_zff_payload_actual_hash = split_hasher.hexdigest().lower()

            with open(filepath_prefix + payload_file, "rb") as pf:
                split_hasher = hashlib.md5()
                split_hasher.update(pf.read())
                expected_hash = split_hasher.hexdigest().lower()

            assert expected_hash == split_zff_payload_actual_hash
    sfr.close()
    try:
        sfr.read(1)
    except IOError as e:
        assert True
    else:
        assert False, "Should have raised an IO Error for a read on a closed file."


if __name__ == "__main__":
    os.chdir('..')
    test_simple_zip_archive_random_access()
    test_zip_archive_random_access()
    test_context_managed_zip_archive()
    test_class_open_zip_archive()
