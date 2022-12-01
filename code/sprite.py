import pygame
from settings import *
from pygame.math import Vector2 as vector


class SimpleSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()


# creates player centered camera
class AllSprites(pygame.sprite.Group):
    def __init__(self, bg):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.bg = pygame.image.load(bg).convert()
        self.offset = vector()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - CANVAS_WIDTH / 2
        self.offset.y = player.rect.centery - CANVAS_HEIGHT / 2

        # draw background first
        self.canvas.blit(self.bg, -self.offset)

        # draw sprites with offset
        for sprite in self.sprites():
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.canvas.blit(sprite.image, offset_rect)

        self.display_surface.blit(pygame.transform.scale(
            self.canvas, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
