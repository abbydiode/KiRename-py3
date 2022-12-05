import os
import sys
from pathlib import Path
from getopt import getopt, GetoptError

version = "0.3.0"

help = (f"KiRename {version}\n"
        "\n"
        "Usage: python kirename.py -p <project path> -n <new name>\n"
        "\n"
        "Description: Renames the specified KiCad 6 project. Project path defaults to current directory if not specified.\n"
        "\n"
        "Options:\n"
        "-p Path to the project you wish to rename\n"
        "-n Desired new project name, use quotation marks for names containing spaces\n"
        "-x Dry run, outputs which files would be renamed without this option active (optional)")

file_extensions = [
    ".kicad_pro",
    ".kicad_pcb",
    ".kicad_sch",
    ".kicad_sym",
    ".kicad_mod",
    ".kicad_wks",
    ".kicad_prl",
    ".zip"
]

def main(argv):
    project_path = ""
    project_name = ""
    new_name = ""
    dry_run = False

    # Try getting options, return error message if invalid
    try:
        opts, _ = getopt(argv, "p:n:x")
    except GetoptError as error:
        sys.exit(error.msg.capitalize())

    # If there were no options specified, return help text
    if len(opts) == 0:
        sys.exit(help)

    for opt, arg in opts:
        if opt in ("-p"):
            project_path = arg
        elif opt in ("-n"):
            new_name = arg
        elif opt in ("-x"):
            dry_run = True

    project_path = os.getcwd() if project_path == "" else project_path

    if new_name == "": sys.exit(f"No project name specified")

    if not os.path.exists(project_path): sys.exit(f"{project_path}: No such directory")

    files = []
    directories = []
    for root, project_directories, project_files in os.walk(project_path):
        for file in project_files:
            files.append(os.path.join(root, file))
        for directory in project_directories:
            directories.append(os.path.join(root, directory))

    # Check if project contains a .kicad_pro file and get project name
    for file in files:
        if file.endswith(".kicad_pro"):
            if project_name == "":
                project_name = Path(file).stem
                print(f"Found project file {project_name}.kicad_pro in {project_path}\n")
            else:
                sys.exit(f"Multiple projects found in {project_path}")
    if project_name == "": sys.exit(f"No project file found in {project_path}")

    # Rename all files
    for file in files:
        file_dir, file_ext = os.path.splitext(file)
        if file_ext in file_extensions:
            file_dir, file_name = os.path.split(file_dir)
            # print(f"{file_dir} + {file_name} + {file_ext}")
            new_file = file_name.replace(project_name, new_name) + file_ext

            if not dry_run:
                try:
                    os.rename(file, os.path.join(file_dir, new_file))
                except IOError as error:
                    sys.exit(f"Could not rename file {error.filename} ({error.errno})")
            print(f"Renamed file {file_name}{file_ext} to {new_file}")

    # Rename all directories
    for directory in directories:
        directory_path, directory_name = os.path.split(file_dir)
        new_directory = directory_name.replace(project_name, new_name)

        if not dry_run:
            try:
                os.rename(directory, os.path.join(directory_path, new_directory))
            except IOError as error:
                sys.exit(f"Could not rename directory {error.filename} ({error.errno})")
        print(f"Renamed directory {directory_name} to {new_directory}")

    # Rename project directory
    new_project_path = os.path.join(os.path.dirname(project_path), new_name)
    if not dry_run:
        try:
            os.rename(project_path, new_project_path)
        except IOError as error:
            sys.exit(f"Could not rename directory {error.filename} ({error.errno})")
    print(f"\nSuccessfully renamed project {project_name} to {new_name}, new path is {new_project_path}")

main(sys.argv[1:])
