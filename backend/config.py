class GameConfig:
    def __init__(self):
        # 游戏主要状态
        self.username = "PLAYER"          # 默认用户名
        self.difficulty = None            # 游戏难度
        self.is_paused = False            # 是否暂停
        self.cur_conj = None         # 当前选择的联结词
        self.is_game_end = False # 游戏是否结束
        self.is_cleared = False # 是否通关
        self.first_play = True          # 是否第一次游玩，默认为True

    # 重置游戏状态
    def reset(self):
        self.is_paused = False
        self.cur_conj = None
        self.is_game_end = False
        self.is_cleared = False

# 全局配置实例
config = GameConfig()

import json
import os

# 确保文件路径存在
settings_path = "saves/settings.json"

# 加载设置
def load_settings():
    if os.path.exists(settings_path):  # 如果文件存在
        with open(settings_path, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)  # 读取并解析 JSON 文件
                return data
            except json.JSONDecodeError:
                print("设置文件损坏，使用默认设置。")
                return {}
    else:
        return {}  # 文件不存在时返回空字典

# 保存配置到本地
import json
import os
# 确保文件路径存在
settings_path = "saves/settings.json"

# 加载设置
def load_settings():
    if os.path.exists(settings_path):  # 如果文件存在
        try:
            with open(settings_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # 读取并解析 JSON 文件
                if 'first_play' not in data:  # 如果没有此字段，添加默认值
                    data['first_play'] = True
                return data
        except json.JSONDecodeError:
            print("配置文件损坏，已覆盖默认配置。")
            create_empty_config_file()  # 文件损坏时创建空配置文件
            return {}  # 返回空字典
    else:
        create_empty_config_file()  # 文件不存在时创建空配置文件
        return {}  # 返回空字典

# 创建空的配置文件
def create_empty_config_file():
    # 如果文件不存在或损坏，则创建一个空的配置文件
    settings_data = {
        "username": "PLAYER",  # 默认用户名
        "first_play": config.first_play,  # 保存是否第一次游玩
    }
    os.makedirs(os.path.dirname(settings_path), exist_ok=True)  # 确保目录存在
    with open(settings_path, 'w', encoding='utf-8') as file:
        json.dump(settings_data, file, ensure_ascii=False, indent=4)
        print(f"配置文件 {settings_path} 已创建")

# 保存设置
def save_settings(config):
    # 创建保存数据的字典
    settings_data = {
        "username": config.username,
    }

    # 确保保存目录存在
    os.makedirs(os.path.dirname(settings_path), exist_ok=True)

    # 写入文件
    with open(settings_path, 'w', encoding='utf-8') as file:
        json.dump(settings_data, file, ensure_ascii=False, indent=4)
        print(f"配置文件 {settings_path} 已写入")

