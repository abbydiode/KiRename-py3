# KiRename

## Installation

**Note:** You need to have Python3 and git installed for this to work.

1. Clone the repository by running `git clone https://github.com/abbydiode/KiRename-py3.git`
2. Move into the cloned directory with `cd KiRename-py3`
3. Run `python kirename` to view the command usage

```output
Usage: python kirename.py [-s <source>] [-d <dest>] [-n <name> ] [ -t <tag> ]

-s              Source directory (default: ./)
-d              Destination directory (default: ./)
-n              New project name
-t              Text to append
-x              Dry run, do not change any files
-h (--help)     You're here
```

## Usage

| Example | Command |
|---------|---------|
| Rename project in current directory to `foo` | `python kirename.py -n foo` |
| Rename project in directory `foo` to `bar` | `python kirename.py -s ./foo -n bar` |
| Append `_v1` to project in current directory | `python kirename.py -t _v1` |
