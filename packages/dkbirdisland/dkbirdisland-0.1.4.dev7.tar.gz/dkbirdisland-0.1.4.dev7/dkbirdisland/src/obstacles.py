import pygame
from random import randrange
from . import tools

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, xpos, SCREEN_HEIGHT, GROUND_HEIGHT, GAME_SPEED):
        pygame.sprite.Sprite.__init__(self)

        self.images = [tools.load_img('snake1.png').convert_alpha(),
                        tools.load_img('barris.png').convert_alpha(),
                        tools.load_img('mouse.png').convert_alpha()]

        range = randrange(0, len(self.images))

        self.image = self.images[range]
        if range == 0:
            self.image = pygame.transform.scale(self.image, (40, 70))
        elif range == 1:
            self.image = pygame.transform.scale(self.image, (73, 70))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT - self.rect[3]

    def update(self, GAME_SPEED):
        self.rect[0] -= GAME_SPEED
