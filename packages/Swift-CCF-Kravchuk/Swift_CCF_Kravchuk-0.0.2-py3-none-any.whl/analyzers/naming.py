from util.util import *
import string

global_changes = {}


def apply_global(file_data):
    """Applies changes implemented in
    static and class property globally"""
    i = 0
    # watch_list[type] = relative nesting scope
    watch_list = {}
    new_file_data = ""
    last_carry_index = 0

    while i < len(file_data) - 1:
        word = file_data[i:i+3]

        if word in ["var", "let"]:
            i += 3

            variable = read_next_word(file_data[i:])
            i += len(variable) + file_data[i:].index(variable)

            var_type = read_next_word(file_data[i:])
            i += len(var_type) + file_data[i:].index(var_type)

            for key in global_changes.keys():
                if key == var_type:
                    watch_list[variable] = {
                        "nestedness": 0, "parent class": var_type}

        to_pop = []

        for variable in watch_list.keys():
            if file_data[i] == "{":
                watch_list[variable]["nestedness"] += 1

            if file_data[i] == "}":
                watch_list[variable]["nestedness"] -= 1

            if watch_list[variable]["nestedness"] < 0:
                to_pop.append(variable)

        for p in to_pop:
            watch_list.pop(p)

        possible_change = read_next_word(file_data[i:])

        if possible_change != None:
            for variable in watch_list.keys():
                if possible_change.startswith(variable):
                    class_change = global_changes[watch_list[variable]
                                                  ["parent class"]]

                    for change_from in class_change.keys():
                        if possible_change.startswith(variable + "." + change_from):
                            i = file_data.index(possible_change, i)
                            new_file_data += file_data[last_carry_index:i]
                            new_file_data += variable + "." + \
                                class_change[change_from]
                            last_carry_index = i + \
                                len(variable + "." + change_from)

        i += 1

    new_file_data += file_data[last_carry_index:]

    return new_file_data


def check_initializers(verif_file, fix_file, filepath, file_data):
    """Changes expressions of type "a=b"
    to "self.a = a" in init"""
    i = 0

    while i < len(file_data) - 1:
        word = read_next_word(file_data[i:])
        if word == None:
            return None

        i += len(word) + file_data[i:].index(word)

        if word == "init":
            symbols_in_parentheses, offset = get_symbols_in_parentheses(
                file_data[i:])
            i += offset

            vars_directly_assigned = get_vars_directly_assigned(
                file_data, symbols_in_parentheses)
            new_data, changes = apply_init_changes(
                file_data, symbols_in_parentheses, vars_directly_assigned, filepath)

            if len(changes) > 0:
                file_write(verif_file,
                           f"{filepath} Warning: init parameters direct assignment should have same name as field")

                for change in changes:
                    file_write(fix_file, change)

            return new_data


def check_properties(verif_file, fix_file, filepath, file_data):
    """Removes return suffix from class and static properties"""
    global global_changes

    i = 0
    inside_class = None
    all_changes = {}
    prop_changes = {}

    nesting = None

    while i < len(file_data):
        if check_word_with_space(file_data[i:], "class") and not check_word_with_space(file_data[i:], "class var"):
            inside_class = read_next_word(file_data[i+6:])
            prop_changes = {}
            nesting = 0

        if inside_class:
            prop = None
            prop_type = None

            if check_word_with_space(file_data[i:], "static var"):
                prop = read_next_word(file_data[i+11:])

                prop_type = read_next_word(file_data[i+11+len(prop):])

            elif check_word_with_space(file_data[i:], "class var"):
                prop = read_next_word(file_data[i+10:])

                prop_type = read_next_word(file_data[i+10+len(prop):])

            if prop != None:
                cut = -1

                for j in range(1, len(prop)):
                    if not prop_type.endswith(prop[-j:]):
                        break

                    if prop[-j] in string.ascii_uppercase:
                        cut = len(prop) - j

                if cut != -1:
                    prop_changes[prop] = prop[:cut]

            if file_data[i] == "{":
                nesting += 1

            if file_data[i] == "}":
                nesting -= 1

                if nesting == 0:  # class ended
                    all_changes[inside_class] = prop_changes

                    inside_class = None

        i += 1

    new_data, changes = apply_static_class_prop_changes(
        file_data, all_changes, filepath)

    if len(changes) > 0:
        file_write(verif_file,
                   f"{filepath} Warning: static and class properties don't need return type suffix")

    for change in changes:
        file_write(fix_file, change)

    global_changes.update(all_changes)

    return new_data


naming_fixers = [
    check_initializers,
    check_properties
]
