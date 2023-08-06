import argparse
import logging

from jsconventionfixer.naming_fixer import NamingFixer

def main():

    logger = logging.getLogger()
    fhandler = logging.FileHandler(filename='all.log', mode='w')
    formatter = logging.Formatter('%(levelname)s: %(message)s')
    fhandler.setFormatter(formatter)
    logger.addHandler(fhandler)
    logger.setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser('JavaScriptCCF')
    parser.add_argument('-v', '--verify', action='store_true', help='verify naming conventions')
    parser.add_argument('-fx', '--fix', action='store_true', help='fix naming conventions')
    parser.add_argument('-f', '--file', nargs=1, required=False, help='javascript source code file')
    parser.add_argument('-p', '--project', nargs=1, required=False, help='javascript project directory javascript source code files')
    parser.add_argument('-d', '--directory', nargs=1, required=False, help='directory javascript source code files')

    my_namespace = parser.parse_args()
    if not (my_namespace.verify or my_namespace.fix) or \
            not (my_namespace.directory is not None or
                 my_namespace.file is not None or
                 my_namespace.project is not None):
        print("Incorrect input. Help:")
        parser.print_help()
        return

    if my_namespace.fix:
        if my_namespace.project is not None:
            NamingFixer.fix_project(my_namespace.project[0])
        elif my_namespace.directory is not None:
            NamingFixer.fix_directory(my_namespace.directory[0])
        else:
            NamingFixer.fix_file(my_namespace.file[0])
    else:
        if my_namespace.project is not None:
            NamingFixer.verify_project(my_namespace.project[0])
        elif my_namespace.directory is not None:
            NamingFixer.verify_directory(my_namespace.directory[0])
        else:
            NamingFixer.verify_file(my_namespace.file[0])

main()