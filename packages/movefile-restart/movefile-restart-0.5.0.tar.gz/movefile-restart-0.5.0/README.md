# python-movefile-restart

A small library to move, delete, and rename files at Windows restart time.

## Installation

`pip install movefile-restart` or `pip3 install movefile-restart`, depending on your configuration of Python and Pip.

## Usage

To import, use `import movefile_restart`

From there, you have a couple functions at your disposal:

`movefile_restart.DeleteFile(file_path)`: Queues `file_path` for deletion.

`movefile_restart.MoveFile(from_path, to_path)` or `movefile_restart.RenameFile(from_path, to_path)`: Moves the file from `from_path` to `to_path`.

`movefile_restart.GetFileOperations()`: Get a list of tuples containing the source and destination of all file movings queued.

`movefile_restart.PrintFileOperations()`: Print a list of file operations that are scheduled to occur during reboot.

## Current Limitations

* Files cannot currently be un-queued.
* Some weird cases such as: if you're moving `a.txt` to `b.txt`, you cannot queue a deletion for `b.txt` after your file move queue. You would have to restart the computer so `b.txt` exists before deleting it.
* Due to using the Windows Registry for handling these kinds of operations, no other operating system is supported, nor is there planned support.