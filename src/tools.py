#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @IDE       :PyCharm
# @Project   :apikey_query
# @FileName  :tools.py
# @Time      :2025/2/24 15:34
# @Author    :Hacon

import yaml

# 读取 YAML 文件
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)  # 使用 safe_load 以避免潜在的安全问题
    return config