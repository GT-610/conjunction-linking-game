from pathlib import Path
import pygame
from backend.config import config
pygame.font.init()
pygame.mixer.init()

# 分辨率和缩放
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
scale = max(SCREEN_WIDTH / 1280, SCREEN_HEIGHT / 720)


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
font = pygame.font.Font(font_path, int(48 * scale))  # 大字体
small_font = pygame.font.Font(font_path, int(36 * scale))  # 小字体

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

        # 计算缩放因子
        bg_width, bg_height = self.bgi.get_size()
        bg_scale = max(SCREEN_WIDTH / bg_width, SCREEN_HEIGHT / bg_height)  # 最大平铺
        # 缩放背景图片
        self.bgi = pygame.transform.scale(self.bgi, (bg_width * scale, bg_height * scale))
        del bg_width, bg_height, bg_scale

        if brightness < 255:
            self.dark_overlay = pygame.Surface(self.bgi.get_size(), flags=pygame.SRCALPHA)
            alpha = 255 - brightness
            self.dark_overlay.fill((0, 0, 0, alpha))

    def draw(self, screen):
        bg_width, bg_height = self.bgi.get_size()
        start_x = (SCREEN_WIDTH - bg_width) // 2
        start_y = (SCREEN_HEIGHT - bg_height) // 2
        screen.blit(self.bgi, (start_x, start_y))
        screen.blit(self.dark_overlay, (start_x, start_y))

bg0 = BgManager(assets_dir/"backgrounds"/"bg0.jpg", 100)

# 按钮参数
button_width = 150 * scale
button_height = 50 * scale
vertical_spacing = 80 * scale

# 按钮类
class Button:
    def __init__(self, text, x, y, callback=None, hover_color=BLUE):
        self.text = small_font.render(text, True, WHITE)
        self.callback = callback
        self.hover_color = hover_color
        self.color = GRAY

        # 测量文本宽度
        text_width = self.text.get_width()
        text_height = self.text.get_height()

        # 动态调整按钮宽度和高度，宽度最小为 button_width
        self.width = max(button_width, text_width)
        self.height = max(button_height, text_height)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        button_click_sound.set_volume(config.sfx_vol / 100)

    def draw(self, screen):
        # 检测鼠标是否悬停
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text, (self.rect.center[0] - self.text.get_width() // 2, self.rect.center[1] - self.text.get_height() // 2))

    # 检查是否被点击
    def check_click(self):
        if self.callback and self.rect.collidepoint(pygame.mouse.get_pos()):
            button_click_sound.play()
            self.callback()

# 滑条类
class Slider:
    def __init__(self, x, y, width, min_value=0, max_value=100, initial_value=50):
        self.width = width
        self.height = 10  # 滑轨高度固定为 10
        self.knob_width = 10 * scale
        self.knob_height = 20 * scale

        # 滑条矩形，以中心点为基准计算左上角位置
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)

        # 滑块矩形
        knob_x = self.rect.x + (initial_value - min_value) / (max_value - min_value) * self.width - self.knob_width // 2
        knob_y = self.rect.y - (self.knob_height - self.height) // 2
        self.knob_rect = pygame.Rect(knob_x, knob_y, self.knob_width, self.knob_height)

        self.min_value = min_value
        self.max_value = max_value
        self.value = initial_value
        self.is_dragging = False

    def draw(self, screen):
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
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (x, y)
        self.text = text
        self.active = False
        self.color = GRAY
        self.font = small_font

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 2)
        text_surface = self.font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + 5 * scale, self.rect.y - 8 * scale))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = (0, 200, 255) if self.active else GRAY

        elif event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
