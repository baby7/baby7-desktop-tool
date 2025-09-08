import os
import json


def get_city_setting():
    drink_config = {}
    # 判断config文件夹是否存在
    if not os.path.exists(str(os.getcwd()) + r"\config"):
        os.mkdir(str(os.getcwd()) + r"\config")
    # 判断config文件是否存在
    config_path = str(os.getcwd()) + r"\config\city_setting.json"
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config_len = len(f.readlines())
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_len != 0:
                drink_config = json.load(f)
    if len(drink_config) == 0:
        drink_config = {
            "province": "",
            "city": "",
            "county": "",
            "countyName": ""
        }
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(drink_config, f)
    return drink_config


def set_city_setting(new_drink_config):
    drink_config = new_drink_config
    config_path = str(os.getcwd()) + r"\config\city_setting.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(drink_config, f)
    return drink_config
