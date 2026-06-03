"""This module contains functions to work with config file"""

import os
from json import load

BASE_DIR = "/home/knowyx/proj/py/vkoltse_fromweb/vkoltse_a"  # put here the same path as in config


def get_config_data(setting):
    """Function to read config data and return setting by key"""
    with open(os.path.join(BASE_DIR, "config/config.json"), encoding="UTF-8") as f:
        data = load(f)
    if setting in data.keys():
        return data[setting]
    return "Failed to find setting in config"
