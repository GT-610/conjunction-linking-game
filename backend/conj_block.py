import pygame
from frontend.commons import *
class ConjunctionBlock:
    def __init__(self, conj_name, position, size, callback):
        """
        初始化联结词块
        :param conj_name: 联结词名称（例如 "与", "或", "异或"）
        :param position: 块的左上角位置 (x, y)
        :param size: 块的大小（正方形边长）
        :param callback: 点击后的回调函数，用于处理选中状态
        """
        self.conj_name = conj_name
        self.rect = pygame.Rect(position, (size, size))
        self.size = size
        self.selected = False
        self.callback = callback  # 处理点击后逻辑的函数

        # 字体初始化
        self.font = pygame.font.Font(font_path, 36)

    def draw(self, screen):
        """绘制联结词块"""
        # 背景颜色
        pygame.draw.rect(screen, GRAY, self.rect)

        # 边框颜色：选中时为黄色，否则为白色
        border_color = RED if self.selected else WHITE
        pygame.draw.rect(screen, border_color, self.rect, 3)

        # 显示联结词文字
        text = self.font.render(self.conj_name, True, BLACK)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_click(self, pos):
        """处理点击事件"""
        if self.rect.collidepoint(pos):
            # 调用回调函数切换选中状态
            self.callback(self)
            return True
        return False

    def set_selected(self, selected):
        """设置选中状态"""
        self.selected = selected
