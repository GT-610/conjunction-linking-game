import pygame
from frontend.commons import small_font, RED, GRAY, WHITE, conj_click_sound
from backend.config import config

class ConjunctionBlock:
    def __init__(self, conj_name, position, size, callback):
        self.conj_name = conj_name
        self.conj_text = small_font.render(self.conj_name, True, WHITE)
        self.rect = pygame.Rect(position, (size, size))
        self.size = size
        self.selected = False  # 是否被选中
        self.callback = callback  # 回调函数

        conj_click_sound.set_volume(config.sfx_vol / 100)

    # 绘制联结词块
    def draw(self, screen):
        
        # 背景颜色
        pygame.draw.rect(screen, GRAY, self.rect)

        # 边框颜色：选中时为黄色，否则为白色
        border_color = RED if config.cur_conj == self.conj_name else WHITE
        pygame.draw.rect(screen, border_color, self.rect, 3)

        # 联结词文字
        screen.blit(self.conj_text, (self.rect.center[0] - self.conj_text.get_width() // 2, self.rect.center[1] - self.conj_text.get_height() // 2))

    # 处理点击事件
    def handle_click(self, pos):
        if self.rect.collidepoint(pos):
            conj_click_sound.stop()
            conj_click_sound.play()
            self.callback(self)
            return True
        return False
