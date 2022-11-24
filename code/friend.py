import pygame


class Friend(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((64, 64))
        self.image.fill('deeppink3')
        self.rect = self.image.get_rect(center=pos)