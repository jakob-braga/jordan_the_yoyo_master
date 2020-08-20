from game import *


game = Game()

pygame.mixer.music.load('./music/title.mp3')
pygame.mixer.music.play(-1)

#game.title()

#game.opening_story()

pygame.mouse.set_visible(False)

pygame.mixer.music.load('./music/jordan_the_yoyo_master.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

while game.is_running():

    clock.tick(60)

    game.handle_events()
    game.update()
    game.draw()

pygame.quit()
