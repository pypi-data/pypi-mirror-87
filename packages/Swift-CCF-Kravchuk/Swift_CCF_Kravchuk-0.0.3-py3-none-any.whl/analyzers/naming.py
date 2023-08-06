from util.util import *
import string

global_changes = {}


def apply_global(file_data):
    """Applies changes implemented in
    static and class property
    and camel case changes globally"""
    i = 0
    # watch_list[type] = relative nesting scope, paretn class
    watch_list = {}
    new_file_data = ""
    last_carry_index = 0

    if global_changes.get(None):
        for variable in global_changes[None]:
            watch_list[variable] = {"nestedness": 0, "parent class": None}

    while i < len(file_data) - 1:
        word = file_data[i:i+3]

        if word in ["var", "let"]:
            i += 3

            tmp_i = i

            variable = read_next_word(file_data[tmp_i:])

            tmp_i += len(variable) + file_data[tmp_i:].index(variable)

            var_type = read_next_word(file_data[tmp_i:])

            for key in global_changes.keys():
                if key == var_type:
                    watch_list[variable] = {
                        "nestedness": 0, "parent class": var_type}

        to_pop = []

        if i < len(file_data) - 1:
            for variable in watch_list.keys():
                if file_data[i] == "{":
                    watch_list[variable]["nestedness"] += 1

                if file_data[i] == "}":
                    watch_list[variable]["nestedness"] -= 1

                if watch_list[variable]["nestedness"] < 0:
                    to_pop.append(variable)

        for p in to_pop:
            watch_list.pop(p)

        possible_change = read_next_word(file_data[i:], ignore_sep=False)

        if possible_change != None:
            for variable in watch_list.keys():
                if possible_change.startswith(variable):
                    par_class = watch_list[variable]["parent class"]
                    class_change = global_changes[par_class]

                    for change_from in class_change.keys():
                        if (possible_change.startswith(variable + "." + change_from)
                                or (par_class == None and possible_change == change_from)):

                            i = file_data.index(possible_change, i)
                            new_file_data += file_data[last_carry_index:i]
                            if par_class == None:
                                new_file_data += class_change[change_from]
                                last_carry_index = i + len(change_from)
                            else:
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

    global_changes = dict_update(global_changes, all_changes)

    return new_data


def check_camel_case(verif_file, fix_file, filepath, file_data):
    """Search and change wrong camel case"""

    global global_changes

    i = 0
    inside_class = None
    all_changes = {}

    nesting = 0

    new_data = ""

    while i < len(file_data):
        found_to_change = False
        variable = None
        lcc_variable = None

        if check_word_with_space(file_data[i:], "class") and not check_word_with_space(file_data[i:], "class var"):
            inside_class = read_next_word(file_data[i+6:])
            ucc_class = upper_camel_case(inside_class)

            new_data += file_data[i:i+6]
            i += 6

            if inside_class != ucc_class:
                class_changes = all_changes.get(inside_class)
                need_assign = False

                if class_changes == None:
                    class_changes = {}
                    all_changes = dict_update(
                        all_changes, {None: class_changes})
                    need_assign = True

                class_changes = dict_update(
                    class_changes, {inside_class: ucc_class})

                if need_assign:
                    all_changes = dict_update(
                        all_changes, {None: class_changes})

                new_data += ucc_class
                i += len(ucc_class)

        if check_word_with_space(file_data[i:], "var") or check_word_with_space(file_data[i:], "let"):
            variable = read_next_word(file_data[i+3:])
            lcc_variable = lower_camel_case(variable)

            new_data += file_data[i:i+4]
            i += 4

            found_to_change = True

        if check_word_with_space(file_data[i:], "func"):
            variable = read_next_word(file_data[i+4:])
            lcc_variable = lower_camel_case(variable)

            new_data += file_data[i:i+5]
            i += 5

            found_to_change = True

        if found_to_change:
            if variable != lcc_variable:
                class_changes = all_changes.get(inside_class)
                need_assign = False

                if class_changes == None:
                    class_changes = {}
                    all_changes = dict_update(
                        all_changes, {None: class_changes})
                    need_assign = True

                if class_changes.get(variable):
                    lcc_variable = lower_camel_case(
                        class_changes.get(variable))

                new_data += lcc_variable
                i += len(lcc_variable)

                class_changes = dict_update(
                    class_changes, {variable: lcc_variable})

                if need_assign:
                    all_changes = dict_update(
                        all_changes, {None: class_changes})

            found_to_change = False

        if file_data[i] == "{":
            nesting += 1

        if file_data[i] == "}":
            nesting -= 1

            if nesting == 0:  # class ended

                inside_class = None

        new_data += file_data[i]
        i += 1

    for class_changes in all_changes:
        for change_k in all_changes[class_changes]:
            file_write(
                fix_file, f"{filepath} Changed: wrong camel case on {change_k}")

    if len(all_changes) > 0:
        file_write(
            verif_file, f"{filepath} Error: wrong camel case declarations")

    global_changes = dict_update(global_changes, all_changes)

    return new_data


naming_fixers = [
    check_initializers,
    check_properties,
    check_camel_case
]
