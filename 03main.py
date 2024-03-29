from multiprocessing import managers
import random
from select import select
import pygame
from pygame.constants import *
import time


image_path = "./data/images/"
music_path = "./data/music/"


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

        if self.rect.right > 480:
            self.direction = "left"
        elif self.rect.right < 95:
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
        pygame.mixer.music.load(music_path + "sound.ogg") # 加载音乐
        pygame.mixer.music.set_volume(0.5)  # 设置音量

        self.__bomb = pygame.mixer.Sound(music_path + "bomb.wav") 

    def playBackgroundMusic(self):
        pygame.mixer.music.play(-1)  # 开始播放音乐  -1无限循环   2两遍
    
    def playBombSound(self):
        pygame.mixer.Sound.play(self.__bomb)  # 爆炸音乐


# 碰撞类
class Bomb(object):
    # 初始化爆炸
    def __init__(self, screen, type):
        self.screen = screen

        if type == "enemy":
            # 加载爆炸资源
            self.mImages = [
                pygame.image.load(image_path + "enemyboom" + str(v) + ".png") for v in range(1,5)
            ]
        else:
            self.mImages = [
                pygame.image.load(image_path + "heroboom" + str(v) + ".png") for v in range(1,5)
            ]

        # 设置当前爆炸播放缩阴
        self.mIndex = 0
        # 爆炸位置
        self.mPos = [0,0]
        # 是否可见
        self.mVisible = False

    def action(self, rect):
        # 触发爆炸方法draw

        #爆炸坐标
        self.mPos[0] = rect.left
        self.mPos[1] = rect.top
        # 打开爆炸的开关
        self.mVisible = True

    # 绘制爆炸
    def draw(self):
        if not self.mVisible:
            return
        self.screen.blit(self.mImages[self.mIndex], (self.mPos[0], self.mPos[1]))
        self.mIndex += 1
        if self.mIndex >= len(self.mImages):
            # 如果下表已经到最后，代表爆炸结束
            # 下标重置 mVisible重置
            self.mIndex = 0
            self.mVisible = False

class Manager(object):
    def __init__(self):
        # 创建窗口
        self.screen = pygame.display.set_mode((480,852),0,32)
        # 创建图片背景
        self.background = pygame.image.load(image_path + "beijing01.png")
        # 初始化一个玩家装精灵的group
        self.players = pygame.sprite.Group()
        # 初始化一个装敌机精灵的group
        self.enemys = pygame.sprite.Group()
        # 初始化一个玩家爆炸的对象
        self.players_bomb = Bomb(self.screen, "player")
        # 初始化一个敌机爆炸的对象
        self.enemys_bomb = Bomb(self.screen, "enemy")
        # 初始化一个声音播放的对象
        self.sound = GameSound()

    def exit(self):
        """退出程序"""
        print("exit")
        pygame.quit()
        exit()

    def new_player(self):
        """创建飞机对象，添加到玩家的组"""
        player = HeroPlane(self.screen)
        self.players.add(player)

    def new_enemy(self):
        """创建敌机的对象，添加到敌机的组"""
        enemy = EnemyPlane(self.screen)
        self.enemys.add(enemy)

    def main(self):
        # 播放背景音乐
        self.sound.playBackgroundMusic()
        # 创建一个玩家
        self.new_player()
        # 创建一个敌机
        self.new_enemy()
        
        # 让屏幕一直显示在窗口
        while True:
            # 3. 将背景图片贴到窗口中
            self.screen.blit(self.background, (0,0))
            # 获取事件
            for event in pygame.event.get():
                # 判断事件类型
                if event.type == pygame.QUIT:
                    self.exit()

            # 调用爆炸的对象
            self.players_bomb.draw()
            self.enemys_bomb.draw()

            # 判断碰撞
            iscollide = pygame.sprite.groupcollide(self.players, self.enemys, True, True)  # 接收玩家和敌机，都为True时将两个都消除
            if iscollide:
                items = list(iscollide.items())[0]
                print(items)
                x = items[0]
                y = items[1][0] 
                # 玩家爆炸图片
                self.players_bomb.action(x.rect)
                # 敌机爆炸图片
                self.enemys_bomb.action(x.rect)
                # 爆炸声音
                self.sound.playBombSound()


            # 玩家飞机子弹显示
            self.players.update()
            # 敌机和子弹显示
            self.enemys.update()
            # 刷新窗口内容
            pygame.display.update()
            time.sleep(0.01)


# 主函数
if __name__ == '__main__':
    manager = Manager()
    manager.main()
