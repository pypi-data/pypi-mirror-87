import pygame
from .src import menu

screen = pygame.display.set_mode((800, 350))

def main():
    menu.menu(screen)

if __name__ == '__main__':
    main()
