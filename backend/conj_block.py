import pygame
from frontend.commons import font_path, RED, BLACK, GRAY, WHITE
from backend.config import config

class ConjunctionBlock:
    def __init__(self, conj_name, position, size, callback):
        self.conj_name = conj_name  # 联结词名称
        self.rect = pygame.Rect(position, (size, size))
        self.size = size
        self.selected = False  # 是否被选中
        self.callback = callback  # 回调函数

        # 字体初始化
        self.font = pygame.font.Font(font_path, 36)

    # 绘制联结词块
    def draw(self, screen):
        
        # 背景颜色
        pygame.draw.rect(screen, GRAY, self.rect)

        # 边框颜色：选中时为黄色，否则为白色
        border_color = RED if config.cur_conj == self.conj_name else WHITE
        pygame.draw.rect(screen, border_color, self.rect, 3)

        # 联结词文字
        text = self.font.render(self.conj_name, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    # 处理点击事件
    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            # 调用回调函数切换选中状态
            self.callback(self)
            return True
        return False
