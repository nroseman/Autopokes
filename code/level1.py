import pygame
from code.state import State
from pygame.math import Vector2 as vector
from random import randint
from pytmx.util_pygame import load_pygame
from code.player import Player
from code.enemy import Enemy
from code.friend import Friend
from code.sprite import SimpleSprite, AllSprites, AnimatedTile

# placeholder for level info - might become JSON or CSV?
levels = {'1': {'data': './data/map1/map.tmx', 'bg': './graphics/map/bg/1.png', 'warp': '2'},
          '2': {'data': './data/map1_int/map.tmx', 'bg': './graphics/map/bg/2.png', 'warp': '1'},
          '3': 'hello'
          }


class Level(State):
    def __init__(self, game, level_num) -> None:
        super().__init__(game)
        # music
        self.music = pygame.mixer.Sound('./sounds/KleptoLindaMountainA.wav')
        # self.music.play(-1)

        # get level info
        self.level_info = levels[level_num]

        # sprite group
        self.all_sprites = AllSprites(self.level_info['bg'])
        self.obstacles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.warp_tiles = pygame.sprite.Group()
        self.animated_tiles = pygame.sprite.Group()

        # sprite setup
        self.setup()

    def setup(self):

        tmx_map = load_pygame(self.level_info['data'])

        for layer in tmx_map.layers:

            if layer.name == 'Collision':
                for x, y, surf in layer.tiles():
                    SimpleSprite((x * 16, y * 16), surf, self.obstacles)
            if layer.name == 'Warp':
                for x, y, surf in layer.tiles():
                    SimpleSprite((x * 16, y * 16), surf,
                                 self.warp_tiles)
            if layer.name == 'Water':
                for x, y, surf in layer.tiles():
                    AnimatedTile((x * 16, y * 16), './graphics/map/water/water' + str(randint(0,3)),
                                 self.all_sprites)
            if layer.name == 'Coast':
                for x, y, surf in layer.tiles():
                    SimpleSprite((x * 16, y * 16), surf,
                                 self.all_sprites)

        # tmx_map = load_pygame('./data/map1/map.tmx')

        # for x, y, surf in tmx_map.get_layer_by_name('Collision').tiles():
        #     SimpleSprite((x * 16, y * 16), surf,
        #                  self.obstacles)

        # for x, y, surf in tmx_map.get_layer_by_name('Warp').tiles():
        #     SimpleSprite((x * 16, y * 16), surf,
        #                  self.warp_tiles)

        # for x, y, surf in tmx_map.get_layer_by_name('Water').tiles():
        #     AnimatedTile((x * 16, y * 16),
        #                  './graphics/map/water/water0/0.png', self.all_sprites)

        # for x, y, surf in tmx_map.get_layer_by_name('Coast').tiles():
        #     SimpleSprite((x * 16, y * 16), surf,
        #                  self.all_sprites)

        for obj in tmx_map.get_layer_by_name('Entity'):
            if obj.name == 'Player':
                self.player = Player(
                    (obj.x, obj.y), self.obstacles, self.warp_tiles, self.all_sprites)
            if obj.name == 'Enemy':
                Enemy((obj.x, obj.y), './graphics/enemy', self.obstacles, [
                      self.enemies, self.all_sprites])
            if obj.name == 'Friend':
                Friend(
                    (obj.x, obj.y), self.player, self.enemies, self.obstacles, self.all_sprites)

    def update(self, dt, actions):
        self.all_sprites.update(dt, actions)

        if self.player.warp:
            self.music.stop()
            new_state = Level(self.game, self.level_info['warp'])
            self.exit_state()
            new_state.enter_state()

    def draw(self):
        self.all_sprites.custom_draw(self.player)
