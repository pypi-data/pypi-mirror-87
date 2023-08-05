import shlex
import io
from contextlib import redirect_stdout, redirect_stderr

from split_file_reader.__main__ import main


def test_main_zip_list():
    with io.StringIO() as output_buffer, redirect_stdout(output_buffer):
        main(shlex.split("--list -az ./test/files/archives/files.zip.000 ./test/files/archives/files.zip.001 "
                         "./test/files/archives/files.zip.002"))
        output = output_buffer.getvalue()
    lines = output.splitlines()
    assert lines[0] == "random_payload_1.bin"
    assert lines[1] == "random_payload_2.bin"
    assert lines[2] == "random_payload_3.bin"
    assert lines[3] == "random_payload_4.bin"
    assert lines[4] == "random_payload_5.bin"


def test_main_tar_list():
    with io.StringIO() as output_buffer, redirect_stdout(output_buffer):
        main(shlex.split("-l --archive=tar ./test/files/archives/files.tar.000 ./test/files/archives/files.tar.001 "
                         "./test/files/archives/files.tar.002 ./test/files/archives/files.tar.003"))
        output = output_buffer.getvalue()
    lines = output.splitlines()
    assert lines[0] == "random_payload_1.bin"
    assert lines[1] == "random_payload_2.bin"
    assert lines[2] == "random_payload_3.bin"
    assert lines[3] == "random_payload_4.bin"
    assert lines[4] == "random_payload_5.bin"


def test_main_tar_test():
    # The `tar` module test arguments write to stderr, instead of stdout.
    with io.StringIO() as output_buffer, redirect_stdout(output_buffer):
        with io.StringIO() as err_buffer, redirect_stderr(err_buffer):
            main(shlex.split("-t -at ./test/files/archives/files.tar.000 ./test/files/archives/files.tar.001 "
                             "./test/files/archives/files.tar.002 ./test/files/archives/files.tar.003"))
            output = output_buffer.getvalue()
            errput = err_buffer.getvalue()
    errput = errput[1:-2]
    errput = errput.split(",")
    errput = [x.strip() for x in errput]
    print(errput)
    assert errput[0].startswith("<TarInfo 'random_payload_1.bin' at ")
    assert errput[1].startswith("<TarInfo 'random_payload_2.bin' at ")
    assert errput[2].startswith("<TarInfo 'random_payload_3.bin' at ")
    assert errput[3].startswith("<TarInfo 'random_payload_4.bin' at ")
    assert errput[4].startswith("<TarInfo 'random_payload_5.bin' at ")


if __name__ == "__main__":
    os.chdir('..')
    test_main_zip_list()
    test_main_tar_list()
    test_main_tar_test()
