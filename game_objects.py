from base import *


class Projectile:
    def __init__(self, pos, vel, r, img_path1='', img_path2='', max_time=0, switch_speed=10):
        self.pos = pos
        self.vel = vel
        self.r = r
        self.timer = 0
        self.switch_speed = switch_speed
        if isinstance(img_path1, str) and img_path1:
            self.img1 = load_img(img_path1)
        elif img_path1:
            self.img1 = img_path1
        if isinstance(img_path2, str) and img_path2:
            self.img2 = load_img(img_path2)
        elif img_path2:
            self.img2 = img_path2
        if max_time:
            self.max_time = max_time

    def update_vel(self, new_vel):
        self.vel = new_vel

    def update(self):
        self.pos = (self.pos[0] + self.vel[0], self.pos[1] + self.vel[1])
        self.timer += 1

    def is_too_long(self):
        if hasattr(self, 'max_time'):
            if self.timer == self.max_time:
                return True
        return False

    def is_too_far(self):
        x = self.pos[0]
        y = self.pos[1]
        osx = 1000
        osy = 300
        if x < -osx or x > window_size[0] + osx or y < -osy or y > window_size[1] + osy:
            return True
        else:
            return False

    def intersect(self, pos, r):
        d = math.sqrt((self.pos[0] - pos[0])**2 + (self.pos[1] - pos[1])**2)
        return d < r + self.r

    def draw(self):
        draw_p = (math.floor(self.pos[0]), math.floor(self.pos[1]))
        img_p = (math.floor(self.pos[0] - self.r), math.floor(self.pos[1] - self.r))
        if hasattr(self, 'img2'):
            if (self.timer // self.switch_speed) % 2 == 0:
                window.blit(self.img1, img_p)
            else:
                window.blit(self.img2, img_p)
        elif hasattr(self, 'img1'):
            window.blit(self.img1, img_p)
        else:
            pygame.draw.circle(window, (255, 0, 0), draw_p, self.r)


class Structure:
    def __init__(self, rect, plat):
        self.rect = rect
        self.x = rect[0]
        self.y = rect[1]
        self.wid = rect[2]
        self.hei = rect[3]
        self.plat = plat

    def draw(self):
        pass
        # pygame.draw.rect(window, (100, 0, 0), (self.x, self.y, self.wid, self.hei / 2))d

    def intersect(self, pos):
        x = pos[0]
        y = pos[1]
        if x in range(self.x, self.x + self.wid) and y in range(self.y, self.y + self.hei):
            return True
        return False

    def is_in_line(self, x):
        if x in range(self.x, self.x + self.wid):
            return True
        return False

    def below(self, pos):
        x = pos[0]
        y = pos[1]
        if (self.y + (tile_len//2) > y > self.y) and (self.x <= x <= self.x + self.wid):
            return True
        return False
