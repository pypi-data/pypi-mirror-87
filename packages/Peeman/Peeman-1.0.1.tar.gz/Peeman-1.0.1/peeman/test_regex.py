
import json
import os
import re


regex_pattern =r'[^{]\{\{([^{}]+)\}\}[^}]'
#list_replace = {"url":"testurl", "test":"burger"}


def check_regex_unique(regex_pattern, data):
    match = re.findall(regex_pattern, json.dumps(data))
    return (list(set(match)))


def replace_string(replace_dict, data):
    for string_to_replace, value in replace_dict.items():
        replace_pattern = '(\{\{' + string_to_replace + '\}\})'
        replace_pattern_complied = re.compile(replace_pattern)
        data = re.sub(replace_pattern_complied, value, data)
    return data


def write_json(filename, data):
    with open(filename, "w") as outfile:
        outfile.write(data)


def place_holder_check_replace(data_string, list_replace):
    placeholders = None
    data_string = json.dumps(data_string)
    flag_replace = True
    placeholders = check_regex_unique(regex_pattern, data_string)
    # we have list here in placeholders which we will compare with dict keys here,
    # if all list values are in dict then we can move forward to replace something like below
    if list_replace and placeholders:
        for placeholder in placeholders:
            if not placeholder in list_replace:
                flag_replace = False
        if flag_replace:
            final_data = replace_string(list_replace, data_string)
            return json.loads(final_data)
        else:
            raise("some placeholders values are not passed")

    elif placeholders and not list_replace:
        raise(f"please provide the following placeholder value : {placeholders}")

    elif not( placeholders and list_replace):
        return json.loads(data_string)
    else:
        raise("Please check the input again")
    

