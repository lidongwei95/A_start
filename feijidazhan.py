import pygame
from pygame import *
import time

image_path = "/home/dongweili/Pictures/"

# 完成整个程序的控制
def main():
    # 1. 创建一个窗口
    screen = pygame.display.set_mode((480,852),0,32)
    # 2. 创建一个图片做背景
    background = pygame.image.load(image_path + "beijing.png")
    # 创建一个图片，玩家的飞机
    player = pygame.image.load(image_path + "wo.png")

    x = 480 / 2 - 100 / 2
    y = 600

    # 飞机速度
    speed = 10

    # 让屏幕一直显示在窗口
    while True:
        # 3. 将背景图片贴到窗口中
        screen.blit(background, (0,0))
        # 将主飞机图片贴到窗口中
        screen.blit(player, (x, y))
        # 获取事件
        for event in pygame.event.get():
            # 判断事件类型
            if event.type == pygame.QUIT:
                # 执行pygame退出
                pygame.quit()
                # python程序退出
                exit()
        # 监听键盘事件
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            print("up")
            y -= speed
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            print("down")
            y += speed
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            print("left")
            x -= speed
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            print("right")
            x += speed
        if key_pressed[K_SPACE] :
            print("space")

        # 4. 显示窗口中的内容
        pygame.display.update()
        time.sleep(0.01)



# 主函数
if __name__ == '__main__':
    main()
