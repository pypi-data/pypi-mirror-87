# SplitFileReader

A python module to transparently read files that have been split on disk, without combining them.  Exposes the 
`readable`, `read`, `writable`, `write`, `tellable`, `tell`, `seekable`, `seek`, `open` and `close` functions, as well
as a Context Manager and an Iterable.

### Usage
#### Simple Example
List all of the files within a TAR file that has been broken into multiple parts.
```python
import tarfile
from split_file_reader import SplitFileReader

filepaths = [
    "./files/archives/files.tar.000",
    "./files/archives/files.tar.001",
    "./files/archives/files.tar.002",
    "./files/archives/files.tar.003",
]

with SplitFileReader(filepaths) as sfr:
    with tarfile.open(fileobj=sfr, mode="r") as tf:
        for tff in tf.filelist:
            print("File in archive: ", tff.name)
```

#### Text files.
The `SplitFileReader` works only on binary data, but does support the use of the `io.TextIOWrapper`.

The `SplitFileReader` may also be given a glob for the filepaths.
```python
import glob
from io import TextIOWrapper

from split_file_reader import SplitFileReader

file_glob = glob.glob("./files/plaintext/Adventures_In_Wonderland.txt.*")
with SplitFileReader(file_glob) as sfr:
    with TextIOWrapper(sfr) as text_wrapper:
        for line in text_wrapper:
            print(line, end='')
```

These files may be anywhere on disk, or across multiple disks.

SplitFileReader does not support writing, `writable` will always return `False`, calls to `write` will raise an
IOError.

### Use case

Many large files are distributed in multiple parts, especially archives.  The general solution to reassembly is to call
`cat` from the terminal, and pipe them into a single cohesive file; however for various reasons this may not always be
possible or desirable.  If the full set of files is larger than the entire disk; if there is not enough space left to
`cat` them all together; or if only a small set of the payload data is required.
```bash
cat ./files/archives/files.zip.* > ./files/archives/file.zip
```

In these scenarios, using the `SplitFileReader` will provide an alternative solution, enabling random access throughout
the archive without making a single file on disk.

#### Github and Gitlab Large File Size

Github and Gitlab (as well as other file repositories) impose file size limits.  By parting these files into
sufficiently small chunks, the `SplitFileReader` will be able to make transparent use of them, as though they were a
single cohesive file.  This will remove any requirements to host these files with pre-fetch or pre-commit scripts, or
any other "setup" mechanism to make use of them.

#### Symmetric Download
Some HTTP file servers set maximum transfer windows.  With the `SplitFileReader`, each piece of data can be streamed
into its own file, and then used directly, without the need to reassemble them; by piping each file stream directly to 
disk.  The files will then be immediately available for use, without a recombination step.

#### Other Uses
Because the file type is transparent to the class, even CSV Files can be split and processed this way, provided
that the column headers are only present on the first file.  The CSV does not even need to be split along the rows, it 
can be split at any point (and even mid character for multi-byte characters). 

This library supports only binary read modes; to support decoding, wrap a String Buffer or other decoding system.
Because the component files may be split at any byte offset, it is possible that files are split mid-character.  This
will be transparant to any module wrapped around the SplitFileReader.

#### Random Access
This module allows for random access of the data, allowing for Tar or Zip files to be extracted without first combining
them.

```python
sfr = split_file_reader.open(filepaths)
with zipfile.ZipFile(sfr, "r") as zf:
    print(zf.filelist)
sfr.close()
```
Or, for text files:
```python
with SplitFileReader(filepaths) as sfr,\
        io.TextIOWrapper(sfr, encoding="utf-8") as tiow:
    for line in tiow:
        print(line, end='')
```

#### Streaming Access
The `SplitFileReader` can be used in a stream-only format, which disables the `seek` functionality.  It allows one to 
call `iter()` on the object, and then call `next()` to produce a stream of bytes; or, it may be wrapped in a `for` loop.

```python
with SplitFileReader(filepaths) as sfr:
    for b in sfr:
        print("{:02X}", b)
```
Or, to produce fixed amounts of data, the `set_iter_size(size)` function can be called, which will read up to the `size` 
amount of data.  `set_iter_size` may be called at any point, even inside the loop.
```python
with SplitFileReader(filepaths) as sfr:
    sfr.set_iter_size(16)
    for byte_list in sfr:
        print(" ".join("{:02X}".format(x) for x in byte_list))
```

Additionally, adding the `streaming_only=True` argument to the initializer will force this mode, but will not create
an iterable.   `iter()` must still be called, either explicitly, or implied via a loop. 

An existiing `SplitFileReader` instance may be converted to Streaming mode at any time, but may not be converted back
to random-access mode.

#### Constructor Arguments
- `files`: a list of zero or more strings, with either a fully qualified explicit location, or a relative location.
These file paths are whatever `builtins.open()` would need.
  - An empty list will always read nothing, and finish iterating immediately.
  - A list with a single file will simply wrap a single file, as a pass-through.
  - Otherwise, each of these files will be opened, one at a time, in the given order.
- `mode`: this must be `rb` or `r`.  It is only left for programs that explicitly set the `mode` argument.
- `stream_only`: Disables the `seek()` method.  The `__init__` will still not return an iterator, must still use 
`__iter__` for that.  Mutually exclusive with `validate_all_readable`
- `validate_all_readable`: Seek to every file in the `files` list, and check if readbale.  Calls `test_all_readable`
method at the end of the constructor.  Mutually exclusive with `stream_only`

#### Context Manager
The `SplitFileReader` allows for a Context Manager.  It simply calls `close()` at exit.

## Command Line Invocation
The module may be used via the command line for some simple processing of certain archive types.  Presently, only Tar
and Zip formats are supported, and they must have been split via the `split` command, or other binary split mechanism.


```
usage:  [-h] [-a {zip,z,tar,t,tgz,tbz,txz}] [-p <password>]
        (-t | -l | -x <destination> | -r <filename>)
        <filepath> [<filepath> ...]

Identify and process parted archives without manual concat. This command line
capability provides supports only Tar and Zip files; but not 7z or Rar.
Designed to work for files that have been split via the `split` utility, or
any other binary cut; but does not support Zip's built-in split capability.
The python module supports any arbitrarily split files, regardless of type.

positional arguments:
  <filepath>            In-order list of the parted files on disk. Use shell
                        expansion, such as ./files.zip.*

optional arguments:
  -h, --help            show this help message and exit
  -a {zip,z,tar,t,tgz,tbz,txz}, --archive {zip,z,tar,t,tgz,tbz,txz}
                        Archive type, either zip, tar, tgz, tbz, or txz
  -p <password>, --password <password>
                        Zip password, if needed
  -t, --test            Test the archive, using the module's built-in test.
  -l, --list            List all the payload files in the archive.
  -x <destination>, --extract <destination>
                        Extract the entire archive to filepath <destination>.
  -r <filename>, --read <filename>
                        Read out payload file contents to stdout.
```

#### Examples
To display the contents of the Zip files included in the test suite of this modules, run
```bash
python3 -m split_file_reader -azip --list ./files/archives/files.zip.*
```
The bash autoexpansion of the `*` wildcard will fill in the files in order, correctly.  `--list` will print out the 
names of the payload fiels within the zip archive, and the `-azip` flag instructs the module to expect the `Zip`
 archive type.

### Mechanics
#### File Descriptors
The `SplitFileReader` will make use of only a single File Descriptor at a time.  In random-access mode, the default
mode, as the file pointer moves over file boundaries, the existing File Descriptor will be closed before a new one is
opened.  For functions that regularly seek and read over a file boundary, the File Descriptors will be opened and 
closed often.  For streaming mode, once a file's File Descriptor is closed, a new one will not be created.

Just like with `open()`, a File Descriptor will be kept open unless `close()` is called on the object.  Using the
Context Managed version with the `with` keyword will automatically close the last file descriptor.  `SplitFileReader`
exposes a `close()` method for this.

Reading beyond the end of the list of files will cause `read()` to return nothing, but will not close the last File
Descriptor.  A `read()` call that crosses the file boundaries will close one and open another, transparently to the
calling Python code, but will always keep one File Descriptor open.  The same applies to `seek()`.

#### Concurrency
The `SplitFileReader` is not designed for concurrent or threaded access, it behaves the same as any other file that
has been opened via `open()` (and in fact uses the `builtins.open()` to operate.)  However, since the data it operates
against is read-only, multiple `SplitFileReader`s can be opened against the same data at the same time.

#### Caveats
While this class can open any arbitrarily split data, Zip chunks that are produced by the `zip` command are *not* simple
binary chunks.  They are logically divided in a separate way.  Zip files that have been parted via the `split` command,
after or during their creation, will work just fine.

Because the `SplitFileReader` allows random-access to the component files, the `files` list must also be random-access,
indexable, and contain only filepaths.  It cannot be generator, even if `streaming-only` is set `True`.

This library has not been tested with Python2.7, and compatibility was not considered.
