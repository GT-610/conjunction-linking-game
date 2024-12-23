from pathlib import Path
import pygame
from backend.config import config
pygame.font.init()
pygame.mixer.init()

# 分辨率和屏幕
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# 资源文件夹
assets_dir = Path("assets")

# 字体
font_path = assets_dir/"fonts"/"SourceHanSansCN-Regular.otf"
font = pygame.font.Font(font_path, 48)  # 大字体
small_font = pygame.font.Font(font_path, 36)  # 小字体

# 声音
button_click_sound = pygame.mixer.Sound(assets_dir/"sounds"/"button_click.mp3")
conj_click_sound = pygame.mixer.Sound(assets_dir/"sounds"/"conj_click.mp3")
hint_sound = pygame.mixer.Sound(assets_dir/"sounds"/"hint.mp3")
link_sound = pygame.mixer.Sound(assets_dir/"sounds"/"link.mp3")
notlink_sound = pygame.mixer.Sound(assets_dir/"sounds"/"notlink.mp3")
success_sound = pygame.mixer.Sound(assets_dir/"sounds"/"success.mp3")
failure_sound = pygame.mixer.Sound(assets_dir/"sounds"/"failure.mp3")


# 背景
class BgManager:
    def __init__(self, image_path, brightness):
        self.bgi = pygame.image.load(image_path).convert()
        if brightness < 255:
            self.dark_overlay = pygame.Surface(self.bgi.get_size(), flags=pygame.SRCALPHA)
            alpha = 255 - brightness
            self.dark_overlay.fill((0, 0, 0, alpha))

    def draw(self, screen):
        screen.blit(self.bgi, (0, 0))
        screen.blit(self.dark_overlay, (0, 0))
bg0 = BgManager(assets_dir/"backgrounds"/"bg0.jpg", 100)

# 按钮参数
button_width = 150
button_height = 50
vertical_spacing = 80

# 按钮类
class Button:
    def __init__(self, text, x, y, width, height, callback=None, hover_color=BLUE):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.callback = callback
        self.color = GRAY
        self.hover_color = hover_color
        button_click_sound.set_volume(config.sfx_vol / 100)

    def draw(self, screen):
        # 检测鼠标是否悬停
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        # 绘制按钮文本
        text_surface = small_font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    # 检查是否被点击
    def check_click(self):
        if self.callback and self.rect.collidepoint(pygame.mouse.get_pos()):
            button_click_sound.play()
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

    def draw(self, screen):
        # 绘制滑轨
        pygame.draw.rect(screen, GRAY, self.rect)
        # 绘制滑块
        pygame.draw.rect(screen, BLUE if self.is_dragging else WHITE, self.knob_rect)

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
        self.font = small_font

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y - 8))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = BLUE if self.active else GRAY

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
