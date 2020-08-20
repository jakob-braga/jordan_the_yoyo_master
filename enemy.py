from game_objects import *


class Enemy:
    def __init__(self, r, pos, sprite_folder):
        self.r = r
        self.pos = pos
        self.speed = -2
        self.fall_timer = 0
        self.timer = 0
        self.health = 1
        self.dead = False
        self.can_hit = True
        self.cool_down_timer = 0

        self.falling = False

        self.projectiles = []

        self.sprite_folder = sprite_folder
        self.walk_l_img_0 = load_img('./images/enemies/' + self.sprite_folder + '/walk_0.png')
        self.walk_l_img_1 = load_img('./images/enemies/' + self.sprite_folder + '/walk_1.png')
        self.walk_r_img_0 = pygame.transform.flip(self.walk_l_img_0, True, False)
        self.walk_r_img_1 = pygame.transform.flip(self.walk_l_img_1, True, False)

    def move(self, lof):
        pos_check = self.pos[0] + self.speed
        for struct in lof:
            if struct.intersect((pos_check + self.r, self.pos[1])) and self.speed > 0:
                self.speed *= -1
            elif struct.intersect((pos_check - self.r, self.pos[1])) and self.speed < 0:
                self.speed *= -1
        self.pos = d_vec(self.pos, self.speed, 0)

    def intersect(self, pos, r):
        d = math.sqrt((self.pos[0] - pos[0])**2 + (self.pos[1] - pos[1])**2)
        return d < r + self.r

    def draw(self):
        draw_p = (math.floor(self.pos[0] - self.r), math.floor(self.pos[1] - self.r))
        if self.speed < 0:
            if (self.timer//10) % 2 == 0:
                window.blit(self.walk_l_img_0, draw_p)
            else:
                window.blit(self.walk_l_img_1, draw_p)
        else:
            if (self.timer//10) % 2 == 0:
                window.blit(self.walk_r_img_0, draw_p)
            else:
                window.blit(self.walk_r_img_1, draw_p)

        for proj in self.projectiles:
            proj.draw()

    def hit(self):
        self.health = 0


class GEnemy(Enemy):

    def fall_check(self, lof):
        b1 = (self.pos[0] - self.r, self.pos[1] + self.r + 5)
        b2 = (self.pos[0] + self.r, self.pos[1] + self.r + 5)
        for floor in lof:
            if (floor.intersect(b1) or floor.intersect(b2)) and self.pos[1] + self.r <= floor.y:
                return False
        return True

    def fall(self, lof):
        acc = 1/20
        dy = acc*(self.fall_timer**2)
        if dy > 50:
            dy = 50
        b1 = (self.pos[0] - self.r, self.pos[1] + self.r + dy + 5)
        b2 = (self.pos[0] + self.r, self.pos[1] + self.r + dy + 5)
        for struct in lof:
            if struct.below(b1) or struct.below(b2):
                self.pos = (self.pos[0], struct.y - self.r)
                self.falling = False
                self.fall_timer = 0
                break
        if self.falling:
            self.pos = d_vec(self.pos, 0, dy)
        self.fall_timer += 1/3

    def manage(self, p_pos, lof):
        if self.pos[1] > window_size[1] + 200 or self.pos[0] < -200:
            self.health = 0
            self.dead = True
        self.move(lof)
        self.falling = self.fall_check(lof)
        if self.falling:
            self.fall(lof)
        self.timer += 1


class FEnemy(Enemy):
    def manage(self, p_pos, lof):
        if self.pos[1] > window_size[1] + 200 or self.pos[0] < -200:
            self.health = 0
            self.dead = True
        self.move(lof)
        self.timer += 1
        if self.cool_down_timer == 120:
            self.drop_fire()
            self.cool_down_timer = 0
        self.cool_down_timer += 1
        for p in self.projectiles:
            p.update()

    def drop_fire(self):
        p1 = './images/enemies/mini_fireball_0.png'
        p2 = './images/enemies/mini_fireball_1.png'
        vel = (0, 5)
        r = int(scale(1/2))
        self.projectiles.append(Projectile(self.pos, vel, r, img_path1=p1, img_path2=p2))
