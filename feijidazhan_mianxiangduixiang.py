import random
import pygame
from pygame.constants import *
import time



image_path = "/home/dongweili/Pictures/"


class EnemyPlane(object):
    # 初始化属性
    def __init__(self, screen):
        # 创建一个图片，玩家的飞机
        self.player = pygame.image.load(image_path + "enemy01.png") # 95 * 90

        self.x = 0
        self.y = 0

        # 飞机速度
        self.speed = 5
        # 记录当前窗口对向
        self.screen = screen
        # 装子弹列表
        self.bullets = []
        # 敌机移动方向
        self.direction = "right"


    def display(self):
        # 将主飞机图片贴到窗口中
        self.screen.blit(self.player, (self.x, self.y))
        # # 遍历所有子弹
        for bullet in self.bullets:
            # 让子弹飞 修改子弹y坐标
            bullet.auto_move()
            # 子弹显示在窗口
            bullet.display()

    def auto_move(self):
        if self.direction == "right":
            self.x += self.speed
        elif self.direction == "left":
            self.x -= self.speed

        if self.x > 480 - 95:
            self.direction = "left"
        elif self.x < 0:
            self.direction = "right"

    def auto_fire(self):
        """自动开火，创建子弹对向，添加进列表"""
        random_num = random.randint(1, 20)
        if random_num == 8:
            bullet = EnemyBullet(self.screen, self.x, self.y)
            self.bullets.append(bullet)


class HeroPlane(object):
    # 初始化属性
    def __init__(self, screen):
        # 创建一个图片，玩家的飞机
        self.player = pygame.image.load(image_path + "heroplane.png")

        self.x = 480 / 2 - 100 / 2
        self.y = 600

        # 飞机速度
        self.speed = 5
        # 记录当前窗口对向
        self.screen = screen
        # 装子弹列表
        self.bullets = []

    def key_control(self):
        # 监听键盘事件
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            print("up")
            self.y -= self.speed
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            print("down")
            self.y += self.speed
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            print("left")
            self.x -= self.speed
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            print("right")
            self.x += self.speed
        if key_pressed[K_SPACE] :
            print("space")
            # 按下空格键发射子弹
            bullet = Bullet(self.screen, self.x, self.y)
            # 把子弹添加到列表里
            self.bullets.append(bullet)

    def display(self):
        # 将主飞机图片贴到窗口中
        self.screen.blit(self.player, (self.x, self.y))
        # 遍历所有子弹
        for bullet in self.bullets:
            # 让子弹飞 修改子弹y坐标
            bullet.auto_move()
            # 子弹显示在窗口
            bullet.display()

# 子弹类
# 属性
class Bullet(object):
    def __init__(self, screen, x, y):
        # 坐标
        self.x = x + 100 / 2 - 22 / 2  # 100飞机长度，22子弹长宽
        self.y = y - 22
        # 图片
        self.image = pygame.image.load(image_path + "bullet.png")
        # 窗口
        self.screen = screen
        # 速度
        self.speed = 10

    def display(self):
        """显示子弹到窗口"""
        self.screen.blit(self.image, (self.x, self.y))

    def auto_move(self):
        """让子弹飞"""
        self.y -= self.speed


# 子弹类
# 属性
class EnemyBullet(object):
    def __init__(self, screen, x, y):
        # 坐标
        self.x = x + 94 / 2 - 20 / 2  
        self.y = y + 30
        # 图片
        self.image = pygame.image.load(image_path + "bullet01.png") # 20 * 30
        # 窗口
        self.screen = screen
        # 速度
        self.speed = 10

    def display(self):
        """显示子弹到窗口"""
        self.screen.blit(self.image, (self.x, self.y))

    def auto_move(self):
        """让子弹飞"""
        self.y += self.speed


# 完成整个程序的控制
def main():

    # 1. 创建一个窗口
    screen = pygame.display.set_mode((480,852),0,32)
    # 2. 创建一个图片做背景
    background = pygame.image.load(image_path + "beijing01.png")
    # 创建一个飞机对向，注意不要忘记传窗口
    player = HeroPlane(screen)
    # 创建一个敌方飞机对象，注意不要忘记传窗口
    enemyplane = EnemyPlane(screen)

    # 让屏幕一直显示在窗口
    while True:
        # 3. 将背景图片贴到窗口中
        screen.blit(background, (0,0))

        # 获取事件
        for event in pygame.event.get():
            # 判断事件类型
            if event.type == pygame.QUIT:
                # 执行pygame退出
                pygame.quit()
                # python程序退出
                exit()

        # 执行飞机按键监听
        player.key_control()
        # 飞机的显示
        player.display()
        # 敌方飞机显示
        enemyplane.display()
        # 敌方自动移动
        enemyplane.auto_move()
        # 敌方自动开火
        enemyplane.auto_fire()

        # 4. 显示窗口中的内容
        pygame.display.update()
        time.sleep(0.01)



# 主函数
if __name__ == '__main__':
    main()
