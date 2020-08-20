from player import *


class Masami:
    def __init__(self, x):
        self.pos = (x, scale(7))
        self.health = 3
        self.dead = False
        self.r = scale(1)
        self.timer = 0
        self.timer_limit = 20
        self.move_set = ['throwing_start', 'skate_start']
        self.move_time = 80

        self.projectiles = []
        self.can_hit = True
        self.hit_timer = 0
        self.hurt = False
        self.post_hurt = False

        # throwing
        self.throwing = False
        self.throw_timer = 0
        self.throws = 0
        self.throw_lim = 3
        self.throw_timer_lim = 40
        self.ball_r = p_scale(7)

        # skating
        self.skating = False
        self.skate_vel = ()
        self.skate_timer = 0
        self.jump_time = 29
        self.go_time = 60

        # falling
        self.dropping = False
        self.drop_timer = 0
        self.drop_time = 30
        self.falling = False
        self.fall_timer = 0

        # explode
        self.fire_r = scale(1/2)

        # sprites

        p = './images/masami/'
        self.left = True
        # left sprites
        self.still_img_l = load_img(p + 'still.png')
        self.to_skate_img_l = load_img(p + 'to_skate.png')
        self.throwing_img_l_0 = load_img(p + 'throwing_0.png')
        self.throwing_img_l_1 = load_img(p + 'throwing_1.png')
        self.skate_img_l = load_img(p + 'skate.png')
        self.skate_flash_img_l = load_img(p + 'skate_flash.png')
        self.fireball_img_l_0 = load_img(p + 'fireball.png')
        self.fireball_img_l_1 = pygame.transform.flip(self.fireball_img_l_0, False, True)
        # right sprites
        self.still_img_r = pygame.transform.flip(self.still_img_l, True, False)
        self.to_skate_img_r = pygame.transform.flip(self.to_skate_img_l, True, False)
        self.throwing_img_r_0 = pygame.transform.flip(self.throwing_img_l_0, True, False)
        self.throwing_img_r_1 = pygame.transform.flip(self.throwing_img_l_1, True, False)
        self.skate_img_r = pygame.transform.flip(self.skate_img_l, True, False)
        self.skate_flash_img_r = pygame.transform.flip(self.skate_flash_img_l, True, False)
        self.fireball_img_r_0 = pygame.transform.flip(self.fireball_img_l_0, True, False)
        self.fireball_img_r_1 = pygame.transform.flip(self.fireball_img_l_1, True, False)
        # other
        self.fireball_img_d_0 = pygame.transform.rotate(self.fireball_img_l_0, 90)
        self.fireball_img_d_1 = pygame.transform.flip(self.fireball_img_d_0, True, False)
        self.dropping_img = load_img(p + 'dropping.png')
        self.falling_img = load_img(p + 'falling.png')
        self.ball_img = load_img(p + 'basketball.png')
        self.hurt_img = load_img(p + 'hurt.png')
        self.mini_fireball_img_0 = load_img(p + 'mini_fireball.png')
        self.mini_fireball_img_1 = pygame.transform.flip(self.mini_fireball_img_0, True, False)
        self.fire_eyes_r_0 = load_img(p + 'fire_eyes_0.png')
        self.fire_eyes_r_1 = load_img(p + 'fire_eyes_1.png')
        self.fire_eyes_l_0 = pygame.transform.flip(self.fire_eyes_r_0, True, False)
        self.fire_eyes_l_1 = pygame.transform.flip(self.fire_eyes_r_1, True, False)

    # throwing

    def throwing_start(self):
        self.throwing = True

    def throw_ball(self, p_pos):
        vel1 = unit_vector(self.pos, p_pos)
        vel2 = scale_vec(vel1, 5)
        self.projectiles.append(Projectile(self.pos, vel2, self.ball_r, 'images/masami/basketball.png'))
        self.throws += 1

    # skating

    def skate_start(self):
        self.skating = True

    def skate_to(self):
        if (self.skate_vel[0] >= 0 and self.pos[0] > mid_x) or (self.skate_vel[0] < 0 and self.pos[0] < mid_x):
            self.skating = False
            self.dropping = True
            self.skate_timer = 0
            self.drop_timer = 0
        else:
            self.pos = (self.pos[0] + self.skate_vel[0], self.pos[1] + self.skate_vel[1])

    # falling

    def fall(self, lof):
        acc = 1/3
        dy = acc * self.fall_timer ** 2
        if dy > 20:
            dy = 20
        check_pos = (self.pos[0], self.pos[1] + dy + self.r)
        for floor in lof:
            if floor.below(check_pos) and not floor.plat:
                self.pos = (self.pos[0], floor.y - self.r)
                self.falling = False
                self.can_hit = True
                self.fall_timer = 0
        if self.falling:
            self.pos = (self.pos[0], self.pos[1] + dy)
            self.fall_timer += 1
        if self.pos[1] > window_size[1] + 200:
            self.health = 0

    # explode

    def explode(self):
        vel = (-6, 0)
        a = 0
        while a <= 360:
            self.projectiles.append(
                Projectile(self.pos, rotate_vec(vel, a), self.fire_r, img_path1=self.mini_fireball_img_0,
                           img_path2=self.mini_fireball_img_1, max_time=90))
            a += 45

    # main

    def hit(self):
        self.hurt = True
        self.can_hit = False
        self.throwing = False
        self.throws = 0
        self.throw_timer = 0
        self.timer = 0
        if self.health == 2:
            self.move_time = 35
            self.throw_lim = 4

    def intersect(self, pos, r):
        d = math.sqrt((self.pos[0] - pos[0]) ** 2 + (self.pos[1] - pos[1]) ** 2)
        return d < r + self.r

    def manage(self, p_pos, lof):
        if self.pos[0] >= p_pos[0]:
            self.left = True
        else:
            self.left = False

        # hurt
        if self.hurt:
            if self.left:
                v0x = 2
            else:
                v0x = -2
            v0 = -3
            acc = 1/3
            dy = v0*self.hit_timer + acc*(self.hit_timer ** 2)
            pos_check = (self.pos[0] + v0x, self.pos[1] + dy + self.r)
            for floor in lof:
                if floor.below(pos_check) and not floor.plat:
                    self.pos = (self.pos[0], floor.y - self.r)
                    self.hit_timer = 0
                    self.hurt = False
                    self.post_hurt = True
                    self.health -= 1
            if self.hurt:
                self.pos = (self.pos[0] + v0x, self.pos[1] + dy)
                self.hit_timer += 1/3

        # throwing
        elif self.throwing:
            if self.throw_timer == self.throw_timer_lim // 2:
                self.throw_ball(p_pos)
            elif self.throw_timer == self.throw_timer_lim:
                self.throw_timer = -1
                if self.throws == self.throw_lim:
                    self.throws = 0
                    self.throwing = False
            self.throw_timer += 1

        # skating
        elif self.skating:
            if self.skate_timer == 1:
                self.can_hit = False
                self.skate_vel = scale_vec(unit_vector(self.pos, p_pos), 10)
            if self.skate_timer <= self.jump_time // 2:
                self.pos = (self.pos[0], self.pos[1] - 1)
            elif self.skate_timer <= self.jump_time:
                self.pos = (self.pos[0], self.pos[1] + 1)
            elif self.skate_timer > self.go_time:
                self.skate_to()
            self.skate_timer += 1

        # dropping
        elif self.dropping:
            self.drop_timer += 1
            if self.drop_timer == self.drop_time:
                self.drop_timer = 0
                self.dropping = False
                self.falling = True
                if self.health == 1:
                    self.explode()

        # falling
        elif self.falling:
            self.fall(lof)

        else:
            self.timer += 1
            if self.timer == self.move_time:
                self.timer = 0
                if self.post_hurt:
                    self.post_hurt = False
                    self.can_hit = True
                    self.explode()
                getattr(self, get_random(self.move_set))()

        for ball in self.projectiles:
            ball.update()
            removed = False
            if ball.is_too_far():
                self.projectiles.remove(ball)
                removed = True
            if ball.is_too_long() and not removed:
                self.projectiles.remove(ball)

    def draw(self):
        draw_pos = (self.pos[0] - scale(1), self.pos[1] - scale(1))
        if self.hurt or self.post_hurt or self.health == 0:
            window.blit(self.hurt_img, draw_pos)

        elif self.skating and self.skate_timer > 1:
            draw_left = self.skate_vel[0] <= 0
            if draw_left:
                if self.skate_timer <= self.jump_time:
                    window.blit(self.to_skate_img_l, draw_pos)
                elif self.skate_timer < self.go_time:
                    if (self.skate_timer // 5) % 2 == 0:
                        window.blit(self.skate_img_l, draw_pos)
                    else:
                        window.blit(self.skate_flash_img_l, draw_pos)
                else:
                    if (self.skate_timer//10) % 2 == 0:
                        window.blit(self.fireball_img_l_0, draw_pos)
                    else:
                        window.blit(self.fireball_img_l_1, draw_pos)
                    window.blit(self.skate_img_l, draw_pos)
                if self.health == 1:
                    if self.timer // 10 % 2 == 1:
                        window.blit(self.fire_eyes_l_1, draw_pos)
                    else:
                        window.blit(self.fire_eyes_l_0, draw_pos)
            else:
                if self.skate_timer <= self.jump_time:
                    window.blit(self.to_skate_img_r, draw_pos)
                elif self.skate_timer < self.go_time:
                    if (self.skate_timer // 5) % 2 == 0:
                        window.blit(self.skate_img_r, draw_pos)
                    else:
                        window.blit(self.skate_flash_img_r, draw_pos)
                else:
                    if (self.skate_timer//10) % 2 == 0:
                        window.blit(self.fireball_img_r_0, draw_pos)
                    else:
                        window.blit(self.fireball_img_r_1, draw_pos)
                    window.blit(self.skate_img_r, draw_pos)
                    if self.health == 1:
                        if self.timer // 10 % 2 == 1:
                            window.blit(self.fire_eyes_r_1, draw_pos)
                        else:
                            window.blit(self.fire_eyes_r_0, draw_pos)

        elif self.dropping:
            if (self.drop_timer//10) % 2 == 0:
                window.blit(self.fireball_img_d_1, draw_pos)
            else:
                window.blit(self.fireball_img_d_0, draw_pos)
            window.blit(self.fireball_img_d_0, draw_pos)
            window.blit(self.dropping_img, draw_pos)

        elif self.falling:
            if (self.fall_timer//10) % 2 == 0:
                window.blit(self.fireball_img_d_1, draw_pos)
            else:
                window.blit(self.fireball_img_d_0, draw_pos)
            window.blit(self.skate_img_r, draw_pos)

        elif self.left:
            if self.throwing:
                if self.throw_timer < self.throw_timer_lim // 2:
                    window.blit(self.throwing_img_l_0, draw_pos)
                    if self.health == 1:
                        if self.timer // 10 % 2 == 1:
                            window.blit(self.fire_eyes_l_1, draw_pos)
                        else:
                            window.blit(self.fire_eyes_l_0, draw_pos)
                    in_hand_p = (
                        math.floor(self.pos[0] + scale(1) * 3 / 4 - self.ball_r), math.floor(self.pos[1] - scale(1) * 3 / 4 - self.ball_r)
                    )
                    window.blit(self.ball_img, in_hand_p)
                else:
                    window.blit(self.throwing_img_l_1, draw_pos)
                    if self.health == 1:
                        if self.timer // 10 % 2 == 1:
                            window.blit(self.fire_eyes_l_1, draw_pos)
                        else:
                            window.blit(self.fire_eyes_l_0, draw_pos)
            else:
                window.blit(self.still_img_l, draw_pos)
                if self.health == 1:
                    if self.timer // 10 % 2 == 1:
                        window.blit(self.fire_eyes_l_1, draw_pos)
                    else:
                        window.blit(self.fire_eyes_l_0, draw_pos)

        else:
            if self.throwing:
                if self.throw_timer < self.throw_timer_lim // 2:
                    window.blit(self.throwing_img_r_0, draw_pos)
                    if self.health == 1:
                        if self.timer // 10 % 2 == 1:
                            window.blit(self.fire_eyes_r_1, draw_pos)
                        else:
                            window.blit(self.fire_eyes_r_0, draw_pos)
                    in_hand_p = (
                        math.floor(self.pos[0] - scale(1) * 3 / 4 - self.ball_r), math.floor(self.pos[1] - scale(1) * 3 / 4 - self.ball_r)
                    )
                    window.blit(self.ball_img, in_hand_p)

                else:
                    window.blit(self.throwing_img_r_1, draw_pos)
                    if self.health == 1:
                        if self.timer // 10 % 2 == 1:
                            window.blit(self.fire_eyes_r_1, draw_pos)
                        else:
                            window.blit(self.fire_eyes_r_0, draw_pos)
            else:
                window.blit(self.still_img_r, draw_pos)
                if self.health == 1:
                    if self.timer//10 % 2 == 1:
                        window.blit(self.fire_eyes_r_1, draw_pos)
                    else:
                        window.blit(self.fire_eyes_r_0, draw_pos)

        for ball in self.projectiles:
            ball.draw()
