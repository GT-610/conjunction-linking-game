from frontend.commons import BLACK, WHITE, SCREEN_WIDTH, SCREEN_HEIGHT, scale, bg0
import pygame
from random import randint

# 显示加载进度
def display_loading_message(screen, message, font):
    bg0.draw(screen)

    # 显示加载文本
    gen_text = font.render("游戏加载中", True, WHITE)
    screen.blit(gen_text, ((SCREEN_WIDTH - gen_text.get_width()) // 2, (SCREEN_HEIGHT - gen_text.get_height()) // 2 - 50 * scale))
    del gen_text

    # 显示加载项
    loading_text = font.render(message, True, WHITE)
    screen.blit(loading_text, ((SCREEN_WIDTH - loading_text.get_width()) // 2, (SCREEN_HEIGHT - loading_text.get_height()) // 2))
    # pygame.time.delay(randint(150, 300)) # 有意延迟，让用户知道游戏在加载（调试时不使用）
    pygame.display.update()