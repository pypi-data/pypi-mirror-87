import pygame
from . import tools

class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos, GROUND_WIDTH, GROUND_HEIGHT, GAME_SPEED, SCREEN_HEIGHT):
        pygame.sprite.Sprite.__init__(self)

        self.image = tools.load_img('ground.fw.png')
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self, GAME_SPEED):
        self.rect[0] -= GAME_SPEED
