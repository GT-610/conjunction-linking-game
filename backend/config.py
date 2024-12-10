class GameConfig:
    def __init__(self):
        # 游戏主要状态
        self.username = "PLAYER" # 默认用户名
        self.difficulty = None # 游戏难度
        self.clear_rate = 0.0 # 完成度
        self.is_paused = False # 是否暂停
        self.cur_conj = None # 当前选择的联结词
        self.is_game_end = False # 游戏是否结束
        self.is_cleared = False # 是否通关

    # 重置游戏状态
    def reset(self):
        self.clear_rate = 0.0
        self.is_paused = False
        self.cur_conj = None
        self.is_game_end = False
        self.is_cleared = False

# 全局配置实例
config = GameConfig()
