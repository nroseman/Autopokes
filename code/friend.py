import pygame
from pygame.math import Vector2 as vector
from os import walk
from math import atan2, pi
from random import uniform


class Friend(pygame.sprite.Sprite):
    def __init__(self, pos, path, player, enemies, collision_sprites, groups):
        super().__init__(groups)

        self.import_assets(path)

        # animation
        self.status = 'idle'
        self.walk_directions = ['up', 'right', 'down', 'left', 'up']
        self.frame_index = 0
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # player interaction
        self.player = player
        self.friendzone_max = 75
        self.friendzone_min = 20
        self.idling = False
        self.idle_duration = 800

        # enemy interaction
        self.enemies = enemies
        self.target = None
        self.targeting = False
        self.targetzone_max = 100

        # battle
        self.attacking = False
        self.attack_radius = 20
        self.health = 100
        self.power = 10

        # float based movement
        self.direction = vector()
        self.pos = vector(self.rect.center)
        self.speed = 200

        # collisions
        self.collision_sprites = collision_sprites
        # self.z = LAYERS['Entity']
        self.hitbox = self.rect.copy()

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

    def get_player_distance_direction(self):
        friend_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)
        distance = (player_pos - friend_pos).magnitude()
        if distance != 0:
            direction = (player_pos - friend_pos).normalize()
        else:
            direction = vector()

        return (distance, direction)

    def get_target(self):
        friend_pos = vector(self.rect.center)
        if not self.target:
            for sprite in self.enemies.sprites():
                distance = (
                    friend_pos - vector(sprite.rect.center)).magnitude()
                if distance < self.friendzone_max:
                    self.target = sprite

        else:
            if (friend_pos - vector(self.target.rect.center)).magnitude() > self.targetzone_max:
                self.target = False

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
            return (0, 0)

    def action_decision(self):
        target_distance, target_direction = self.get_target_distance_direction()
        player_distance, player_direction = self.get_player_distance_direction()
        # walk to targeted enemy
        if self.target and target_distance <= self.attack_radius and not self.attacking:
            self.attacking = True
            self.frame_index = 0

        # if self.attacking:
        #     self.status = self.status.split('_')[0] + '_attack'

        if self.target and player_distance < self.friendzone_max:
            self.direction = target_direction
            self.idling = False
            self.speed = 25
            if not self.targeting:
                self.target.noticed(self)  # enemy starts tracking
        # walk to player or idle
        elif player_distance > self.friendzone_max:
            self.direction = player_direction
            self.idling = False
            self.speed = 200
            self.targeting = False
        else:
            self.idle_walk()

    # random idle path while close to player
    def idle_walk(self):
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

    def get_status(self):
        # idle
        if self.direction.x == 0 and self.direction.y == 0:
            self.status = 'idle'
        else:
            # use vector to get cardinal direction
            degree = atan2(self.direction.x, -self.direction.y)/pi*180
            if degree < 0:
                degree = 360 + degree
            print(degree)
            self.status = self.walk_directions[round(degree/90)]

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 10 * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    def update(self, dt, actions):
        self.get_target()
        self.action_decision()
        self.idle_timer()
        self.get_status()
        self.animate(dt)
        self.move(dt)
