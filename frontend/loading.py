from frontend.commons import BLACK, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, bg0
import pygame

# 显示加载进度
def display_loading_message(screen, message, font):
    bg0.draw(screen)

    # 显示加载文本
    map_generating_text = font.render("游戏加载中", True, WHITE)
    map_generating_rect = map_generating_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(map_generating_text, map_generating_rect)

    # 显示加载项
    loading_text = font.render(message, True, WHITE)
    loading_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(loading_text, loading_rect)
    pygame.display.update()