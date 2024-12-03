import pygame
pygame.init()

class Timer:
    def __init__(self):
        self.time_start = 0  # 游戏开始的时间
        self.paused_duration = 0  # 总暂停时长
        self.pause_start_time = 0  # 暂停开始时刻
        self.is_paused = False  # 暂停状态标志

    def start(self):
        """开始计时"""
        self.time_start = pygame.time.get_ticks()  # 记录游戏开始的时间
        self.paused_duration = 0  # 重置暂停时长

    def pause(self):
        """暂停计时"""
        if not self.is_paused:
            self.pause_start_time = pygame.time.get_ticks()  # 记录暂停开始时间
            self.is_paused = True

    def resume(self):
        """恢复计时"""
        if self.is_paused:
            paused_time = pygame.time.get_ticks() - self.pause_start_time  # 计算暂停时长
            self.paused_duration += paused_time  # 更新总暂停时长
            self.is_paused = False

    def get_elapsed_time(self):
        """获取已经过去的时间（秒）"""
        if self.is_paused:
            # 在暂停时，时间不再增加，返回暂停期间的时间
            return (self.pause_start_time - self.time_start - self.paused_duration) // 1000
        else:
            # 在正常计时情况下，返回实际已用时间
            return (pygame.time.get_ticks() - self.time_start - self.paused_duration) // 1000