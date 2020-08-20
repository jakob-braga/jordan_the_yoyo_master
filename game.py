from world import *
import shutil


class Game:
    def __init__(self):
        self.player = Player()
        self.world = World()

        self.cross_hair = load_img('./images/cross_hair.png')

        self.font = pygame.font.Font('./font/pfont.ttf', 24)

        self.running = True

        self.masami_defeated = False

        self.post_boss_music_time = 0

        # ending
        self.end_up_img = load_img('./images/structures/end_up.png')
        self.end_down_img = load_img('./images/structures/end_down.png')

        # title screen
        self.title_screen_img = load_img('./images/title_screen.png')
        self.click_to_play_img = load_img('./images/click_to_play.png')

        # you died idiot
        self.death_screen = load_img('./images/you_died.png')
        new_scale = (self.death_screen.get_width() + 50, self.death_screen.get_height())
        self.death_screen = pygame.transform.scale(self.death_screen, new_scale)

        # cutscene
        self.cutscene_running = False
        p = 'images/masami/cutscene/'
        self.challenger_text = load_img(p + 'challenger_text.png')
        self.masami_text_1 = load_img(p + 'masami_text_1.png')
        self.masami_text_2 = load_img(p + 'masami_text_2.png')
        self.fireball_1 = load_img(p + 'fireball.png')
        self.fireball_2 = pygame.transform.flip(self.fireball_1, True, False)

        # sounds and music
        self.start_sound = pygame.mixer.Sound('./sound_effects/start.wav')
        self.jump_sound = pygame.mixer.Sound('./sound_effects/jump.wav')
        self.yoyo_sound = pygame.mixer.Sound('./sound_effects/yoyo.wav')
        self.take_damage_sound = pygame.mixer.Sound('./sound_effects/take_damage.wav')
        self.you_died_sound = pygame.mixer.Sound('./sound_effects/death.wav')
        self.hit_sound = pygame.mixer.Sound('./sound_effects/hit.wav')
        self.challenger_sound = pygame.mixer.Sound('./sound_effects/challenger.wav')
        self.text_sound = pygame.mixer.Sound('./sound_effects/text_printing_sound.wav')
        self.you_win_sound = pygame.mixer.Sound('./sound_effects/you_win.wav')

    # cutscene and menues

    def title(self):
        fade_in = 255
        fade_out = 0

        fade = pygame.Surface(window_size)
        fade.fill((0, 0, 0))

        title_screen = True
        exiting = False
        while title_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    title_screen = False
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and fade_in < 0:
                    exiting = True
                    self.start_sound.play()
                    pygame.mixer.music.fadeout(5000)

            clock.tick(60)

            if exiting:
                fade.set_alpha(fade_out)
                fade_out += 1
            else:
                fade.set_alpha(fade_in)
                fade_in -= 1

            if fade_out == 350:
                title_screen = False

            window.blit(self.title_screen_img, (0, 0))

            if fade_in < 0:
                if -fade_in // 30 % 2 == 1:
                    window.blit(self.click_to_play_img, (0, 0))

            window.blit(fade, (0, 0))

            pygame.display.update()

    def opening_story(self):
        self.text_sound.play()
        text = 'March 18, 2197'
        print_text_to_screen(text, (30, 50, window_size[0] - 60, window_size[1] - 100))
        self.text_sound.stop()

        fade = pygame.Surface(window_size)
        fade_out = 0
        fade.fill((0, 0, 0))
        exiting = False
        click_count = 0

        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif e.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    if click_count == 0:
                        self.text_sound.play()
                        text = 'The world has fallen into a state of chaos since the rise of the new era Mongolians and the inevitable disintegration of all democratic governments. Warlords have risen up to take control over what was once their neighbourhoods. The slums of Cambridge have been split into many districts governed by these new world tyrants, and the city is in a constant state of war.'
                        print_text_to_screen(text, (30, 150, window_size[0] - 60, window_size[1] - 100))
                        self.text_sound.stop()
                    elif click_count == 1:
                        self.text_sound.play()
                        text = 'Only one man is capable of putting an end to the tyranny, his name...'
                        print_text_to_screen(text, (30, 500, window_size[0] - 60, window_size[1] - 100))
                        self.text_sound.stop()
                    elif click_count == 2:
                        self.text_sound.play()
                        text = 'Jordan the yo yo master.'
                        print_text_to_screen(text, (30, 650, window_size[0] - 60, window_size[1] - 100))
                        self.text_sound.stop()
                    elif click_count == 3:
                        exiting = True
                        self.start_sound.play()
                    click_count += 1

            if exiting:
                fade_out += 1

            if fade_out > 255:
                waiting = False

            clock.tick(60)

            fade.set_alpha(fade_out)

            window.blit(fade, (0, 0))

            pygame.display.update()

    def you_died(self):

        timer = 0

        exiting = False
        fade_out = 0
        fade = pygame.Surface(window_size)
        fade.fill((0, 0, 0))

        death_delay = 120

        while fade_out < 256:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    fade_out = 3000
                elif event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_ESCAPE] and timer >= death_delay:
                        self.running = False
                        fade_out = 3000
                    elif pygame.key.get_pressed()[pygame.K_r] and timer >= death_delay:
                        exiting = True
                        self.start_sound.play()

            clock.tick(60)

            if timer == death_delay:
                window.blit(self.death_screen, (0, 0))
                pygame.display.update()

            if exiting:
                fade.set_alpha(fade_out)
                fade_out += 1
                window.blit(fade, (0, 0))
                pygame.display.update()

            timer += 1

        if fade_out < 3000:
            self.restart()

    def masami_cutscene(self):
        running = True

        incoming_sound = pygame.mixer.Sound('./sound_effects/incoming.wav')
        landed_sound = pygame.mixer.Sound('./sound_effects/landed.wav')
        masami_intro = pygame.mixer.Sound('./sound_effects/masami_intro.wav')

        self.post_boss_music_time = pygame.mixer.music.get_pos()

        pygame.mixer.music.load('./music/masami.mp3')

        self.challenger_sound.play(loops=1)

        self.player.yoyo.active = False
        self.player.moving = False

        timer = 0

        fireball_x = mid_x + 200

        first_pause = 80
        challenger_text = first_pause + 170
        fireball = challenger_text + 64
        rand_pause_after_fireball = 50
        masami_text = fireball + rand_pause_after_fireball + 210

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    running = False

            clock.tick(60)

            self.draw(update=False)

            if first_pause < timer < challenger_text:
                if (timer - first_pause) // 20 % 2 == 1:
                    window.blit(self.challenger_text, (0, 0))

            elif challenger_text <= timer < fireball:
                if timer == challenger_text:
                    incoming_sound.play()
                if (timer - challenger_text) // 10 % 2 == 1:
                    window.blit(self.fireball_1, (fireball_x, (timer - challenger_text) * 8))
                else:
                    window.blit(self.fireball_2, (fireball_x, (timer - challenger_text) * 8))

            elif timer == fireball:
                self.world.spawn_masami(fireball_x + scale(1))
                landed_sound.play()

            elif fireball + rand_pause_after_fireball <= timer < masami_text:
                if timer == fireball + rand_pause_after_fireball:
                    masami_intro.play()
                if (timer - fireball + rand_pause_after_fireball) // 20 % 2 == 1:
                    window.blit(self.masami_text_1, (0, 0))
                else:
                    window.blit(self.masami_text_2, (0, 0))

            if timer == masami_text:
                running = False

            pygame.display.update()

            timer += 1

        self.cutscene_running = False
        pygame.mixer.music.play()

    def masami_death_cutscene(self, masami):
        running = True

        self.masami_defeated = True
        self.world.floors.append(Structure(r_scale(100, 8, 6, 1), True))
        self.world.floors[-1].x += self.world.x

        explode_sound = pygame.mixer.Sound('./sound_effects/explosions.wav')
        beat_masami_sound = pygame.mixer.Sound('./sound_effects/beat_masami.wav')

        pygame.mixer.music.load('./music/jordan_the_yoyo_master.mp3')

        explosions_img = [
            load_img('./images/masami/cutscene/dead_1.png'),
            load_img('./images/masami/cutscene/dead_2.png'),
            load_img('./images/masami/cutscene/dead_3.png'),
            load_img('./images/masami/cutscene/dead_4.png')
        ]

        self.player.yoyo.active = False
        self.player.moving = False

        timer = 0
        explode_timer = 0

        first_pause = 60
        explosions = first_pause + 170
        post_explosions = explosions + 200

        draw_p = (masami.pos[0] - masami.r, masami.pos[1] - masami.r)

        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    running = False

            clock.tick(60)

            self.draw(update=False)

            if first_pause <= timer < explosions:
                if timer == first_pause:
                    explode_sound.play()
                window.blit(explosions_img[explode_timer // 7], draw_p)
                explode_timer += 1
                if explode_timer == 28:
                    explode_timer = 0
                if timer == first_pause + 30:
                    self.world.enemies.remove(masami)

            elif explosions <= timer < post_explosions:
                if timer == explosions + 30:
                    beat_masami_sound.play()

            if timer == post_explosions:
                running = False

            pygame.display.update()

            timer += 1

        self.cutscene_running = False
        pygame.mixer.music.play(-1, self.post_boss_music_time/1000)

    def you_win(self):
        pygame.mixer.music.stop()
        self.draw(player=False)
        running = True
        music_done = False
        timer = 0

        fade = pygame.Surface(window_size)
        fade.fill((0, 0, 0))

        fade_out = 0

        # save pictures to desktop
        original = './images/evidence_of_win.png'
        for i in range(0, 20):
            target = './../congrats' + str(i) + '.png'
            shutil.copyfile(original, target)

        while running:

            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    running = False

            fade.set_alpha(fade_out)

            if music_done and fade_out < 250:
                fade_out += 1

            elif not music_done:
                timer += 1

            if timer == 30:
                self.you_win_sound.play()

            elif timer == 200:
                music_done = True

            if fade_out == 250:
                running = False

            window.blit(fade, (0, 0))
            pygame.display.update()

        self.text_sound.play()
        text = 'With Masami, the warlord of Sag, defeated, the city became ever so closer to stable. Although Jordans work had just begun the rest is a story for another time... $%^ $%^ $%^ Press the Escape Key to Exit.'
        print_text_to_screen(text, (30, 150, window_size[0] - 60, window_size[1] - 100))
        self.text_sound.stop()

        running2 = True

        while running2:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    running2 = False
                elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    self.running = False
                    running2 = False

    # world updates ########################################################################################

    def world_update(self):
        self.world.enemy_update()
        if self.player.is_hit:
            self.player.hit_update()
        if self.player.y > window_size[1] + 300:
            self.player.health = 0
            pygame.mixer.music.stop()
            self.you_died_sound.play()
        player_pos_u = (int(mid_x), int(self.player.y - tile_len*3//2))
        player_pos_l = (int(mid_x), int(self.player.y - tile_len//2))
        for enemy in self.world.enemies:
            enemy.manage(self.player.get_upper_pos(), self.world.floors)
            if (enemy.intersect(player_pos_u, self.player.r) or enemy.intersect(player_pos_l, self.player.r)) and not self.player.is_hit:
                self.player.hit()
                if self.player.health > 1:
                    pygame.mixer.music.pause()
                    self.take_damage_sound.play()
                else:
                    pygame.mixer.music.stop()
                    self.you_died_sound.play()
            elif enemy.projectiles:
                for p in enemy.projectiles:
                    if (p.intersect(player_pos_u, self.player.r) or p.intersect(player_pos_l, self.player.r)) and not self.player.is_hit:
                        self.player.hit()
                        if self.player.health > 1:
                            pygame.mixer.music.pause()
                            self.take_damage_sound.play()
                        else:
                            pygame.mixer.music.stop()
                            self.you_died_sound.play()
                        break
            if (self.player.yoyo.intersect(enemy.pos, enemy.r) and enemy.can_hit and self.player.yoyo.active) and not self.player.is_hit:
                enemy.hit()
                self.hit_sound.play()
            if enemy.health <= 0:
                if isinstance(enemy, Masami):
                    self.masami_death_cutscene(enemy)
                else:
                    self.world.enemies.remove(enemy)

    def check_for_end_of_level(self):
        if -8000 <= self.world.x <= -7970 and not self.player.falling and not self.player.jumping:
            self.you_win()

    # main ##########################################################################################

    def is_running(self):
        return self.running

    def restart(self):
        self.__init__()
        pygame.mixer.music.load('./music/jordan_the_yoyo_master.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.5)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and not self.player.yoyo.active:
                if not self.player.is_hit:
                    m_pos = pygame.mouse.get_pos()
                    self.player.yoyo.set((mid_x, self.player.y - scale(1)), m_pos)
                    self.yoyo_sound.play()

        # movement

        if pygame.key.get_pressed()[pygame.K_a] and self.player.can_move_left:
            self.world.move(-1)
            self.player.moving = True
            self.player.right = False
        elif pygame.key.get_pressed()[pygame.K_d] and self.player.can_move_right:
            self.world.move(1)
            self.player.moving = True
            self.player.right = True
        else:
            self.player.moving = False

        # jumping/falling

        if pygame.key.get_pressed()[pygame.K_s]:
            self.player.drop(self.world.floors)
        elif pygame.key.get_pressed()[pygame.K_w] and not self.player.jumping and not self.player.falling:
            self.player.jumping = True
            self.jump_sound.play()
        elif pygame.key.get_pressed()[pygame.K_SPACE] and not self.player.jumping and not self.player.falling:
            self.player.jumping = True
            self.jump_sound.play()

    def update(self):
        self.player.move_check(self.world.floors, self.world.speed)
        self.player.falling = self.player.fall_check(self.world.floors)

        # unpause music after being hit
        if self.player.is_hit_timer == 100:
            pygame.mixer.music.unpause()

        if self.player.jumping:
            self.player.jump(self.world.floors)
        elif self.player.falling:
            self.player.jump(self.world.floors, fall=True)

        # yoyo

        if self.player.yoyo.active:
            self.player.yoyo.yoyo((mid_x, self.player.y - scale(1)))

        # death

        if self.player.health == 0:
            self.you_died()

        # world update

        self.world_update()

        if self.world.masami_event_trigger():
            self.cutscene_running = True
            self.masami_cutscene()

        if self.masami_defeated:
            self.check_for_end_of_level()

    def draw(self, update=True, player=True):
        self.world.draw()
        if self.world.x < -scale(85):
            if self.masami_defeated:
                window.blit(self.end_down_img, (scale(100) + self.world.x, 0))
            else:
                window.blit(self.end_up_img, (scale(100) + self.world.x, 0))
        if player:
            self.player.draw()
            if self.player.yoyo.active:
                p_cent = (mid_x, self.player.y - tile_len + 10)
                yoyo_pos = (math.floor(self.player.yoyo.pos[0]), math.floor(self.player.yoyo.pos[1]))
                pygame.draw.line(window, (0, 0, 0), p_cent, yoyo_pos, 5)
            cross_hair_draw_p = (math.floor(pygame.mouse.get_pos()[0] - scale(1/4)), math.floor(pygame.mouse.get_pos()[1] - scale(1/4)))
            self.player.yoyo.draw()
            window.blit(self.cross_hair, cross_hair_draw_p)

        fps = self.font.render(str(math.floor(clock.get_fps())), True, (200, 200, 200), (50, 50, 50))
        window.blit(fps, (0, 0))

        if update:
            pygame.display.update()
