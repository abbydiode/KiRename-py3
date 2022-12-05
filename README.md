# KiRename

Rename a KiCad project


## Usage

```
python kirename.py [-s <source>] [-d <dest>] [-n <name> ] [ -t <tag> ]

-s               Source directory (./)
-d               Destination directory (./)
-n               New name
-t               Tag to add
-x               Dry run, do not change any files
-h (--help)      You're here
```

## Examples

| Description | Command |
| ----------- | ------- |
| Rename project in current directory to `foo` | `python kirename.py -n foo` |
| Rename project in directory `foo` to `bar` | `python kirename.py -s ./foo -n bar`
| Append `_v1` to project in current directory | `python kirename.py -t _v1` |
