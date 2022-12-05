import pygame
from os import listdir
from settings import *
from pygame.math import Vector2 as vector

# mostly for hidden tiles


class SimpleSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.copy()

# animated, non-interactive


class AnimatedTile(pygame.sprite.Sprite):
    def __init__(self, pos, path, groups):
        super().__init__(groups)

        self.import_assets(path)

        self.frame_index = 0
        self.image = self.animations[self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

    def import_assets(self, path):
        # animation images
        self.animations = []
        for img in listdir(path):
            img_name = path + '/' + img
            surf = pygame.image.load(img_name).convert_alpha()
            self.animations.append(surf)

    def update(self, dt, actions):
        self.frame_index += 1.5 * dt
        if self.frame_index >= len(self.animations):
            self.frame_index = 0

        self.image = self.animations[int(self.frame_index)]


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

        # reset canvas
        self.canvas.fill('black')

        # draw background first
        self.canvas.blit(self.bg, -self.offset)

        # draw sprites with offset
        for sprite in self.sprites():
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.canvas.blit(sprite.image, offset_rect)

        self.display_surface.blit(pygame.transform.scale(
            self.canvas, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))
