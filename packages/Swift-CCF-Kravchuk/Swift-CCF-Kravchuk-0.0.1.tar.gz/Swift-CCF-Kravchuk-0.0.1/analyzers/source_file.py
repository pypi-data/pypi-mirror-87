from util.util import *
import re


def check_filename(verif_file, fix_file, filepath, file_data, filename):
    """Check types in a file, if there's one
    check filename for convention compliance,
    also check for extensions"""
    types = []
    extensions = []
    i = 0

    while i < len(file_data) - 1:
        # check for class keyword
        if check_word_with_space(file_data[i:], "class") and not check_word_with_space(file_data[i:], "class var"):
            types.append(read_next_word(file_data[i+6:]))

        # check struct keyword
        if check_word_with_space(file_data[i:], "struct"):
            types.append(read_next_word(file_data[i+6:]))

        # check type extension
        if check_word_with_space(file_data[i:], "extension"):
            # get type being extended
            offset = len("extension ")
            i += offset
            decl_type = read_next_word(file_data[i:])
            i = len(decl_type) + file_data.index(decl_type, i)

            types.append(decl_type)

            # get first extension
            extension1 = read_next_word(file_data[i:])
            i = len(extension1) + file_data.index(extension1, i)
            extensions.append(extension1)

            # perform check for second extension (by searching for comma)
            second_extension = False

            for j in range(i, len(file_data)):
                if file_data[j] == " ":
                    continue

                elif file_data[j] == ",":
                    second_extension = True

                break

            # get second extension if it exists, no need to check for more
            if second_extension:
                extension2 = read_next_word(file_data[i:])
                i = len(extension2) + file_data.index(extension2, i)
                extensions.append(extension2)

        i += 1

    if len(types) == 1:
        if len(extensions) == 0:
            if filename != types[0]:
                file_write(verif_file,
                           f"{filepath} Error: file name with one type must match type it's declaring")

        elif len(extensions) == 1:
            if filename != types[0] + "+" + extensions[0]:
                file_write(verif_file,
                           f"{filepath} Error: file name with one type single extension must match TypeName+Protocol")

        else:
            if not filename.startswith(types[0] + "+"):
                file_write(verif_file,
                           f"{filepath} Error: file name with one type multiple extensions must match TypeName+Stuff")


def various_char_checks(verif_file, fix_file, filepath, file_data, filename):
    """Checks source file for not allowed spaces

    Checks for unicode escaped characters that
    can be written as special escape sequence"""

    for i in range(0, len(file_data)):
        if (re.match(r"\s", file_data[i]) and file_data[i] != " "
                and file_data[i] != "\n" and file_data[i:i+2] != "\r\n"):

            file_write(verif_file,
                       f"{filepath} Error: source file contains illegal whitespace characters")

        if (file_data[i:i+5] in [r"\u{0}", r"\u{9}", r"\u{A}", r"\u{D}"]
                or file_data[i:i+6] in [r"\u{22}", r"\u{27}", r"\u{5C}"]):

            file_write(verif_file,
                       f"{filepath} Error: source file contains unicode escaped chars that can be represented as special escaped char")


source_fixers = [
    check_filename,
    various_char_checks
]
