import pygame
import sys
from settings import *

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('AUTOPOKES')
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    # if X button clicked in window, really make sure program exits
                    self.running = False
                    pygame.quit()
                    sys.exit()
        
        # update
        self.display_surface.fill('chartreuse')
        # draw

        # render frame
        pygame.display.update()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
