import pygame
from pygame.math import Vector2 as vector


class Friend(pygame.sprite.Sprite):
    def __init__(self, pos, player, groups):
        super().__init__(groups)
        self.image = pygame.Surface((32, 32))
        self.image.fill('deeppink3')
        self.rect = self.image.get_rect(center=pos)

        # player interaction
        self.player = player
        self.friendzone_max = 200
        self.friendzone_min = 100

        # float based movement
        self.direction = vector()
        self.pos = vector(self.rect.center)
        self.speed = 200

        # collisions
        # self.collision_sprites = collision_sprites
        # self.z = LAYERS['Entity']
        self.hitbox = self.rect.copy()

    def get_player_distance_direction(self):
        friend_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)
        distance = (player_pos - friend_pos).magnitude()
        if distance != 0:
            direction = (player_pos - friend_pos).normalize()
        else:
            direction = vector()

        return (distance, direction)

    def walk_to_player(self):
        distance, direction = self.get_player_distance_direction()
        if distance > self.friendzone_max:
            self.direction = direction
            # self.status = self.status.split('_')[0]
        else:
            self.direction = vector()

    def move(self, dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx

        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery

    def update(self, dt):
        self.walk_to_player()
        self.move(dt)
