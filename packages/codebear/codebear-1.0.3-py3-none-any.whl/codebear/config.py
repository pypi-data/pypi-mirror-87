import random

import pygame
from .exception import *
import math
import copy
from threading import Thread


class BackGround():
    def __init__(self, screen):
        '''

        :param screen: 窗口对象  Surface
        '''
        # if
        self.screen = screen
        self.image = None
        self.image2 = None

        self.is_change = False
        self.is_vertical = False
        self.moveSpeed = 0
        #
        self.img_width = None
        self.image1x = 0
        self.image2x = 0
        self.image1y = 0
        self.image2y = 0

        self.img_width = None

    def load_image(self, *args):
        if len(args) == 1:
            try:
                image = pygame.image.load(args[0])
                self.image = image
                self.image2 = self.image
                self.rect = image.get_rect()
                self.img_width = self.rect[2]
                self.image2x = self.rect[2]
            except:
                e = BackGround_Error("错误的图片加载路径或者这不是一张图片")
                raise e
        else:
            e = BackGround_Error("图片必须至少有一张最多两张")
            raise e

    def update(self, is_change=False, move_speed=1, vertical=False):
        self.is_change = is_change
        self.is_vertical = vertical
        self.moveSpeed = move_speed
        if self.is_change:
            if self.is_vertical:
                # 竖着
                pass
            else:
                # 横着
                self.image1x = self.image1x - self.moveSpeed
                self.image2x = self.image2x - self.moveSpeed
                if self.image1x <= -self.img_width:
                    self.image1x = self.img_width
                if self.image2x <= -self.img_width:
                    self.image2x = self.img_width
                self.screen.blit(self.image, (self.image1x, self.image1y))
                self.screen.blit(self.image2, (self.image2x, self.image2y))
        if not self.is_change:
            self.screen.blit(self.image, (self.image1x, self.image1y))


class Action():
    action = {}
    '''
    Action(): 人物 动作类
. getImages(self, images, rate)    加载图片对象Surface列表初始化动作类    参数：images 图像列表  rate 越大 速度越慢
. image_next(self): 获取下一个人物的动作

. set_jump(self, speed)        设置跳跃高度 不是像素而是内部简单的算法 数值越高 跳跃的越高
. jump(self, pos, floor)     获取跳跃时的坐标返回一个 坐标列表  pos 当前的坐标  floor ：开始跳跃的高度
. set_speed(self, speed)     设置人物移动的速度       参数 speed 移动速度
. move(self, pos, face="left")  移动角色  参数  pos坐标想 x,y 的值 朝某个方向移动  up down left right


Action.distance(pos1, pos2, distance1_center=5,distance2_center=5 ) 检测两个角色之间的距离 需要参数 角色1 的坐标，角色2的坐标
可选参数 角色1 图片左上角到圆心的距离  默认为5
可选参数 角色2 图片左上角到圆心的距离  默认为5
    '''

    def __init__(self):
        pass

        # 未设置前为空
        self.blood = None

        self.image = None
        self.images = None

        self.long = None
        self.select = 0
        self.flag = 0
        self.rate = 0
        # 跳跃
        self.height = 0
        self.speed_up_flag = 0

        # 移动
        self.speed = 0

        # role 属性
        self.rolex = None
        self.roley = None
        self.roleImage = None
        self.rolewidth = None
        self.roleheight = None
        self.__is_alive = None

    def getImages(self, images, rate):
        self.images = images
        self.long = len(images)
        self.rate = rate
        pass

    def set_attribute(self, blood):
        pass

    def image_next(self):
        self.image = self.images[self.select]

        self.flag += 1
        if self.flag >= self.rate:
            self.select += 1
            self.flag = 0
            if self.select >= self.long - 1:
                self.select = 0

        return self.image

    #   跳跃动作
    def set_jump(self, speed):
        self.speed_up_flag = -speed
        self.speed_up = self.speed_up_flag

    def jump(self, pos, floor):
        x = pos[0]
        y = pos[1]
        try:
            if self.speed_up < 0:
                pass
        except:
            Action_Error("没有给角色设置起跳高度")
        if self.speed_up < 0:
            self.speed_up += 0.6
        elif self.speed_up > 0:
            self.speed_up += 0.9
        y += self.speed_up
        if y > floor:
            y = floor
            self.speed_up = self.speed_up_flag

        pos = [x, y]
        return pos

    def set_speed(self, speed):
        self.speed = speed

    def move(self, pos, face="left"):
        x = pos[0]
        y = pos[1]
        if face == "left":
            x -= self.speed
            return [x, y]
        if face == "right":
            x += self.speed
            return [x, y]

        if face == "up":
            y -= self.speed
            return [x, y]
        if face == "down":
            y += self.speed
            return [x, y]

    def mange_role(self, x, y, img):
        self.rolex = x
        self.roley = y
        self.roleImage = img

    def setAlive(self, value):
        if type(value) == bool:
            # print("设置生命成功")
            self.__is_alive = value

    def getAlive(self):

        return self.__is_alive

    @staticmethod
    def distance(pos1, pos2, distance1_center=5, distance2_center=5):
        x1 = pos1[0] + distance1_center
        y1 = pos1[1] + distance1_center
        x2 = pos2[0] + distance2_center
        y2 = pos2[1] + distance2_center

        a = x1 - x2
        b = y1 - y2

        return math.sqrt(a * a + b * b)


class Role():
    def __init__(self, image, x, y, action=False, rate=5):
        self.rate = rate
        self.image = image
        self.action = action
        if action == True:
            self.a = Action()
            self.a.getImages(image, self.rate)
        self.x = x
        self.y = y
        self.__is_alive = True
        self.__blood = 0
        self.__speed = 1
        self.mydict_list = []

    def setBlood(self, blood):
        if type(blood) != int:
            raise Role_Error("设置的血量必须为int类型")
        self.__blood = blood

    def getBlood(self):
        return self.__blood

    def update(self):
        self.image = self.a.image_next()

    def get_pos(self):
        return [self.x, self.y]

    def setSpeed(self, speed):
        self.__speed = speed

    def getSpeed(self):
        return self.__speed

    def setAlive(self, value):
        if type(value) == bool:
            # print("设置生命成功")
            self.__is_alive = value

    def getAlive(self):
        return self.__is_alive

    def move(self, face="left"):
        faces = ["down", "up", "right", "left"]
        if face not in faces:
            raise Role_Error("必须输入一个正确的方向{}".format(faces))

        if face == "left":
            self.x -= self.__speed
        if face == "right":
            self.x += self.__speed

        if face == "up":
            self.y -= self.__speed
        if face == "down":
            self.y += self.__speed

    def setJumpHeight(self, speed=5):
        if type(speed) != int or speed < 0:
            raise Role_Error("速度必须是int类型的正数")
        self.a.set_jump(speed=speed)

    def jump(self, floor):
        try:
            if self.a.speed_up < 0:
                pass
            self.x, self.y = self.a.jump([self.x, self.y], floor=floor)
        except:
            raise Action_Error("没有给角色设置起跳高度,需要使用 setJumpHeight() 方法设定")

    def kill(self):
        self.x = -1000
        self.y = -1000
        del self

    def distance(self, pos, center_d2=5):
        try:
            x, y = pos[0], pos[1]
        except:
            raise Action_Error("被检测碰撞元素的坐标不是期望的类型 我们想要[x,y]的坐标格式")
        pos = (x, y)
        xx, yy, width, height = self.image.get_rect()
        center_d = ((width // 2) + (height // 2)) // 2
        value = Action.distance(self.get_pos(), pos, center_d, center_d2)
        # print(value)
        return value

    def setMyDefine(self, **kwargs):
        d = kwargs
        for i in self.mydict_list:
            if i.keys() == d.keys():
                self.mydict_list.remove(i)
        self.mydict_list.append(d)

    def getMyDefine(self, key):
        for i in self.mydict_list:
            for k, v in i.items():
                if key == k:
                    return v

    @staticmethod
    def deepcopy(list, size):
        newlist = []
        for img in list:
            s = copy.deepcopy(img)
            print(s)
        return newlist

    @staticmethod
    def thload(list):
        new_list = []
        for i in list:
            img = pygame.image.load(i)
            new_list.append(img)
        return new_list

    @staticmethod
    def tload(list):
        t = Thread(target=Role.thload, args=(list))


class Tload(Thread):
    def __init__(self,list):
        super().__init__()
        self.__list = list
        self.isok = False
        self.__imglist = []
        # print("初始化")
    def run(self):
        print("启动了")
        for i in self.__list:
            img = pygame.image.load(i)
            self.__imglist.append(img)
            # print(i,"完成了")
        self.isok = True
        print( "oko完成了",len(self.__imglist))

    def getImageList(self):
        return self.__imglist

    def isOk(self):
        return self.isok


class Fall():

    def __init__(self, img, milliseconds=500):
        # if type(img) == pygame.Surface:
        self.image = pygame.image.load(img)
        # else:
        #     # path = CLASS_PATH[0] + "\\codebear\\image\\snow.png"
        #     # self.image = pygame.image.load(path)
        #     raise Fall_Error("下飘落物体，不被识别的图像，需要一个Surface对象")
        # self.speed_down = [1, 5]
        # self.speed_x = [-5, -1]
        # self.x_range = x_range
        # self.snow_list = []
        # for i in range(count):
        #     img = self.image
        #     x = random.uniform(0, x_range)
        #     y = random.uniform(-500, 0)
        #     speedx = random.uniform(self.speed_x[0], self.speed_x[1])
        #     speedd = random.uniform(self.speed_down[0], self.speed_down[1])
        #     s = {img: [x, y, speedx, speedd]}
        #     self.snow_list.append(s)
        self.__fall_list = []
        self.__create_event = pygame.USEREVENT - 15
        # print( self.__create_event)
        pygame.time.set_timer(self.__create_event, milliseconds)

    # 获取飘落物事件
    def getEvent(self):
        return self.__create_event

    # 创建指定数量飘落物体
    def create(self, pos, crosswise_speed=-1, vertical_speed=1):
        x = pos[0]
        y = pos[1]
        snow = {self.image: [[x, y], crosswise_speed, vertical_speed]}
        self.__fall_list.append(snow)

    def descent(self, screen):
        # for s in self.snow_list:
        #     for k, v in s.items():
        #         if v[2] < 0:
        #             v[0] += v[2]
        #         if v[2] > 0:
        #             v[0] -= v[2]
        #         v[1] += v[3]
        #         if v[1] > 2000:
        #             v[1] = random.uniform(-100, 10)
        #         print(v[0], v[1])
        #         if v[0] < -30:
        #             v[0] = random.uniform(0, self.x_range)
        #         screen.blit(k, (v[0], v[1]))
        for i in self.__fall_list:
            for k, v in i.items():
                screen.blit(k, v[0])
                v[0][0] += v[1]
                v[0][1] += v[2]
                if v[0][0] > 5000 or v[0][0] < -1000 or v[0][1] > 3000 or v[0][1] < -1000:
                    self.__fall_list.remove(i)
        # print(len(self.__fall_list))
