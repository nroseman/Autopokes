import pygame
from pygame.math import Vector2 as vector
from random import uniform


class Friend(pygame.sprite.Sprite):
    def __init__(self, pos, player, collision_sprites, groups):
        super().__init__(groups)
        self.image = pygame.Surface((16, 16))
        self.image.fill('deeppink3')
        self.rect = self.image.get_rect(center=pos)

        # player interaction
        self.player = player
        self.friendzone_max = 100
        self.friendzone_min = 50
        self.idling = False
        self.idle_duration = 800

        # float based movement
        self.direction = vector()
        self.pos = vector(self.rect.center)
        self.speed = 200

        # collisions
        self.collision_sprites = collision_sprites
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
            self.idling = False
            self.speed = 200
            # self.status = self.status.split('_')[0]
        else:
            self.idle_walk(direction)

    # random idle path while close to player
    def idle_walk(self, direction):
        if not self.idling:
            self.direction = vector(uniform(-1, 1),
                                    uniform(-1, 1))
            self.idling = True
            self.speed = 50
            self.idle_start = pygame.time.get_ticks()

    # timer to change idle direction
    def idle_timer(self):
        if self.idling:
            current_time = pygame.time.get_ticks()
            if current_time - self.idle_start > self.idle_duration:
                self.idling = False

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
        self.walk_to_player()
        self.idle_timer()
        self.move(dt)
