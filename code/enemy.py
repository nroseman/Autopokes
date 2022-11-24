import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((64, 64))
        self.image.fill('cyan3')
        self.rect = self.image.get_rect(center=pos)