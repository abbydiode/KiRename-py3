# KiRename

Rename a KiCad project


## Usage

```
python kirename.py [-s <source>] [-d <dest>] [-n <name> | -t <tag> ]

-s               source directory (./)
-d               destination directory (./)
-n               new name
-t               tag to add
-x               dry run, do not change any files
-h | --help      show quick help | more help
```

## Examples

| Usage | Command |
|-------|---------|
| Rename project in current directory to `foo` | `python kirename.py -n foo` |
| Rename project in directory `foo` to `bar` | `python kirename.py -s ./foo -n bar`
| Append `_v1` to project in current directory | `python kirename.py -t _v1` |
