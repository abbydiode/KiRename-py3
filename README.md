# KiRename

Renames the specified KiCad 6 project. Project path defaults to current directory if not specified.

![image](https://user-images.githubusercontent.com/16174954/205734988-b35b41c1-09e5-4a90-93c4-4618441ac744.png)

## Installation

**Note:** You need to have Python3 and git installed for this to work. If you download the python file directly, git is not necessary.

1. Clone the repository by running `git clone https://github.com/abbydiode/KiRename-py3.git`
2. Move into the cloned directory with `cd KiRename-py3`
3. Run `python kirename` to view the command usage

```output
Usage: python kirename.py -p <project path> -n <new name>

Description: Renames the specified KiCad 6 project. Project path defaults to current directory if not specified.

Options:
-p Path to the project you wish to rename
-n Desired new project name, use quotation marks for names containing spaces
-x Dry run, outputs which files would be renamed without this option enabled
```

## Usage

| Example                                      | Command                              |
|:---------------------------------------------|:-------------------------------------|
| Rename project in current directory to `foo` | `python kirename.py -n foo`          |
| Rename project in directory `foo` to `bar`   | `python kirename.py -p ./foo -n bar` |
