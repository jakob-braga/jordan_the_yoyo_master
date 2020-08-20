from boss import *


class World:
    def __init__(self):
        self.x = 0
        self.speed = 5
        self.enemy_timer = 0
        self.enemy_timer_2 = 0

        self.masami_triggered = False
        self.masami_cutscene_fin = False

        self.floors = [
            # Structure(r_scale(3, 6, 3, 1), True),  # first platform
            # floors (first floor)
            Structure(r_scale(7, 8, 22, 1), False),
            Structure(r_scale(25, 7, 4, 1), False),  # start of first pyramid
            Structure(r_scale(26, 6, 3, 1), False),
            Structure(r_scale(27, 5, 2, 1), False),
            Structure(r_scale(28, 4, 1, 1), False),  # end of first pyramid
            # 2nd floor
            Structure(r_scale(33, 8, 7, 1), False),
            Structure(r_scale(35, 7, 1, 1), False),  # block
            Structure(r_scale(39, 7, 1, 1), False),  # block
            # 3rd floor
            Structure(r_scale(43, 8, 8, 1), False),
            Structure(r_scale(43, 7, 1, 1), False),  # block
            Structure(r_scale(47, 7, 1, 1), False),  # block
            # forth floor (pillar 1)
            Structure(r_scale(61, 7, 1, 2), False),
            # 5th floor (pillar 2)
            Structure(r_scale(67, 7, 1, 2), False),
            # final floor
            Structure(r_scale(77, 8, 23, 1), False),
            # end floor
            Structure(r_scale(106, 8, 7, 1), False),

            # platforms
            Structure(r_scale(8, 6, 3, 1), True),
            Structure(r_scale(12, 4, 3, 1), True),
            Structure(r_scale(17, 4, 7, 1), True),
            Structure(r_scale(53, 3, 3, 1), True),
            Structure(r_scale(53, 7, 3, 1), True),
            Structure(r_scale(57, 5, 3, 1), True),
            Structure(r_scale(62, 5, 3, 1), True),
            Structure(r_scale(67, 4, 7, 1), True),
            Structure(r_scale(79, 6, 3, 1), True),
            Structure(r_scale(82, 4, 3, 1), True),
            Structure(r_scale(85, 6, 3, 1), True),
            Structure(r_scale(89, 6, 3, 1), True),
            Structure(r_scale(92, 4, 3, 1), True),
            Structure(r_scale(95, 6, 3, 1), True),
            ]

        self.enemies = []

        p = 'images/backgrounds/'
        self.background_1 = load_img(p + 'background_1.png')
        self.background_2 = load_img(p + 'background_2.png')
        self.foreground = load_img(p + 'foreground.png')

    def is_top_struct(self, floor, x):
        for struct in self.floors:
            if struct.is_in_line(x) and struct.y < floor.y:
                return False
        return True

    def enemy_update(self):
        x_spawn = window_size[0] + 200
        if self.enemy_timer >= 120 and self.enemy_timer % 2 == 1 and len(self.enemies) < 15:
            for struct in self.floors:
                if struct.is_in_line(x_spawn) and self.is_top_struct(struct, x_spawn):
                    e_pos = (x_spawn, struct.y - scale(1/2))
                    if self.enemy_near_check(e_pos) and self.x > -scale(85):
                        self.enemies.append(GEnemy(scale(1/2), e_pos, 'cats'))
                        self.enemy_timer = 0
                        return

        if self.enemy_timer_2 > 60:
            rand_chance = random.random()
            if rand_chance < 0.05:
                e_pos = (x_spawn, scale(1))
                if self.enemy_near_check(e_pos) and self.x > -scale(85):
                    self.enemies.append(FEnemy(scale(1/2), e_pos, 'birds'))
                    self.enemy_timer_2 = 0
                    return

        self.enemy_timer += 1
        self.enemy_timer_2 += 1

    def enemy_near_check(self, pos):
        for e in self.enemies:
            d = math.sqrt((e.pos[0] - pos[0])**2 + (e.pos[1] - pos[1])**2)
            if d < 3 * tile_len:
                return False
        return True

    def masami_event_trigger(self):
        if -scale(75) <= self.x <= -scale(75) and not self.masami_triggered:
            self.masami_triggered = True
            return True
        else:
            return False

    def spawn_masami(self, x):
        self.enemies.append(Masami(x))

    def move(self, direction):
        self.x -= self.speed*direction
        for floor in self.floors:
            floor.x -= self.speed*direction
        for enemy in self.enemies:
            enemy.pos = (enemy.pos[0] - self.speed*direction, enemy.pos[1])
            if hasattr(enemy, 'projectiles'):
                for proj in enemy.projectiles:
                    proj.pos = (proj.pos[0] - self.speed*direction, proj.pos[1])

    def draw(self):
        window.blit(self.background_2, (self.x // 10, 0))
        window.blit(self.background_1, (self.x // 5, 0))
        window.blit(self.foreground, (self.x, 0))
        for floor in self.floors:
            floor.draw()
        for enemy in self.enemies:
            enemy.draw()
