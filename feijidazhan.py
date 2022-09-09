from turtle import back
import pygame


# 完成整个程序的控制
def main():
    # 1. 创建一个窗口
    screen = pygame.display.set_mode((480,852),0,32)
    # 2. 创建一个图片做背景
    background = pygame.image.load("/home/dongweili/Pictures/beijing.png")
    # 3. 将北京图片贴到窗口中
    screen.blit(background, (0,0))

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
        # 4. 显示窗口中的内容
        pygame.display.update()



# 主函数
if __name__ == '__main__':
    main()
