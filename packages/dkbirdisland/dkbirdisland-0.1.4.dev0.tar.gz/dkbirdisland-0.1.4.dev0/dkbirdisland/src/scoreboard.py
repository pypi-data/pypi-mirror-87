from . import tools


class Scoreboard:
    def __init__(self):
        self.score = '00000'
        self.font = tools.load_font('ARCADEPI.ttf', 30)

    def update(self):
        self.score = int(self.score) + 1
        self.score = f'{self.score:05}'
        self.scoreboard = self.font.render(self.score, True, (255, 255, 255))

    def draw(self, screen):
        screen.blit(self.scoreboard, (678, 5))