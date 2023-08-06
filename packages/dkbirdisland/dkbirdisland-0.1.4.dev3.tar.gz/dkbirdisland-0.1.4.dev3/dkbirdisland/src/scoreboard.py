import shelve
import os
from . import tools

MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
SHELVE_PATH = os.path.join(MAIN_DIR, 'high_score.txt')


class Scoreboard:
    def __init__(self, screen):
        self.score = '00000'
        self.last_score = '00000'
        self.high_score = '00000'
        self.font = tools.load_font('ARCADEPI.ttf', 23)

        d = shelve.open(SHELVE_PATH)

        if 'hi' in d:
            self.high_score = d['hi']

        if 'score' in d:
            self.last_score = d['score']

        self.high_score_text = self.font.render(self.high_score, False, (255, 255, 255))
        self.scoreboard = self.font.render(self.score, False, (255, 255, 255))
        d.close()

    def display(self, screen):
        screen.blit(self.font.render("HI", False, (255, 255, 255)), (550, 5))
        screen.blit(self.high_score_text, (590, 5))
        screen.blit(self.scoreboard, (705, 5))

    def update(self):
        self.score = int(self.score) + 1
        self.score = f'{self.score:05}'
        self.scoreboard = self.font.render(self.score, False, (255, 255, 255))

    def add(self):
        d = shelve.open(SHELVE_PATH)
        d['score'] = self.score

        if int(self.score) > int(self.high_score):
            d['hi'] = self.score
            self.high_score = self.score
            self.high_score_text = self.font.render(self.high_score, False, (255, 255, 255))

        d.close()

    def draw(self, screen):
        self.scoreboard = self.font.render(self.last_score, False, (255, 255, 255))
        screen.blit(self.scoreboard, (705, 5))
