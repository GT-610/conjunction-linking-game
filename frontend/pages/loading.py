from frontend.commons import BLACK, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT
import pygame
pygame.init()

# 显示加载进度的函数
def display_loading_message(screen, message, font):
    screen.fill(BLACK)  # 清空屏幕
    loading_text = font.render(message, True, WHITE)
    loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(loading_text, loading_rect)
    pygame.display.update()