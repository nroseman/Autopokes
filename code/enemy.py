import pygame
from pygame.math import Vector2 as vector
from os import walk


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, path, collision_sprites, groups):
        super().__init__(groups)

        self.import_assets(path)  # animation imgs and audio

        # animation
        self.status = 'down'
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # float based movement
        self.direction = vector()
        self.pos = vector(self.rect.center)
        self.speed = 25

        # collisions
        self.collision_sprites = collision_sprites
        # self.z = LAYERS['Entity']
        self.hitbox = self.rect.copy()

        # targeting
        self.target = None

    def import_assets(self, path):
        # animation images
        self.animations = {}
        for index, folder in enumerate(walk(path)):
            if index == 0:
                for name in folder[1]:
                    self.animations[name] = []
            else:
                for name in sorted(folder[2], key=lambda string: int(string.split('.')[0])):
                    file_path = folder[0].replace('\\', '/') + '/' + name
                    surf = pygame.image.load(file_path).convert_alpha()
                    key = folder[0].split('\\')[1]
                    self.animations[key].append(surf)

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

    def noticed(self, target):
        self.target = target

    def get_target_distance_direction(self):
        if self.target:
            friend_pos = vector(self.rect.center)
            enemy_pos = vector(self.target.rect.center)
            distance = (enemy_pos - friend_pos).magnitude()
            if distance != 0:
                direction = (enemy_pos - friend_pos).normalize()
            else:
                direction = vector()

            return (distance, direction)
        else:
            return (vector(), vector())

    def check_to_disengage(self):
        if self.target and not self.target.target:
            self.direction = vector()
            self.target = None

    def move(self, dt):
        distance, self.direction = self.get_target_distance_direction()
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

    def animate(self, dt):

        current_animation = self.animations[self.status]

        if self.direction.magnitude() != 0:
            self.frame_index += 10 * dt
            if self.frame_index >= len(current_animation):
                self.frame_index = 0
        else:
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    def update(self, dt, actions):
        self.check_to_disengage()
        self.move(dt)
        self.animate(dt)
