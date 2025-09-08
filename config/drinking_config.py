import os
import json


def get_drinking_config():
    drinking_config = []
    config_path = str(os.getcwd()) + r"\config\drinking_config.json"
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config_len = len(f.readlines())
        with open(config_path, 'r') as f:
            if config_len != 0:
                drinking_config = json.load(f)
    drinking_config_result = []
    for record in drinking_config:
        drinking_config_result.append(record)
    return drinking_config_result


def set_drinking_config(add_record):
    drinking_config = get_drinking_config()
    config_path = str(os.getcwd()) + r"\config\drinking_config.json"
    if os.path.exists(config_path):
        tag = True
        for record in drinking_config:
            if record['date'] == add_record['date']:
                record['count'] = add_record['count']
                tag = False
                break
        if tag:
            drinking_config.append(add_record)
    else:
        drinking_config = [add_record]
    with open(config_path, 'w') as f:
        json.dump(drinking_config, f)
    return drinking_config
