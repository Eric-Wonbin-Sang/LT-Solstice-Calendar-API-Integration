import os


def get_curr_parent_dir(path_addition=None):
    return os.path.dirname(os.getcwd()) + path_addition if path_addition is not None else ""


def flip_list_list(data_list_list):
    return [list(x) for x in zip(*data_list_list)]


def is_none_list(data_list):
    for data in data_list:
        if data is not None:
            return False
    return True


def empty_strings_to_none(data_list_list):      # Make this recursive
    ret_list_list = []
    for data_list in data_list_list:
        ret_list = []
        for data in data_list:
            ret_list.append(data if data != "" else None)
        ret_list_list.append(ret_list)
    return ret_list_list


def split_2d_list_by_vertical_none_list(data_list_list):
    flipped_list_list = flip_list_list(data_list_list)
    for i, data_list in enumerate(flipped_list_list):
        if is_none_list(data_list):
            return flip_list_list(flipped_list_list[:i]), flip_list_list(flipped_list_list[i + 1:])
    return data_list_list, []


def dict_to_str(data_dict):
    ret_str = ""
    for key in data_dict:
        ret_str += "{}:  \t{}".format(key, data_dict[key])
    return ret_str


def tab_str(data_str):
    return "\t" + data_str.replace("\n", "\n\t")
