import os
import json


def get_drinking_setting():
    drink_config = {}
    config_path = str(os.getcwd()) + r"\config\drinking_setting.json"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config_len = len(f.readlines())
        with open(config_path, 'r') as f:
            if config_len != 0:
                drink_config = json.load(f)
    if len(drink_config) == 0:
        drink_config = {
            "drinking_count": 8,            # 喝水数量
            "view_message": "positive"      # 窗口信息 正着计数(positive)/倒着计数(negative)
        }
        with open(config_path, 'w') as f:
            json.dump(drink_config, f)
    return drink_config


def set_drinking_setting(new_drink_config):
    drink_config = new_drink_config
    config_path = str(os.getcwd()) + r"\config\drinking_setting.json"
    with open(config_path, 'w') as f:
        json.dump(drink_config, f)
    return drink_config
