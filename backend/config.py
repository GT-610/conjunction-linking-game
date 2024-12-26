class GameConfig:
    def __init__(self):
        # 游戏主要状态
        self.username = "PLAYER" # 默认用户名
        self.position = "main_menu" # 当前页面位置
        self.sfx_vol = 50 # 音效音量
        self.params = {} # 切换页面时的传参
        self.difficulty = None # 游戏难度
        self.clear_rate = 0.0 # 完成度
        self.is_paused = False # 是否暂停
        self.cur_conj = None # 当前选择的联结词
        self.is_game_end = False # 游戏是否结束
        self.is_cleared = False # 是否通关
        self.restart = False # 是否重启页面
        self.first_play = first_play = [True, True, True, True]  # 是否第一次游玩

    # 重置游戏状态
    def reset(self):
        self.clear_rate = 0.0
        self.is_paused = False
        self.cur_conj = None
        self.is_game_end = False
        self.is_cleared = False
        self.restart = False

# 全局配置实例
config = GameConfig()

# 难度映射
DIFFICULTY_MAPPING = ["基本", "高级", "专家", "大师"]

# 版本
ver = "1.00"
minver = ""

# 传参
def navigate_with_params(position, **kwargs):
    config.position = position
    config.params = kwargs
    if kwargs:
        print(f"切换到页面 {position}，传递参数：{kwargs}")

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
                    data['first_play'] = [True, True, True]
                return data
        except json.JSONDecodeError:
            print("配置文件损坏，已覆盖默认配置。")
    
    # 如果文件不存在或损坏，创建并返回默认配置
    settings_data = {
        "username": "PLAYER",
        "sfx_vol": 50,
        "first_play": config.first_play,
    }
    os.makedirs(os.path.dirname(settings_path), exist_ok=True)  # 确保目录存在
    with open(settings_path, 'w', encoding='utf-8') as file:
        json.dump(settings_data, file, ensure_ascii=False, indent=4)
        print(f"配置文件 {settings_path} 已创建")
    return settings_data


# 保存设置
def save_settings(config):
    settings_data = {
        "username": config.username,
        "sfx_vol": config.sfx_vol,
        "first_play": config.first_play
    }

    # 确保保存目录存在
    os.makedirs(os.path.dirname(settings_path), exist_ok=True)

    # 写入文件
    with open(settings_path, 'w', encoding='utf-8') as file:
        json.dump(settings_data, file, ensure_ascii=False, indent=4)
        print(f"配置文件 {settings_path} 已写入")

