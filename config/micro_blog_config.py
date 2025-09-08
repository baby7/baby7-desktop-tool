import os
import json


def get_micro_blog_config():
    micro_blog_config = {}
    config_path = str(os.getcwd()) + r"\config\micro_blog.json"
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config_len = len(f.readlines())
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_len != 0:
                micro_blog_config = json.load(f)
    if micro_blog_config is None or micro_blog_config == {}:
        micro_blog_config = {
          "active": False,
          "screen_word_list": [],
          "screen_type_list": []
        }
    return micro_blog_config


def set_micro_blog_config(new_micro_blog_config):
    micro_blog_config = new_micro_blog_config
    config_path = str(os.getcwd()) + r"\config\micro_blog.json"
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(micro_blog_config, f, ensure_ascii=False)
    return micro_blog_config
