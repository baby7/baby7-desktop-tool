import os
import json


def get_start_module_list_config():
    start_module_list_config = {}
    config_path = str(os.getcwd()) + r"\config\start_module_list.json"
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config_len = len(f.readlines())
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_len != 0:
                start_module_list_config = json.load(f)
    if start_module_list_config is None or start_module_list_config == {}:
        start_module_list_config = {"start_module_list": []}
    return start_module_list_config


def set_start_module_list_config(new_start_module_list_config):
    start_module_list_config = new_start_module_list_config
    config_path = str(os.getcwd()) + r"\config\start_module_list.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(start_module_list_config, f, ensure_ascii=False)
    return start_module_list_config
