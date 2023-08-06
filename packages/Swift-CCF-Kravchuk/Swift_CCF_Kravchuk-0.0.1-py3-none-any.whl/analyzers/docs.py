from util.util import *


def javadoc_to_slashes(verif_file, fix_file, filepath, file_data):
    """Transforms javadoc-style comment to three slash block"""
    i = 0
    in_javadoc = False
    new_data = ""
    changed = False

    while i < len(file_data):
        if file_data[i:i+3] == "/**":
            in_javadoc = True
            changed = True
            i += 4

        if in_javadoc:
            line = read_until_newline(file_data[i:]) + "\n"
            i += len(line)
            line = remove_star_in_line(line)

            if line == None:
                in_javadoc = False
                continue

            new_data += "/// " + line

        else:
            new_data += file_data[i]
            i += 1

    if changed:
        file_write(verif_file,
                   f"{filepath} Warning: Javadoc-style block comments not allowed")
        file_write(fix_file,
                   f"{filepath} Changed: Javadoc-style block comments transformed into ///")

    return new_data


def comment_tags(verif_file, fix_file, filepath, file_data):
    """Check and modify comment tags, so
    that they follow code convetions"""
    i = 0
    new_file_data = ""
    warnings = []
    changes = []

    while i < len(file_data):
        if file_data[i:i+3] == "///":
            comment_lines, flags, count, offset = process_doc_block(
                file_data[i:])
            i += offset

            if not check_tags_order(flags):
                file_write(verif_file,
                           f"{filepath} Error: tags in doc block are in the wrong order")

            new_block_lines, changes, warnings = redo_comment_block(
                comment_lines, count, filepath)

            new_block = "\n".join(new_block_lines)
            new_file_data += new_block

        new_file_data += file_data[i]
        i += 1

    for warning in warnings:
        file_write(verif_file, warning)

    for change in changes:
        file_write(fix_file, change)

    return new_file_data


docs_fixers = [
    javadoc_to_slashes,
    comment_tags
]
