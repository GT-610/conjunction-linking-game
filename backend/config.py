class GameConfig:
    def __init__(self):
        # 游戏主要状态
        self.username = "PLAYER"          # 默认用户名
        self.difficulty = None            # 游戏难度
        self.is_paused = False            # 是否暂停
        self.conjunction = None         # 当前选择的联结词
        self.final_score = 0              # 最终得分
        self.elapsed_time = 0             # 总用时

    def reset(self):
        """重置游戏状态"""
        self.username = "PLAYER"
        self.difficulty = None
        self.is_paused = False
        self.conjunction = None
        self.final_score = 0
        self.elapsed_time = 0

# 全局配置实例
config = GameConfig()
