import math
import copy

def learning(attributes, examples, parent_examples, level):
    if not examples:
        return {level: plurality_val(parent_examples)}
    elif examples.count(examples[0]) == len(examples):
        return {level: examples[0]}
    elif no_attributes(attributes):
        return {level: plurality_val(examples)}
    else:
        max_key = argmax(attributes, examples)
        root = create_tree_entry(max_key, attributes[max_key], level)
        exs = copy.deepcopy(examples)
        a = attributes[max_key]
        attrs = copy.deepcopy(attributes)

        for attribute_item in set(a):
            indexes_to_delete = []
            for i in range(0, len(a)):
                if a[i] != attribute_item:
                    indexes_to_delete.append(i)

            indexes_to_delete.sort(reverse=True)

            for index in indexes_to_delete:
                del exs[index]
                for attr_key in attrs:
                    del attrs[attr_key][index]

            del attrs[max_key]  # TODO
            root = create_sub_tree_entry(root, learning(attrs, exs, examples, level+1))
            exs = copy.deepcopy(examples)
            attrs = copy.deepcopy(attributes)
        return root
def plurality_val(examples):
    example_set = set(examples)
    return max(example_set, key=examples.count)

def no_attributes(attributes):
    for attribute in attributes.values():
        if len(attribute) != 0:
            return False
    return True

def create_tree_entry(key, a, level):
    attribute_set = set(a)
    tree_entry = {key: list(attribute_set)}
    return {level: tree_entry}

def create_sub_tree_entry(root, entries):
    expanded_root = root

    # if level of entry exists in tree, append tree with entry
    # else, create new level and set entry as first list item
    for entry_key in entries:
        if entry_key in expanded_root:
            expanded_root[entry_key] = [expanded_root[entry_key], entries[entry_key]]
        else:
            expanded_root[entry_key] = entries[entry_key]

    return expanded_root

def argmax(attributes, examples):
    max_information_gane = 0
    imp_key = {}
    for key in attributes.keys():
        ig_a = importance(attributes[key], examples)
        if ig_a > max_information_gane:
            max_information_gane = ig_a
            imp_key = key
    return imp_key


# a = "sunny, sunny, rainy, sunny, sunny"
# examples = "1, 1, 0, 1, 0"
def importance(a, examples):
    attribute_dict = {}
    for i in range(0, len(a)):
        if a[i] in attribute_dict:
            attribute_dict[a[i]][0] += 1
        else:
            attribute_dict[a[i]] = [1, 0]
        if examples[i] == 1:
            attribute_dict[a[i]][1] += 1
    return information_gane(examples, attribute_dict)


def information_gane(examples, rem_data):
    d_chance = (examples.count(1) / len(examples))
    h_d = H(d_chance)


    for key, value in rem_data.items():
        rem_chance = value[1] / value[0]
        rem_factor = value[0]/ len(examples)

        if (rem_chance != 0) and (rem_chance!= 1):

            h_d = h_d - rem_factor*H(rem_chance)

    return h_d

def H(chance):
    reverse_chance = (1 - chance)
    return -(chance * math.log(chance, 2) + reverse_chance * math.log(reverse_chance, 2))

def pretty_print(tree):
    longest_string = 0
    all_strings = []
    indentations = 0

    for level in tree:
        level_string = None
        if level == 0:
            level_string = 'root:   '
        else:
            level_string = 'level ' + str(level) + ':'

        root_strings = [level_string]
        sub_strings = ['actions:']
        indentations += 1

        for entry in tree[level]:
            if type(entry) is str:
                entry = tree[level]
            if type(entry) is dict:
                root_strings.append('<' + str(list(entry.keys())[0]) + '>')
                for value in list(entry.values())[0]:
                    sub_strings.append('[' + str(value) + ']')
                    if(len(sub_strings[-1]) > longest_string):
                        longest_string = len(sub_strings[-1])
            else:
                root_strings.append(str(entry))
                sub_strings.append(None)
            if len(root_strings[-1]) > longest_string:
                longest_string = len(root_strings[-1])
        all_strings.append(root_strings)
        if(sub_strings.count(None) < len(sub_strings) -1):
            all_strings.append(sub_strings)

    empty_places = []
    for j in range(len(all_strings)):
        print("")
        for i in range(len(all_strings[j])):
            if(i == 1):
                print("".ljust(longest_string * indentations), end="")
                if j % 2 == 0:
                    indentations -=1
            if(all_strings[j][i] is not None):
                if i in empty_places:
                    print("".ljust(longest_string), end="    ")
                all_strings[j][i] = all_strings[j][i].ljust(longest_string)
            else:
                all_strings[j][i] = "".ljust(longest_string)
                if i not in empty_places:
                    empty_places.append(i)

            print(all_strings[j][i], end="    ")


if __name__ == '__main__':

    attributes = {'sky': ['sunny', 'sunny', 'rainy', 'sunny', 'sunny', 'rainy'],
                  'air': ['warm', 'warm', 'warm', 'warm', 'warm', 'warm'],
                  'humid': ['normal', 'high', 'high', 'high', 'normal', 'high'],
                  'wind': ['strong', 'strong', 'strong', 'strong', 'weak', 'strong'],
                  'water': ['warm', 'warm',  'warm',  'cool',  'warm', 'warm'],
                  'forecast': ['same', 'same',  'change',  'change',  'same', 'change']}

    examples = [1, 1, 0, 1, 0, 0]

    tree = learning(attributes, examples, [], 0)

    print('unformatted tree :', tree)

    pretty_print(tree)

