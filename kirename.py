import getopt
import errno
import shutil
import sys
import os
from time import strftime
version = "0.2.0"


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


def help():
    print("KiRename Version %s\n" % version)
    print('python kirename.py [-s <source>] [-d <dest>] [-n <name> | -t <tag> ]\n')
    print('Rename a KiCad project\n')
    print('-s               Source directory (default: ./)')
    print('-d               Destination directory (default: ./)')
    print('-n               New project name')
    print('-t               Text to append')
    print('-x               Dry run, do not change any files')
    print('-h (--help)      You\'re here')


def main(argv):

    mode = "none"
    new_name = ""
    sourcedir = ""
    suffix = ""
    destdir = ""
    recurse = False
    dry_run = False

    try:
        opts, arg = getopt.getopt(argv, "s:d:n:t:hxv", ["help"])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit()
        elif opt in ("-s"):
            sourcedir = arg
        elif opt in ("-d"):
            destdir = arg
        elif opt in ("-t"):
            suffix = arg
        elif opt in ("-n"):
            new_name = arg
        elif opt in ("-x"):
            dry_run = True

    if sourcedir == "":
        sourcedir = os.getcwd()

    if not os.path.exists(sourcedir):
        print("Error: Invalid directory %s" % sourcedir)
        quit()

    top_level_files = [f for f in os.listdir(
        sourcedir) if os.path.isfile(os.path.join(sourcedir, f))]

    files = []
    if recurse:
        for root, dirnames, filenames in os.walk(sourcedir):
            for filename in filenames:
                files.append(os.path.join(after(root, sourcedir), filename))
    else:
        files = [f for f in os.listdir(sourcedir) if os.path.isfile(
            os.path.join(sourcedir, f))]

    project = ""
    for file in top_level_files:
        if file.endswith(".kicad_pro"):

            if project == "":
                project = before(file, ".kicad_pro")
            else:
                print("Error: Multiple projects found in %s" % sourcedir)
                quit(1)

    if project == "":
        print("Error: No project file found in %s" % sourcedir)
        quit(2)

    if destdir == "":
        if (suffix == "" and new_name == ""):
            mode = "copy"
            destdir = sourcedir
            new_name = project
        elif (suffix != "" and new_name != ""):
            print("Error: Must specify only one of name or tag")
            quit()
        elif suffix != "":
            mode = "rename"
            destdir = sourcedir
            new_name = project + suffix
        elif new_name != "":
            mode = "rename"
            destdir = sourcedir
    else:
        if (suffix == "" and new_name == ""):
            mode = "copy"
            destdir = os.path.join(sourcedir, destdir)
            new_name = project
        elif (suffix != "" and new_name != ""):
            print("Error: Must specify only one of name or tag")
            quit()
        elif suffix != "":
            mode = "copy"
            # destdir = destdir
            new_name = project + suffix
        elif new_name != "":
            mode = "copy"

    print("project name: %s" % project)
    print("new project name: %s" % new_name)
    print("")

    if dry_run:
        print("mode      : %s" % mode)
        print("sourcedir : %s" % sourcedir)
        print("destdir   : %s" % destdir)
        print("")

    if dry_run:
        if not os.path.exists(destdir):
            print("create : %s" % destdir)
    else:
        try:
            make_sure_path_exists(destdir)
        except:
            print("Error creating dest folder %s" % destdir)
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
                    # copy with rename

                    source_file = os.path.join(sourcedir, file)
                    dest_file = os.path.join(
                        destdir, new_name + after(file, project))

                    if dry_run:
                        print("rename : %s ==> %s" % (file, dest_file))
                    else:
                        if mode == "copy":
                            shutil.copy2(source_file, dest_file)
                        else:
                            os.rename(source_file, dest_file)
                else:
                    if mode == "copy":
                        source_file = os.path.join(sourcedir, file)
                        dest_file = os.path.join(destdir, file)
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
