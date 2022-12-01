import pygame
import sys
from settings import *
from player import Player
from enemy import Enemy
from friend import Friend
from sprite import SimpleSprite
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame

# creates player centered camera
class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.bg = pygame.image.load('./graphics/map2.png').convert()
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


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('AUTOPOKES')
        self.clock = pygame.time.Clock()
        self.running = True

        # music
        music = pygame.mixer.Sound('./sounds/KleptoLindaMountainA.wav')
        music.play(-1)
        
        # sprite group
        self.all_sprites = AllSprites()
        self.obstacles = pygame.sprite.Group()

        # sprite setup
        self.setup()
        # self.player = Player(
        #     (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2), self.all_sprites)
        # self.enemy = Enemy(
        #     (CANVAS_WIDTH / 3, CANVAS_HEIGHT / 3), self.all_sprites)
        # self.friend = Friend(
        #     (CANVAS_WIDTH / 1.5, CANVAS_HEIGHT / 1.5), self.player, self.all_sprites)

    def setup(self):
        tmx_map = load_pygame('./data/map2/map2.tmx')

        for x, y, surf in tmx_map.get_layer_by_name('Collision').tiles():
            SimpleSprite((x * 16, y * 16), surf,
                         self.obstacles)

        for obj in tmx_map.get_layer_by_name('Entity'):
            if obj.name == 'Player':
                self.player = Player(
                    (obj.x, obj.y), self.obstacles, self.all_sprites)
            if obj.name == 'Enemy':
                Enemy((obj.x, obj.y), self.all_sprites)
            if obj.name == 'Friend':
                Friend(
                    (obj.x, obj.y), self.player, self.obstacles, self.all_sprites)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # if X button clicked in window, really make sure program exits
                    self.running = False
                    pygame.quit()
                    sys.exit()

            # delta time
            dt = self.clock.tick() / 1000

            # update
            self.display_surface.fill('darkgoldenrod4')
            self.all_sprites.update(dt)
            # draw
            self.all_sprites.custom_draw(self.player)
            # render frame
            pygame.display.update()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
