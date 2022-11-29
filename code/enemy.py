import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((16, 16))
        self.image.fill('cyan3')
        self.rect = self.image.get_rect(center=pos)
