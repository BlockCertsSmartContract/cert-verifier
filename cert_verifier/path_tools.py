import os


def get_root_dir():
    root_dir = os.path.abspath(__file__)
    for _ in range(2):
        root_dir = os.path.dirname(root_dir)
    return root_dir

def get_contr_info_path():
    return get_root_dir() + "/data/contr_info.json"
