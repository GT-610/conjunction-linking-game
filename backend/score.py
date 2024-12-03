class Score:
    def __init__(self):
        self.score = 0

    def add_score(self, points: int):
        """增加分数"""
        self.score += points

    def get_score(self):
        """获取当前分数"""
        return self.score

    def reset(self):
        """重置分数"""
        self.score = 0
