import pygame

# 初始化 pygame
pygame.init()

# 设置颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 102, 255)

# 字体
font_path = "fonts/SourceHanSansCN-Regular.otf"  # 字体文件路径
button_font = pygame.font.Font(font_path, 36)  # 按钮字体

# 按钮类
class Button:
    def __init__(self, text, x, y, width, height, callback=None, hover_color=BLUE):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.color = GRAY
        self.hover_color = hover_color

    def draw(self, surface):
        # 检测鼠标是否悬停
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(surface, self.hover_color, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)
        # 绘制按钮文本
        text_surface = button_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self):
        if self.callback and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.callback()

# 滑条类
class Slider:
    def __init__(self, x, y, width, min_value=0, max_value=100, initial_value=50):
        self.rect = pygame.Rect(x, y, width, 10)
        self.knob_rect = pygame.Rect(x + (initial_value / max_value) * width - 5, y - 5, 10, 20)
        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.is_dragging = False

    def draw(self, surface):
        # 绘制滑轨
        pygame.draw.rect(surface, GRAY, self.rect)
        # 绘制滑块
        pygame.draw.rect(surface, BLUE if self.is_dragging else WHITE, self.knob_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.knob_rect.collidepoint(event.pos):
                self.is_dragging = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.is_dragging = False
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            # 更新滑块位置
            new_x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.width))
            self.knob_rect.x = new_x - self.knob_rect.width // 2
            # 计算当前值
            self.value = self.min_value + (new_x - self.rect.x) / self.rect.width * (self.max_value - self.min_value)

# 文本输入框
class TextInputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.active = False
        self.color = GRAY
        self.font = button_font

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, WHITE)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = BLUE if self.active else GRAY
        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
