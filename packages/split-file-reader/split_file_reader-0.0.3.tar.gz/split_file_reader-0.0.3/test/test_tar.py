import hashlib
import os
import tarfile

from split_file_reader import SplitFileReader

"""
dd if=/dev/urandom of=random_payload_1.bin bs=1024 count=256
dd if=/dev/urandom of=random_payload_2.bin bs=1024 count=256
dd if=/dev/urandom of=random_payload_3.bin bs=1024 count=256
dd if=/dev/urandom of=random_payload_4.bin bs=1024 count=256
dd if=/dev/urandom of=random_payload_5.bin bs=1024 count=256
tar -cvzf files.tar random_payload_*
split -d -n4 -a3 files.tar files.tar.
"""

filepath_prefix = "./test/files/archives/"

tar_parted_filepaths = [
    "./test/files/archives/files.tar.000",
    "./test/files/archives/files.tar.001",
    "./test/files/archives/files.tar.002",
    "./test/files/archives/files.tar.003",
]

tar_filepath = "./test/files/archives/files.tar"

payload_files = [
    "random_payload_1.bin",
    "random_payload_2.bin",
    "random_payload_3.bin",
    "random_payload_4.bin",
    "random_payload_5.bin",
]


def test_simple_tar_archive_random_access():
    """
    This puts a SplitFileReader around the original tar archive, and compares it to opening the original tar archive
    in parallel, and then checks the on-disk original payload files.  If all three approaches to getting to the original
    payload files produce the same hashes, it passes.
    :return:
    """
    # put the SplitFileReader around just the single complete Tar file, no actual files to traverse.
    sfr = SplitFileReader([tar_filepath], "rb")
    print(sfr)
    with tarfile.open(fileobj=sfr, mode="r") as split_tf, tarfile.open(tar_filepath, "r") as original_tf:
        # This is a hack for IDE typehints.
        split_tf: tarfile.TarFile = split_tf
        original_tf: tarfile.TarFile = original_tf

        for payload_file in payload_files:
            split_tff = split_tf.extractfile(payload_file)
            split_hasher = hashlib.md5()
            split_hasher.update(split_tff.read())
            split_tff_payload_actual_hash = split_hasher.hexdigest().lower()

            original_tff = original_tf.extractfile(payload_file)
            original_hasher = hashlib.md5()
            original_hasher.update(original_tff.read())
            original_tff_payload_actual_hash = original_hasher.hexdigest().lower()

            with open(filepath_prefix + payload_file, "rb") as pf:
                split_hasher = hashlib.md5()
                split_hasher.update(pf.read())
                expected_hash = split_hasher.hexdigest().lower()

            assert expected_hash == split_tff_payload_actual_hash
            assert expected_hash == original_tff_payload_actual_hash


def test_tar_archive_random_access():
    sfr = SplitFileReader(tar_parted_filepaths, "rb")
    with tarfile.open(fileobj=sfr, mode="r:*") as tf:
        # This is a hack for IDE typehints.
        tf: tarfile.TarFile = tf
        for payload_file in payload_files:
            tff = tf.extractfile(payload_file)
            hasher = hashlib.md5()
            hasher.update(tff.read())
            tff_payload_actual_hash = hasher.hexdigest().lower()

            with open(filepath_prefix + payload_file, "rb") as pf:
                hasher = hashlib.md5()
                hasher.update(pf.read())
                expected_hash = hasher.hexdigest().lower()

            assert expected_hash == tff_payload_actual_hash


def test_tar_archive_stream():
    sfr = SplitFileReader(tar_parted_filepaths, "rb", stream_only=True)
    with tarfile.open(fileobj=sfr, mode="r|") as tf:
        # This is a hack for IDE typehints.
        tf: tarfile.TarFile = tf
        for member in tf:
            member: tarfile.TarInfo = member
            # print("Streaming Tar member: {}".format(member))
            tff = tf.extractfile(member)
            hasher = hashlib.md5()
            hasher.update(tff.read())
            tff_payload_actual_hash = hasher.hexdigest().lower()

            with open("./test/files/archives/" + member.name, "rb") as pf:
                hasher = hashlib.md5()
                hasher.update(pf.read())
                expected_hash = hasher.hexdigest().lower()

            assert expected_hash == tff_payload_actual_hash


if __name__ == "__main__":
    os.chdir('..')
    test_simple_tar_archive_random_access()
    test_tar_archive_random_access()
    test_tar_archive_stream()
