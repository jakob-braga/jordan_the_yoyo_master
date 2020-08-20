from enemy import *


class Yoyo:
    def __init__(self):
        self.pos = (0, 0)
        self.r = 15
        self.active = False
        self.timer = 0
        self.out_time = 12
        self.dest = (0, 0)
        self.out_vel = (0, 0)

    def set(self, pos, dest):
        self.active = True
        self.pos = pos
        self.dest = dest
        self.out_vel = scale_vec(unit_vector(pos, dest), 20)

    def move(self, vel=()):
        if vel:
            self.pos = (self.pos[0] + vel[0], self.pos[1] + vel[1])
        else:
            self.pos = (self.pos[0] + self.out_vel[0], self.pos[1] + self.out_vel[1])
        self.timer += 1

    def intersect(self, pos, r=0):
        if math.dist(pos, self.pos) < r + self.r:
            return True

    def come_back(self, p_pos):
        vel = scale_vec(unit_vector(self.pos, p_pos), 20)
        self.move(vel=vel)
        if math.dist(self.pos, p_pos) < 20:
            self.active = False
            self.timer = 0

    def yoyo(self, p_cent):
        if self.timer < self.out_time:
            self.move()
        else:
            self.come_back(p_cent)

    def draw(self):
        if self.active:
            new_pos = (math.floor(self.pos[0]), math.floor(self.pos[1]))
            pygame.draw.circle(window, (100, 0, 100), new_pos, self.r)


class Player:
    def __init__(self):
        self.r = scale(1/2)
        self.y = scale(8)
        self.pos = (mid_x, self.y)
        self.width = tile_len
        self.jumping = False
        self.falling = False
        self.right = True
        self.can_move_right = True
        self.can_move_left = True
        self.left = False
        self.moving = True
        self.yoyo = Yoyo()
        self.timer = 0
        self.jump_timer = 0
        self.health = 3
        self.is_hit = False
        self.is_hit_timer = 0

        # sprites

        p = './images/char_sprites/'

        self.right_sprites = [
            load_img(p + 'right_0.png'),
            load_img(p + 'right_1.png'),
            load_img(p + 'right_2.png'),
            load_img(p + 'right_1.png')
        ]

        self.left_sprites = [
            pygame.transform.flip(self.right_sprites[0], True, False),
            pygame.transform.flip(self.right_sprites[1], True, False),
            pygame.transform.flip(self.right_sprites[2], True, False),
            pygame.transform.flip(self.right_sprites[3], True, False)
        ]

        self.still_r_sprite = load_img(p + 'still.png')

        self.still_l_sprite = pygame.transform.flip(self.still_r_sprite, True, False)

        self.jump_r_sprite = load_img(p + 'jump.png')

        self.jump_l_sprite = pygame.transform.flip(self.jump_r_sprite, True, False)

        self.right_yoyo_sprites = [
            load_img(p + 'right_0.png'),
            load_img(p + 'right_yoyo_1.png'),
            load_img(p + 'right_yoyo_2.png'),
            load_img(p + 'right_yoyo_1.png')
        ]

        self.left_yoyo_sprites = [
            pygame.transform.flip(self.right_yoyo_sprites[0], True, False),
            pygame.transform.flip(self.right_yoyo_sprites[1], True, False),
            pygame.transform.flip(self.right_yoyo_sprites[2], True, False),
            pygame.transform.flip(self.right_yoyo_sprites[3], True, False)
        ]

        self.still_yoyo_r_sprite = load_img(p + 'still_yoyo.png')

        self.still_yoyo_l_sprite = pygame.transform.flip(self.still_yoyo_r_sprite, True, False)

        self.jump_yoyo_r_sprite = load_img(p + 'jump_yoyo.png')

        self.jump_yoyo_l_sprite = pygame.transform.flip(self.jump_yoyo_r_sprite, True, False)

        self.hit_r_sprite = load_img(p + 'hit.png')

        self.health_img = load_img('./images/health.png')

    def intersect(self, p, r=0):
        lower = (mid_x, self.y - tile_len / 2)
        upper = (mid_x, self.y - (tile_len * 3 / 2))
        if math.dist(p, lower) < r + self.r:
            return True
        if math.dist(p, upper) < r + self.r:
            return True
        return False

    def move_check(self, los, vel):
        self.falling = self.fall_check(los)
        self.can_move_left = True
        self.can_move_right = True
        pxr = mid_x + self.r + vel
        pxl = mid_x - self.r - vel
        for s in los:
            if s.intersect((pxr, self.y-5)) or s.intersect((pxr, self.y - self.r*4)) or s.intersect((pxr, self.y - self.r*2)):
                if not s.plat:
                    self.can_move_right = False
                    return
            if s.intersect((pxl, self.y-5)) or s.intersect((pxl, self.y - self.r*4)) or s.intersect((pxr, self.y - self.r*2)):
                if not s.plat:
                    self.can_move_left = False
                    return
        if 1 < self.is_hit_timer < 40:
            self.can_move_left = False
            self.can_move_right = False

    def get_upper_pos(self):
        upper_p = (mid_x, self.y - (tile_len * 3/2))
        return upper_p

    def jump(self, lof, fall=False, drop=False):
        if fall:
            v0 = 0
        elif drop:
            v0 = 1
        else:
            v0 = -3
        jt = self.jump_timer
        dy = math.floor((v0 * jt) + (jt ** 2)/4)
        player_b1 = ((mid_x - tile_len/2), self.y + dy)
        player_b2 = (mid_x - tile_len/2 + self.width, self.y + dy)
        for floor in lof:
            if (floor.intersect(player_b1) or floor.intersect(player_b2)) and dy > 0 and self.y <= floor.y:
                self.jumping = False
                self.falling = False
                self.y = floor.y
                self.jump_timer = 0
        if self.jumping or self.falling:
            self.y += dy
            self.jump_timer += 1 / 3
        else:
            self.jump_timer = 0

    def drop(self, lof):
        if not self.falling or not self.jumping:
            player_b1 = (mid_x - tile_len/2, self.y + 6)
            player_b2 = (mid_x - tile_len/2 + self.width, self.y + 6)
            for floor in lof:
                if (floor.intersect(player_b1) or floor.intersect(player_b2)) and self.y <= floor.y:
                    if floor.plat:
                        self.y += 2
                        self.jump(lof, drop=True)

    def fall_check(self, lof):
        if not self.jumping:
            player_b1 = (mid_x - (tile_len / 2), self.y + 5)
            player_b2 = ((mid_x - (tile_len / 2)) + self.width, self.y + 5)
            for floor in lof:
                if (floor.intersect(player_b1) or floor.intersect(player_b2)) and self.y <= floor.y:
                    return False
            return True

    def hit(self):
        self.is_hit = True

    def hit_update(self):
        self.is_hit_timer += 1
        if self.is_hit_timer == 110:
            self.is_hit = False
            self.is_hit_timer = 0
        elif self.is_hit_timer == 2:
            self.health -= 1

    def draw_health(self):
        for i in range(0, self.health):
            window.blit(self.health_img, (scale(1/4) + scale(1)*i, scale(1/4)))

    def draw(self):
        if self.timer == 22:
            self.timer = -6

        it = 6  # initial timer
        s_time = 7  # timer interval for sprite
        x = mid_x - tile_len / 2
        y = self.y - tile_len*2 + 5  # minor correction with the + 5
        p = (x, y)
        index = (self.timer + it) // s_time

        # pygame.draw.circle(window, (0, 150, 0), (player_x, self.y - 8 * 5), self.r)
        # pygame.draw.circle(window, (0, 150, 0), (player_x, self.y - 24 * 5), self.r)
        if 1 < self.is_hit_timer < 40:
            window.blit(self.hit_r_sprite, p)
        elif self.is_hit_timer//5 % 2 == 0:
            if self.yoyo.active:
                if self.yoyo.dest[0] >= mid_x:
                    if self.jumping or self.falling:
                        window.blit(self.jump_yoyo_r_sprite, p)
                        self.timer = 0
                    elif self.moving:
                        window.blit(self.right_yoyo_sprites[index], p)
                    else:
                        window.blit(self.still_yoyo_r_sprite, p)
                        self.timer = 0
                else:
                    if self.jumping or self.falling:
                        window.blit(self.jump_yoyo_l_sprite, p)
                        self.timer = 0
                    elif self.moving:
                        window.blit(self.left_yoyo_sprites[index], p)
                    else:
                        window.blit(self.still_yoyo_l_sprite, p)
                        self.timer = 0
            else:
                if self.right:
                    if self.jumping or self.falling:
                        window.blit(self.jump_r_sprite, p)
                        self.timer = 0
                    elif self.moving:
                        window.blit(self.right_sprites[index], p)
                    else:
                        window.blit(self.still_r_sprite, p)
                        self.timer = 0
                else:
                    if self.jumping or self.falling:
                        window.blit(self.jump_l_sprite, p)
                        self.timer = 0
                    elif self.moving:
                        window.blit(self.left_sprites[index], p)
                    else:
                        window.blit(self.still_l_sprite, p)
                        self.timer = 0

        self.timer += 1

        self.draw_health()
