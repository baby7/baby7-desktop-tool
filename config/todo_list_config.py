import os
import json


def get_todo_list_config():
    todo_list_config = {}
    config_path = str(os.getcwd()) + r"\config\todo_list.json"
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config_len = len(f.readlines())
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_len != 0:
                todo_list_config = json.load(f)
    if todo_list_config is None or todo_list_config == {}:
        todo_list_config = {"proceed_todo_list": [], "complete_todo_list": []}
    return todo_list_config


def set_todo_list_config(new_todo_list_config):
    todo_list_config = new_todo_list_config
    config_path = str(os.getcwd()) + r"\config\todo_list.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(todo_list_config, f, ensure_ascii=False)
    return todo_list_config
