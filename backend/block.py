import pygame

from frontend.commons import small_font, BLUE, WHITE, YELLOW, BLACK

class Block:
    def __init__(self, map, point, block_size, offset_x, offset_y):
        self.innerX, self.innerY = point  # 块的位置 (map的坐标)
        self.value = map[self.innerX][self.innerY]  # 块的值 (0 或 1)

        # 块的基本信息
        self.outerWidth = block_size # 外部尺寸
        self.outerX = offset_x + self.innerY * block_size  # 外部 x 坐标
        self.outerY = offset_y + self.innerX * block_size  # 外部 y 坐标
        self.outerCenterPoint = (self.outerX + int(self.outerWidth / 2), self.outerY + int(self.outerWidth / 2))
        self.rect = pygame.Rect(self.outerX, self.outerY, self.outerWidth, self.outerWidth)

        # 选中状态
        self.selected = False

    def draw(self, screen):
        # 根据块的值 (0 或 1) 选择颜色
        color = WHITE if self.value == 0 else BLUE
        pygame.draw.rect(screen, color, (self.outerX, self.outerY, self.outerWidth, self.outerWidth))
        pygame.draw.rect(screen, BLACK, (self.outerX, self.outerY, self.outerWidth, self.outerWidth), 2)

        # 如果块被选中，绘制黄色边框
        if self.selected:
            pygame.draw.rect(screen, YELLOW, (self.outerX, self.outerY, self.outerWidth, self.outerWidth), 4)  # 黄色边框

        # 绘制块的边界
        pygame.draw.rect(screen, BLACK, (self.outerX, self.outerY, self.outerWidth, self.outerWidth), 2)

        # 渲染块的值（0 或 1）
        text_color = BLACK if self.value == 0 else WHITE
        value_text = small_font.render(str(self.value), True, text_color)
        screen.blit(value_text, (self.outerX + (self.outerWidth - value_text.get_width()) // 2, self.outerY + (self.outerWidth - value_text.get_height()) // 2))

    # 切换选中状态
    def toggle_selection(self):
        self.selected = not self.selected
 