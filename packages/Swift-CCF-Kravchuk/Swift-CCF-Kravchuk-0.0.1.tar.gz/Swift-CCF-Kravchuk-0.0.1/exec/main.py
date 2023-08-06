import argparse
from pathlib import Path

from analyzers import *

# folder to store results
results_folder = Path("results/")

# specify file extention of interest
extention = "swift"

# create  and configure argparse
arg_parser = argparse.ArgumentParser(description="Swift CCF")

group1 = arg_parser.add_mutually_exclusive_group(required=True)
group1.add_argument("-d", action="store", dest="directory",
                    help="directory to parse")
group1.add_argument("-f", action="store", dest="file", help="file to parse")
group1.add_argument("-p", action="store", dest="project",
                    help="project directory to parse (recursive)")

arg_parser.add_argument("-v", "--verify", action="store_true",
                        dest="verify", help="output unfixable errors and warnings")
arg_parser.add_argument("-fx", "--fix", action="store_true", dest="fix",
                        help="output fixed errors")

args = arg_parser.parse_args()


def scan_and_fix_file(filepath, outname):
    """Apply usual fixers"""
    data = ""
    verify = None
    fixing = None

    with open(filepath, "r") as infile:
        data = infile.read()

        results_folder.mkdir(exist_ok=True)

        if args.verify:
            verify = open(results_folder /
                          (outname + "_verification.log"), "a+")

        if args.fix:
            fixing = open(results_folder / (outname + "_fixing.log"), "a+")

        # exit without doing anything if both none
        if verify == None and fixing == None:
            return

        for fixer in source_fixers:
            fixer(verify, fixing, filepath, data, filepath.stem)

        for fixer in naming_fixers:
            changed_data = fixer(verify, fixing, filepath, data)
            if changed_data != None:
                data = changed_data

        for fixer in docs_fixers:
            changed_data = fixer(verify, fixing, filepath, data)
            if changed_data != None:
                data = changed_data

        if verify != None:
            verify.close()

        if fixing != None:
            fixing.close()

    if fixing != None:
        with open(filepath, "w") as outfile:
            outfile.write(data)


def final_fix(filepath):
    """Apply global changes"""
    data = ""

    with open(filepath, "r") as infile:
        data = infile.read()

        data = apply_global(data)

    if args.fix:
        with open(filepath, "w") as outfile:
            outfile.write(data)


if args.file:
    file = Path(args.file)

    outname = file.stem

    if not file.exists():
        raise FileNotFoundError("File not found")

    scan_and_fix_file(file, outname)

    final_fix(file)

if args.directory:
    directory = Path(args.directory)

    outname = directory.stem

    if not directory.exists():
        raise FileNotFoundError("Directory not found")

    for filepath in directory.glob("*." + extention):
        scan_and_fix_file(filepath, outname)

    for filepath in directory.glob("*." + extention):
        final_fix(filepath)

if args.project:
    project = Path(args.project)

    outname = project.stem

    if not project.exists():
        raise FileNotFoundError("Project directory not found")

    for filepath in project.glob("**/*." + extention):
        scan_and_fix_file(filepath, outname)

    for filepath in project.glob("**/*." + extention):
        final_fix(filepath)
