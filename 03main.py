import random
import pygame
from pygame.constants import *
import time


image_path = "/home/dongweili/Pictures/"


class EnemyPlane(pygame.sprite.Sprite):
    # 初始化属性
    def __init__(self, screen):
        # 这个精灵的初始化方法，必须调用
        pygame.sprite.Sprite.__init__(self)

        # 创建一个图片，玩家的飞机
        self.player = pygame.image.load(image_path + "enemy01.png")

        # 根据图片iamge获取矩形对象
        self.rect = self.player.get_rect()  # rect: 矩形
        self.rect.topleft = [0, 0]  # 确定矩形左上坐标位置


        # 飞机速度
        self.speed = 5
        # 记录当前窗口对向
        self.screen = screen
        # 装子弹列表
        self.bullets = pygame.sprite.Group()
        # 敌机移动方向
        self.direction = "right"


    def display(self):
        # 将主飞机图片贴到窗口中
        self.screen.blit(self.player, self.rect)
        # 更新子弹坐标
        self.bullets.update()

        # 把所有子弹全部添加到屏幕
        self.bullets.draw(self.screen)

    def auto_move(self):
        if self.direction == "right":
            self.rect.right += self.speed
        elif self.direction == "left":
            self.rect.right -= self.speed

        if self.rect.right > 480 - 95:
            self.direction = "left"
        elif self.rect.right < 0:
            self.direction = "right"

    def auto_fire(self):
        """自动开火，创建子弹对向，添加进列表"""
        random_num = random.randint(1, 20)
        if random_num == 8:
            bullet = EnemyBullet(self.screen, self.rect.left, self.rect.top)
            self.bullets.add(bullet)

    def update(self):
        self.display()
        self.auto_fire()
        self.auto_move()


class HeroPlane(pygame.sprite.Sprite):
    # 初始化属性
    def __init__(self, screen):
        # 这个精灵的初始化方法，必须调用
        pygame.sprite.Sprite.__init__(self)

        # 创建一个图片，玩家的飞机
        self.player = pygame.image.load(image_path + "heroplane.png")

        # 根据图片iamge获取矩形对象
        self.rect = self.player.get_rect()  # rect: 矩形
        self.rect.topleft = [480 / 2 - 100 / 2, 600]  # 确定矩形左上坐标位置


        # 飞机速度
        self.speed = 5
        # 记录当前窗口对向
        self.screen = screen
        # 装子弹列表
        self.bullets = pygame.sprite.Group()

    def key_control(self):
        # 监听键盘事件
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            print("up")
            self.rect.top -= self.speed
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            print("down")
            self.rect.bottom += self.speed
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            print("left")
            self.rect.left -= self.speed
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            print("right")
            self.rect.right += self.speed
        if key_pressed[K_SPACE] :
            print("space")
            # 按下空格键发射子弹
            bullet = Bullet(self.screen, self.rect.left, self.rect.top)
            # 把子弹添加到列表里
            self.bullets.add(bullet)

    def display(self):
        # 将主飞机图片贴到窗口中
        self.screen.blit(self.player, self.rect)
        # 更新子弹坐标
        self.bullets.update()

        # 把所有子弹全部添加到屏幕
        self.bullets.draw(self.screen)

    def update(self):
        self.key_control()
        self.display()


# 子弹类
# 属性
class Bullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self)

        # 图片
        self.image = pygame.image.load(image_path + "bullet.png")

        # h获取矩形对象
        self.rect = self.image.get_rect()
        self.rect.topleft = [x + 100 / 2 - 22 / 2, y - 22]

        # 窗口
        self.screen = screen
        # 速度
        self.speed = 10


    def update(self):
        # 修改子弹坐标
        self.rect.top -= self.speed
        # 如果子弹移出屏幕，则小辉子弹对象
        if self.rect.top < -22:
            self.kill()


# 子弹类
# 属性
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, screen, x, y):
        pygame.sprite.Sprite.__init__(self)
        # 图片
        self.image = pygame.image.load(image_path + "bullet01.png") # 20 * 30    
        # h获取矩形对象
        self.rect = self.image.get_rect()
        self.rect.topleft = [x + 94 / 2 - 20 / 2 , y + 30]

        # 窗口
        self.screen = screen
        # 速度
        self.speed = 10

    def update(self):
        # 修改子弹坐标
        self.rect.top += self.speed
        # 如果子弹移出屏幕，则小辉子弹对象
        if self.rect.top > 852:
            self.kill()



# 创建背景音乐
class GameSound(object):
    def __init__(self) -> None:
        pygame.mixer.init() # 音乐模块初始化
        pygame.mixer.music.load(image_path + "sound.ogg") # 加载音乐
        pygame.mixer.music.set_volume(0.5)  # 设置音量

    def playBackgroundMusic(self):
        pygame.mixer.music.play(-1)  # 开始播放音乐  -1无限循环   2两遍


# 完成整个程序的控制
def main():

    # 播放音乐
    sound = GameSound()
    sound.playBackgroundMusic()

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
