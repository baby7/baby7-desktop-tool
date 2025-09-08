import os
import json


def get_special_list_config():
    special_list_config = []
    config_path = str(os.getcwd()) + r"\config\special_list.json"
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config_len = len(f.readlines())
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_len != 0:
                special_list_config = json.load(f)
    if special_list_config is None or special_list_config == []:
        special_list_config = []
    return special_list_config
