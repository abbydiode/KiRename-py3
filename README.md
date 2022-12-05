# KiRename

Rename a KiCad project


## Usage

```
rename_project.py [-s <source>] [-d <dest>] [-n <name> | -t <tag> ]

-s               source directory (./)
-d               destination directory (./)
-n               new name
-t               tag to add
-x               dry run, do not change any files
-h | --help      show quick help | more help
```

## Typical uses

1. Rename a project foo.kicad_pro to bar.kicad_pro

> $ python rename_project.py -n new_name

2. Rename a project foo.kicad_pro to foo_v1.kicad_pro

> $ python rename_project.py -t _v1

3. Rename a project foo.kicad_pro to /temp/bar.kicad_pro

> $ python rename_project.py -d /temp -n bar

4. Rename a project foo.kicad_pro to /temp/foo_v1.kicad_pro

> $ python rename_project.py -d /temp -t _v1

5. Rename a project foo.kicad_pro to ./YYYY-MM-DD_HH-MM-SS/foo.kicad_pro

> $ python rename_project.py

6. Rename a project foo.kicad_pro to ./save1/foo.kicad_pro

> $ python rename_project.py -d save1
