import pygame
from pygame.math import Vector2 as vector


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, collision_sprites, groups):
        super().__init__(groups)

        # animation
        # self.status = 'down'
        # self.frame_index = 0

        # self.image = self.animations[self.status][self.frame_index]
        self.image = pygame.image.load(
            './graphics/justaguy.png').convert_alpha()

        self.rect = self.image.get_rect(center=pos)

        # float based movement
        self.direction = vector()
        self.pos = vector(self.rect.center)
        self.speed = 150

        # collisions
        self.collision_sprites = collision_sprites
        # self.z = LAYERS['Entity']
        self.hitbox = self.rect.copy()
    # def get_status(self):
    #     if self.direction.magnitude() == 0:
    #     self.status = self.status.split('_')[0] + '_idle'

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.status = 'right'
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.status = 'left'
            self.direction.x = -1
        else:
            self.direction.x = 0
        if keys[pygame.K_DOWN]:
            self.status = 'down'
            self.direction.y = 1
        elif keys[pygame.K_UP]:
            self.status = 'up'
            self.direction.y = -1
        else:
            self.direction.y = 0

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx

                else:
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery

    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def update(self, dt):
        self.input()
        self.move(dt)
