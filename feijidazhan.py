from turtle import back
import pygame
from pygame import *


image_path = "/home/dongweili/Pictures/"

# 完成整个程序的控制
def main():
    # 1. 创建一个窗口
    screen = pygame.display.set_mode((480,852),0,32)
    # 2. 创建一个图片做背景
    background = pygame.image.load(image_path + "beijing.png")
    # 创建一个图片，玩家的飞机
    player = pygame.image.load(image_path + "wo.png")
    # 3. 将背景图片贴到窗口中
    screen.blit(background, (0,0))
    # 将主飞机图片贴到窗口中
    screen.blit(player, (480/2 - 100/2, 600))

    # 让屏幕一直显示在窗口
    while True:
        # 获取事件
        for event in pygame.event.get():
            # 判断事件类型
            if event.type == pygame.QUIT:
                # 执行pygame退出
                pygame.quit()
                # python程序退出
                exit()
            # 响应键盘事件
            elif event.type == pygame.KEYDOWN:
                # 检验按键是否是a或者left
                if event.key == K_a or event.key == pygame.K_LEFT:
                    print("left")
                elif event.key == K_d or event.key == pygame.K_RIGHT:
                    print("right")
                elif event.key == pygame.K_w or event.key == pygame.K_UP:
                    print("up")
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    print("down")
        # 4. 显示窗口中的内容
        pygame.display.update()



# 主函数
if __name__ == '__main__':
    main()
