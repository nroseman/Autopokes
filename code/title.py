import pygame
from code.state import State
from code.level1 import Level


class Title(State):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.font = pygame.font.Font(None, 50)
        self.text_surf = self.font.render(
            'PRESS ENTER TO START', True, 'white')
        self.text_rect = self.text_surf.get_rect()
        width, height = pygame.display.get_window_size()
        self.text_rect.center = (width/2, height/2)

    def update(self, dt, actions):
        if actions['start']:
            new_state = Level(self.game, '1')
            new_state.enter_state()

    def draw(self):
        self.game.display_surface.blit(self.text_surf, self.text_rect)
