import pygame
import os

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]


def load_img(name):
    path = os.path.join(MAIN_DIR, '../images', name)
    return pygame.image.load(path)


def load_font(name, size):
    path = os.path.join(MAIN_DIR, '../fonts', name)
    return pygame.font.Font(path, size)


def load_sound(name, volume):
    path = os.path.join(MAIN_DIR, '../sounds', name)
    sound = pygame.mixer.Sound(path)
    sound.set_volume(volume)
    return sound

def play_music(name, volume):
    path = os.path.join(MAIN_DIR, '../sounds', name)
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(loops=-1)


