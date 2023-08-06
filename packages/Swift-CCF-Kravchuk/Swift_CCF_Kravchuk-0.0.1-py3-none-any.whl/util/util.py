def file_write(file, data):
    if file != None:
        file.write(data + "\n")


SEPARATORS = [" ", "\n", "\r", "{", "}", "=", ">",
              "<", ":", "?", ",", "\"", "\'", "(", ")"]


def next_separator_without_spaces_index(data):
    """Get index of next separator
    that is not a space"""

    tmp_seps = SEPARATORS[:]
    tmp_seps.remove(" ")
    tmp_seps.remove("\n")
    tmp_seps.remove("\r")

    for i in range(0, len(data)):
        if data[i] in tmp_seps:
            return i

        elif data[i] in [" ", "\n", "\r"]:
            continue

        break

    return None  # EOF or non-separator


def get_next_separator_without_spaces(data):
    """Get next separator that is not a space"""

    index = next_separator_without_spaces_index(data)

    if index == None:
        return None

    return data[index]


def get_next_word_indices(data):
    """Get indices between separators,
    skipping separators at start"""

    start = None

    for i in range(0, len(data)):
        if start == None and data[i] not in SEPARATORS:
            start = i

        if start != None and data[i] in SEPARATORS:
            return start, i

    return (None, None)  # file read until EOF


def read_next_word(data):
    """Read the word, disregard indices"""
    start, end = get_next_word_indices(data)

    if start == None:
        return None

    return data[start:end]


def check_word_with_space(data, word):
    """Checks for a type"""

    word_len = len(word)

    if len(data) < word_len + 1:
        return False

    if data.startswith(word + " "):
        return True

    return False


def get_symbols_in_parentheses(data):
    """Get parameter names in parentheses"""

    i = 0
    res = {}

    while get_next_separator_without_spaces(data[i:]) != ")":
        word1 = read_next_word(data[i:])
        i += len(word1) + data[i:].index(word1)

        word2 = None

        if get_next_separator_without_spaces(data[i]) == None:
            word2 = read_next_word(data[i:])
            i += len(word2) + data[i:].index(word2)

        # res[outerName] = innerName
        if word2 != None:
            res[word1] = word2
        else:
            res[word1] = word1

        # disregard parameter type
        tmp = read_next_word(data[i:])
        i += len(tmp) + data[i:].index(tmp)

    return res, i


def is_next_newline(data):
    """While skipping spaces, checks for \n as next char"""
    for i in range(len(data)):
        if data[i] == "\n":
            return True

        elif data[i] in [" ", "\r"]:
            continue

        return False


def get_vars_directly_assigned(data, symbols):
    """Looking for expression "a = b" in init"""

    res = {}
    newline = False
    i = 0
    nesting = 0

    while i < len(data):
        if data[i] == "\n":
            newline = True
            i += 1
            continue

        if data[i] == "{":
            nesting += 1

        if data[i] == "}":
            nesting -= 1

            if nesting == 0:
                break

        if newline == True:
            word1 = read_next_word(data[i:])

            if word1 == None:
                break

            i += len(word1) + data[i:].index(word1)

            if get_next_separator_without_spaces(data[i:]) == "=":
                word2 = read_next_word(data[i:])
                i += len(word2) + data[i:].index(word2)

                if is_next_newline(data[i:]) and word2 in symbols.values() and not word1.startswith("self."):
                    res[word1] = word2  # word1 = word2

            newline = False

        else:
            i += 1

    return res


def apply_init_changes(file_data, symbols_in_parentheses, vars_directly_assigned, filepath):
    """Change "a = b" in init to "self.a = a" """
    i = 0
    start = None
    changes = []

    while i < len(file_data):
        word = read_next_word(file_data[i:])

        if word == None:
            break

        i += len(word) + file_data[i:].index(word)

        if word == "init":
            start = i

    if start == None:
        return None

    unprocessed = file_data[start:]

    new_file_data = file_data[:start]

    # modify parameters to match type fields
    for key in symbols_in_parentheses.keys():
        if symbols_in_parentheses[key] in vars_directly_assigned.values():
            start_change = unprocessed.index(key)
            new_file_data += unprocessed[:start_change]
            unprocessed = unprocessed[start_change:]

            word1 = read_next_word(unprocessed)
            offset = len(word1) + unprocessed.index(word1)
            unprocessed = unprocessed[offset:]

            word2 = read_next_word(unprocessed)
            offset = len(word2) + unprocessed.index(word2)
            unprocessed = unprocessed[offset:]

            for k, v in vars_directly_assigned.items():
                if symbols_in_parentheses[key] == v:
                    new_file_data += k
                    break

    init_start = unprocessed.index("{")
    new_file_data += unprocessed[:init_start]
    unprocessed = unprocessed[init_start:]

    for key in vars_directly_assigned.keys():
        start_change = unprocessed.index(key)

        new_file_data += unprocessed[:start_change]
        unprocessed = unprocessed[start_change:]

        word1 = read_next_word(unprocessed)
        offset = len(word1) + unprocessed.index(word1)
        unprocessed = unprocessed[offset:]

        word2 = read_next_word(unprocessed)
        offset = len(word2) + unprocessed.index(word2)
        unprocessed = unprocessed[offset:]

        new_file_data += f"self.{key} = {key}"

        changes.append(
            f"{filepath} Changed: parameter in init was changed to class field {key}")

    new_file_data += unprocessed

    return new_file_data, changes


def apply_static_class_prop_changes(data, all_changes, filepath):
    """Apply removing suffix from static and class properties"""
    nesting = 0
    new_file_data = ""
    changes = []
    prop_changes = None

    while len(data) > 0:
        for class_change in all_changes.keys():
            if data.startswith("class " + class_change):
                prop_changes = all_changes[class_change]

        if prop_changes != None:
            if data[0] == "{":
                nesting += 1

            if data[0] == "}":
                nesting -= 1

                if nesting == 0:
                    prop_changes = None
                    continue

            for change_prop in prop_changes.keys():
                if data.startswith(change_prop):
                    new_file_data += prop_changes[change_prop]
                    data = data[len(change_prop):]
                    changes.append(
                        f"{filepath} Changed: class/static property {change_prop} (doesn't need return suffix)")
                    break

        new_file_data += data[:1]
        data = data[1:]

    return new_file_data, changes


def read_until_newline(data):
    """Read data until newline is found"""
    res = ""
    if data[0] == "\n":
        data = data[1:]

    while len(data) > 0:
        if data[0] != "\n":
            res += data[:1]
            data = data[1:]

        else:
            return res


def remove_star_in_line(line):
    """Return (docstring) line without javadoc style *"""
    for i in range(0, len(line)):
        if line[i] == " ":
            continue

        elif line[i:i+2] == "*/":
            return None

        elif line[i:i+2] == "* ":
            return line[i+2:]

        elif line[i] == "*":
            return line[i+1:]

        else:
            return line

    return ""


def process_doc_block(data):
    """Gather info about current doc block"""
    i = 0
    comment_lines = []
    flag = 1
    flags = {"Parameter": 0, "Parameters": 0,
             "Returns": 0, "Throws": 0}

    count = {"Parameter": 0, "Parameters": 0,
             "Returns": 0, "Throws": 0, "Params amount": 0}

    while i < len(data):
        line = read_until_newline(data[i:])

        if not line.lstrip().startswith("///"):
            return comment_lines, flags, count, i-1

        comment_lines.append(line)
        i += len(line) + 1  # +1 accounts for skipped \n

        try:
            line.index("- Parameters")
            flags["Parameters"] = flag
            count["Parameters"] += 1
            flag += 1
        except ValueError:

            try:
                line.index("- Parameter")
                flags["Parameter"] = flag
                count["Parameter"] += 1
                flag += 1
            except ValueError:
                pass

        try:
            line.index("- Returns")
            flags["Returns"] = flag
            count["Returns"] += 1
            flag += 1
        except ValueError:
            pass

        try:
            line.index("- Throws")
            flags["Throws"] = flag
            count["Throws"] += 1
            flag += 1
        except ValueError:
            pass

        try:
            line.index("///   - ")
            count["Params amount"] += 1
        except ValueError:
            pass


def check_tags_order(flags):
    """Check if tags go in allowed order"""
    if flags["Parameter"] == 1 and flags["Parameter"] < flags["Returns"] < flags["Throws"] and flags["Parameters"] == 0:
        return True

    if flags["Parameters"] == 1 and flags["Parameters"] < flags["Returns"] < flags["Throws"] and flags["Parameter"] == 0:
        return True

    if flags["Parameter"] == 1 and flags["Parameter"] < flags["Returns"] and flags["Throws"] == 0 and flags["Parameters"] == 0:
        return True

    if flags["Parameters"] == 1 and flags["Parameters"] < flags["Returns"] and flags["Throws"] == 0 and flags["Parameter"] == 0:
        return True

    if flags["Parameter"] == 1 and flags["Parameter"] < flags["Throws"] and flags["Returns"] == 0 and flags["Parameters"] == 0:
        return True

    if flags["Parameters"] == 1 and flags["Parameters"] < flags["Throws"] and flags["Returns"] == 0 and flags["Parameter"] == 0:
        return True

    if flags["Parameter"] == 1 and flags["Returns"] == 0 and flags["Throws"] == 0 and flags["Parameters"] == 0:
        return True

    if flags["Parameters"] == 1 and flags["Returns"] == 0 and flags["Throws"] == 0 and flags["Parameter"] == 0:
        return True

    return False


def redo_comment_block(comment_lines, count, filename):
    """Modify comment block, so that if follows code conventions"""
    new_comment_lines = []
    last_non_tag = 0
    warnings = []
    changes = []

    for line in comment_lines:
        if not line[3:].lstrip().startswith("- "):
            new_comment_lines.append(line)
            last_non_tag += 1
            continue

        break

    tags_start = last_non_tag

    if count["Parameter"] == 1:
        for i in range(tags_start, len(comment_lines)):
            try:
                comment_lines[i].index("- Parameter")
                new_comment_lines.append(comment_lines[i])

                # check next ones continuing current
                for j in range(i+1, len(comment_lines)):
                    if not comment_lines[j].startswith("/// - ") and not comment_lines[j].startswith("///   - "):
                        new_comment_lines.append(comment_lines[j])

                    else:
                        break

                break
            except ValueError:
                pass

    elif count["Parameter"] > 1:
        warnings.append(
            f"{filename} Error: When there are more than 2 parameters use \"Parameters\" instead of \"Parameter\"")

        changes.append(
            f"{filename} Changed: multiple \"Parameter\" changed to \"Parameters\"")

        new_comment_lines.append("/// - Parameters:")

        for i in range(tags_start, len(comment_lines)):
            try:
                param_index = comment_lines[i].index("- Parameter")
                new_comment_lines.append(
                    "///   -" + comment_lines[i][param_index + 11:])

                # check next ones continuing current
                for j in range(i+1, len(comment_lines)):
                    if not comment_lines[j].startswith("/// - ") and not comment_lines[j].startswith("///   - "):
                        new_comment_lines.append(comment_lines[j])

                    else:
                        break

            except ValueError:
                pass

    if count["Parameters"] == 1:
        if count["Params amount"] == 1:
            warnings.append(
                f"{filename} Error: When there is 1 parameter use \"Parameter\" instead of \"Parameters\"")

            changes.append(
                f"{filename} Changed: single parameter in \"Parameters\" changed to \"Parameter\"")

            for i in range(tags_start, len(comment_lines)):
                try:
                    param_index = comment_lines[i].index("///   - ")
                    new_comment_lines.append(
                        "/// - Parameter " + comment_lines[i][param_index + 8:])

                    # check next ones continuing current
                    for j in range(i+1, len(comment_lines)):
                        if not comment_lines[j].startswith("/// - ") and not comment_lines[j].startswith("///   - "):
                            new_comment_lines.append(comment_lines[j])

                        else:
                            break

                    break
                except ValueError:
                    pass

        else:
            new_comment_lines.append("/// - Parameters:")

            for i in range(tags_start, len(comment_lines)):
                try:
                    param_index = comment_lines[i].index("///   - ")
                    new_comment_lines.append(comment_lines[i])

                    # check next ones continuing current
                    for j in range(i+1, len(comment_lines)):
                        if not comment_lines[j].startswith("/// - ") and not comment_lines[j].startswith("///   - "):
                            new_comment_lines.append(comment_lines[j])

                        else:
                            break

                except ValueError:
                    pass

    if count["Returns"] == 1:
        for i in range(tags_start, len(comment_lines)):
            try:
                param_index = comment_lines[i].index("- Returns")
                new_comment_lines.append(comment_lines[i])

                # check next ones continuing current
                for j in range(i+1, len(comment_lines)):
                    if not comment_lines[j].startswith("/// - ") and not comment_lines[j].startswith("///   - "):
                        new_comment_lines.append(comment_lines[j])

                    else:
                        break

                break

            except ValueError:
                pass

    if count["Throws"] == 1:
        for i in range(tags_start, len(comment_lines)):
            try:
                param_index = comment_lines[i].index("- Throws")
                new_comment_lines.append(comment_lines[i])

                # check next ones continuing current
                for j in range(i+1, len(comment_lines)):
                    if not comment_lines[j].startswith("/// - ") and not comment_lines[j].startswith("///   - "):
                        new_comment_lines.append(comment_lines[j])

                    else:
                        break

                break

            except ValueError:
                pass

    return new_comment_lines, changes, warnings
