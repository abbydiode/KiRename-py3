import os
import sys
import errno
import shutil
from getopt import getopt, GetoptError

version = "0.2.0"

help = (f"KiRename {version}\n"
    "\n"
    "Usage: python kirename.py [-s <source>] [-d <destination>] [-n <name>] [-a <append> ]\n"
    "\n"
    "-s Source Directory (default: ./)\n"
    "-d Desination directory (default: ./)\n"
    "-n Desired new project name\n"
    "-t Text to append\n"
    "-x Dry run, doesn't rename any files but outputs what would be changed")

def before(value, a):
    pos_a = value.find(a)
    if pos_a == -1:
        return ""
    return value[0:pos_a]

def after(value, a):
    pos_a = value.rfind(a)
    if pos_a == -1:
        return ""
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= len(value):
        return ""
    return value[adjusted_pos_a:]

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def main(args):
    mode = "none"
    new_name = ""
    source_dir = ""
    append_name = ""
    dest_dir = ""
    dry_run = False

    try:
        opts, arg = getopt(args, "s:d:n:a:x")
    except GetoptError as error:
        sys.exit(error.msg.capitalize())

    for opt, arg in opts:
        if opt in ("-s"):
            source_dir = os.getcwd() if arg == "" else arg
        elif opt in ("-d"):
            dest_dir = arg
        elif opt in ("-a"):
            append_name = arg
        elif opt in ("-n"):
            new_name = arg
        elif opt in ("-t"):
            dry_run = True

    if len(opts) == 0:
        sys.exit(help)

    if new_name == "" and append_name == "":
        sys.exit(f"No new project name or text to append specified")

    if not os.path.exists(source_dir):
        print(f"{source_dir}: No such directory")
        quit()

    top_level_files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f))]

    files = []
    for root, directories, filenames in os.walk(source_dir):
        for filename in filenames:
            files.append(os.path.join(after(root, source_dir), filename))

    project = ""
    for file in top_level_files:
        if file.endswith(".kicad_pro"):
            if project == "":
                project = before(file, ".kicad_pro")
            else:
                print(f"Error: Multiple projects found in {source_dir}")
                quit(1)

    if project == "":
        print(f"Error: No project file found in {source_dir}")
        quit(2)

    if dest_dir == "":
        if (append_name == "" and new_name == ""):
            mode = "copy"
            dest_dir = source_dir
            new_name = project
        elif (append_name != "" and new_name != ""):
            print("Error: Must specify only one of name or tag")
            quit()
        elif append_name != "":
            mode = "rename"
            dest_dir = source_dir
            new_name = project + append_name
        elif new_name != "":
            mode = "rename"
            dest_dir = source_dir
    else:
        if (append_name == "" and new_name == ""):
            mode = "copy"
            dest_dir = os.path.join(source_dir, dest_dir)
            new_name = project
        elif (append_name != "" and new_name != ""):
            print("Error: Must specify only one of name or tag")
            quit()
        elif append_name != "":
            mode = "copy"
            new_name = project + append_name
        elif new_name != "":
            mode = "copy"

    print("project name: %s" % project)
    print("new project name: %s" % new_name)
    print("")

    if dry_run:
        print("mode      : %s" % mode)
        print("sourcedir : %s" % source_dir)
        print("destdir   : %s" % dest_dir)
        print("")

    if dry_run:
        if not os.path.exists(dest_dir):
            print("create : %s" % dest_dir)
    else:
        try:
            make_sure_path_exists(dest_dir)
        except:
            print("Error creating dest folder %s" % dest_dir)
            quit()

    try:
        for file in files:
            if (file.endswith(".kicad_sch") or
                file.endswith(".kicad_lib") or
                file.endswith(".kicad_mod") or
                file.endswith(".kicad_cmp") or
                file.endswith(".kicad_brd") or
                file.endswith(".kicad_pcb") or
                file.endswith(".kicad_pos") or
                file.endswith(".kicad_net") or
                file.endswith(".kicad_pro") or
                file.endswith(".kicad_py") or
                file.endswith(".kicad_pdf") or
                file.endswith(".kicad_txt") or
                file.endswith(".kicad_dcm") or
                file.endswith(".kicad_wks") or
                file == "fp-lib-table"):

                if file.startswith(project):
                    source_file = os.path.join(source_dir, file)
                    dest_file = os.path.join(
                        dest_dir, new_name + after(file, project))

                    if dry_run:
                        print("rename : %s ==> %s" % (file, dest_file))
                    else:
                        if mode == "copy":
                            shutil.copy2(source_file, dest_file)
                        else:
                            os.rename(source_file, dest_file)
                else:
                    if mode == "copy":
                        source_file = os.path.join(source_dir, file)
                        dest_file = os.path.join(dest_dir, file)
                        if dry_run:
                            print("copy   : %s ==> %s" % (file, dest_file))
                        else:
                            shutil.copy2(source_file, dest_file)

    except IOError as exception:
        print("Error copying file %s : %s" %
              (exception.filename, exception.strerror))
        quit()


if __name__ == "__main__":
    main(sys.argv[1:])
