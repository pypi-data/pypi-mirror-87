import argparse

from ccfcsharp.code_convention_fixer import CodeConventionFixer

def main():

    parser = argparse.ArgumentParser('_dir')
    parser.add_argument('-v', '--verify', action='store_true', help='Verify naming conventions')
    parser.add_argument('-fx', '--fix', action='store_true', help='Fix naming accordingly to conventions')
    parser.add_argument('-f', '--file', nargs=1, required=False, help='*.cs file')
    parser.add_argument('-p', '--project', nargs=1, required=False, help='CSharp project directory with *.cs files')
    parser.add_argument('-d', '--directory', nargs=1, required=False, help='Directory with *.cs files')

    my_namespace = parser.parse_args()
    if not (my_namespace.verify or my_namespace.fix) or \
            not (my_namespace.directory is not None or
                 my_namespace.file is not None or
                 my_namespace.project is not None):
        print("Incorrect input. See help:")
        parser.print_help()
        return

    if my_namespace.fix:
        if my_namespace.project is not None:
            CodeConventionFixer.fix_project_conventions(my_namespace.project[0])
        elif my_namespace.directory is not None:
            CodeConventionFixer.fix_directory_conventions(my_namespace.directory[0])
        else:
            CodeConventionFixer.fix_file_conventions(my_namespace.file[0])
    else:
        if my_namespace.project is not None:
            CodeConventionFixer.verify_project_conventions(my_namespace.project[0])
        elif my_namespace.directory is not None:
            CodeConventionFixer.verify_directory_conventions(my_namespace.directory[0])
        else:
            CodeConventionFixer.verify_file_conventions(my_namespace.file[0])

main()