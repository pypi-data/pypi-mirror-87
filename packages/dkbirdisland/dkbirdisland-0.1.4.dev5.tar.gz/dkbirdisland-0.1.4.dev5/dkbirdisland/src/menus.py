import pygame
import sys
from . import tools
from .scoreboard import Scoreboard
from .game import game
from .donkey import Donkey


def menu(screen):
    pygame.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    class Main_Menu:
        def __init__(self):
            self.press = tools.load_img('press.png')
            self.background = tools.load_img("menu.png")
            self.verify = 1

        def update(self):
            if self.verify:
                screen.blit(self.press, (130, 300))
                self.verify = 0
            else:
                self.verify = 1

        def draw(self):
            screen.blit(self.background, (0, 0))

    pygame.display.set_caption('Donkey Kong: Bird Island')

    # Plays music
    volume = 0.3
    tools.play_music('menu_music.ogg', volume)
    menu = Main_Menu()
    running = True

    while running:
        pygame.time.delay(500)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                pygame.mixer.music.stop()
                screen.fill((0, 0, 0))
                pygame.display.update()
                pygame.time.wait(400)
                game(screen)

        menu.draw()
        menu.update()

        pygame.display.update()


def gameover(screen, MIN_HEIGHT, SPEED_JUMP, GRAVITY):
    pygame.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    class GameOver:
        def __init__(self):
            self.background = tools.load_img('game_over.png')
            self.retry_button = tools.load_img('retry.png')
            self.retry_button = pygame.transform.scale(self.retry_button, (60, 60))

        def draw(self, screen):
            screen.blit(self.background, (0, 0))
            screen.blit(self.retry_button, (370, 190))

    game_over = GameOver()
    scb = Scoreboard(screen)

    tools.play_music('gameover_music.ogg', 0.3)

    donkey_group = pygame.sprite.Group()
    donkey = Donkey(MIN_HEIGHT, SPEED_JUMP)
    donkey_group.add(donkey)

    running = True
    while running:
        pygame.time.delay(100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    screen.fill((0, 0, 0))
                    pygame.display.update()
                    pygame.time.wait(400)
                    game(screen)

        game_over.draw(screen)
        scb.draw(screen)
        donkey.sad()
        donkey_group.update(GRAVITY, MIN_HEIGHT)
        donkey_group.draw(screen)

        pygame.display.update()
