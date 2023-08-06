import pygame
import random
import sys
from . import menus
from .donkey import Donkey
from .ground import Ground
from .obstacles import Obstacles
from .scoreboard import Scoreboard
from . import tools


def game(screen):
    pygame.display.set_caption("Donkey Kong: Bird Island")

    pygame.init()
    pygame.font.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 350
    GAME_SPEED = 16
    SPEED_JUMP = 50
    GRAVITY = 9
    GROUND_WIDTH = 2 * SCREEN_WIDTH
    GROUND_HEIGHT = 35
    MIN_HEIGHT = 228

    def is_off_screen(sprite):
        return sprite.rect[0] < -(sprite.rect[2])

    def get_random(sprite, width):
        return sprite.rect[0] <= width


    BACKGROUND = tools.load_img("background.png")
    tools.play_music('game_music.ogg', 0.3)

    # Defining groups and instantiating objects
    donkey_group = pygame.sprite.Group()
    donkey = Donkey(MIN_HEIGHT, SPEED_JUMP)
    donkey_group.add(donkey)

    ground_group = pygame.sprite.Group()
    for i in range(2):
        ground = Ground(GROUND_WIDTH * i, GROUND_WIDTH, GROUND_HEIGHT, GAME_SPEED, SCREEN_HEIGHT)
        ground_group.add(ground)

    obstacle_group = pygame.sprite.Group()
    obstacle = Obstacles(800, SCREEN_HEIGHT, GROUND_HEIGHT, GAME_SPEED)
    obstacle_group.add(obstacle)

    scb = Scoreboard(screen)

    clock = pygame.time.Clock()

    # Main loop
    verify = True
    running = True
    count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    donkey.jump(SPEED_JUMP, MIN_HEIGHT)

                if event.key == pygame.K_DOWN:
                    donkey.down(SPEED_JUMP, MIN_HEIGHT, GRAVITY)

        screen.blit(BACKGROUND, (0, 0))
        scb.display(screen)

        # Adds a new ground and remove
        if is_off_screen(ground_group.sprites()[0]):
            new_ground = Ground(ground_group.sprites()[1].rect[0] + GROUND_WIDTH, GROUND_WIDTH, GROUND_HEIGHT, GAME_SPEED, SCREEN_HEIGHT)
            ground_group.add(new_ground)
            ground_group.remove(ground_group.sprites()[0])

        # Removes obstacles
        if len(obstacle_group.sprites()) > 0 and is_off_screen(obstacle_group.sprites()[0]):
            obstacle_group.remove(obstacle_group.sprites()[0])
            verify = True
        
        # Check if the distance between the obstacles is correct
        if get_random(obstacle_group.sprites()[0], 300) and verify:
            verify = False
            new_obstacle1 = Obstacles(random.randint(800, 1300), SCREEN_HEIGHT, GROUND_HEIGHT, GAME_SPEED)
            obstacle_group.add(new_obstacle1)

        # Acceleration
        acceleration = 0
        if GAME_SPEED < 60:
            if count == 100:
                acceleration = 1
            elif count == 200:
                acceleration = 2
                count = 0
            GAME_SPEED += acceleration
            count += 1

        scb.update()
        donkey_group.update(GRAVITY, MIN_HEIGHT)
        obstacle_group.update(GAME_SPEED)
        ground_group.update(GAME_SPEED)

        donkey_group.draw(screen)
        obstacle_group.draw(screen)
        ground_group.draw(screen)

        pygame.display.update()

        # Collision
        if pygame.sprite.groupcollide(donkey_group, obstacle_group, False, False, pygame.sprite.collide_mask):
            pygame.mixer.music.stop()
            screen.fill((0, 0, 0))
            pygame.display.update()
            pygame.time.wait(400)
            scb.add()
            menus.gameover(screen, MIN_HEIGHT, SPEED_JUMP, GRAVITY)

        clock.tick(20)

