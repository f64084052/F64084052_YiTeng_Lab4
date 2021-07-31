import pygame
import os
import math

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        # 取得敵人的位置
        x1, y1 = enemy.get_pos()
        # 算出敵人跟塔的距離
        distance = math.sqrt((x1 - self.center[0])**2 + (y1 - self.center[1])**2) 
        # 如果距離比半徑大，回傳False
        if(distance > self.radius):
            return False
        else:
            return True
        

    def draw_transparent(self, win):
        # 建立一個平面，長寬皆為2倍半徑(正方形)
        transparent_surface = pygame.Surface((2*self.radius, 2*self.radius), pygame.SRCALPHA)
        # 透明度
        transparency = 80
        # (192, 192, 192)為RGB，代表灰色
        # 以平面的中心為圓心在平面上畫圓
        pygame.draw.circle(transparent_surface, (192, 192, 192, transparency), (self.radius, self.radius), self.radius)
        # 將平面疊到win上，平面的座標為塔中心左上的頂點
        win.blit(transparent_surface, (self.center[0]-self.radius, self.center[1]-self.radius))


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = False  # 塔的初始狀態是沒有被滑鼠點到
        self.type = "tower"       

    def is_cool_down(self):
        # 如果count沒數到60，代表塔還在冷卻中
        if(self.cd_count < self.cd_max_count):
            self.cd_count += 1
            return True
        else:
            self.cd_count = 0
            return False
            

    def attack(self, enemy_group):
        # 如果塔已經冷卻完畢，就檢查第一個敵人有沒有在塔的攻擊範圍內，如果有就攻擊
        if(self.is_cool_down() == False):
            for en in enemy_group.get():
                if(self.range_circle.collide(en) == True):
                    en.get_hurt(self.damage)
                    break
        

    def is_clicked(self, x, y):
        # 如果滑鼠點擊的區域在塔的長寬範圍裡，就代表點到塔了
        if((x, y) >= (self.rect.x, self.rect.y) and (x, y) <= self.rect.bottomright):
            return True
        else:
            return False

    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

