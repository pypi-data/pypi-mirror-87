import pygame
from . import tools
from .game import game


def menu(screen):
    pygame.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    
    class Main_Menu:
        def __init__(self):
            self.text = 'Press any key to start'
            self.font = tools.load_font('ARCADEPI.ttf', 30)

        def update(self):
            self.text_menu = self.font.render(self.text, True, (255, 255, 255))
        def draw(self, screen):
            screen.blit(self.text_menu, (170, 300))

    BACKGROUND = tools.load_img("background.png")

    pygame.display.set_caption('Donkey Kong: Bird Island')
    clock = pygame.time.Clock()
    
    #Plays music
    volume = 0.3
    tools.play_music('music_menu.wav', volume)
    text_menu = Main_Menu()

    running = True
    while running:
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                pygame.mixer.music.pause()
                game(screen)
        screen.blit(BACKGROUND, (0, 0))

        text_menu.update()
        text_menu.draw(screen)

        pygame.display.update()
    pygame.quit()
