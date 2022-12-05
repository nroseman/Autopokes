import pygame
import sys

from code.title import Title

# Finished: basic enemy/friend targeting and enemy animation
# Finished: Animate enviro tiles (ex. water)
# Finished: graphics refactoring
# Just Finished - friend animation
# TODO CURRENT: add friend attack mechanic
# TODO: Animate Player
# TODO: Make friend target a list (ie, self.targets = [])
# TODO: Give maps Warp, Spawn points
# TODO: Create game save file to save/load game states


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (1280, 720))
        # pygame.display.set_caption('AUTOPOKES')
        self.clock = pygame.time.Clock()

        self.dt = 0
        self.running = True

        # dictionary of valid key events
        self.actions = {"left": False, "right": False, "up": False,
                        "down": False, "action1": False, "action2": False, "start": False}
        self.state_stack = []

        self.load_state()

    def load_state(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

    def get_events(self):
        # main event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # if X button clicked in window, really make sure program exits
                self.running = False
                pygame.quit()
                sys.exit()
            # key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.actions['left'] = True

                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.actions['right'] = True

                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.actions['up'] = True

                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.actions['down'] = True

                if event.key == pygame.K_p:
                    self.actions['action1'] = True
                if event.key == pygame.K_o:
                    self.actions['action2'] = True
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = True
            # key no longer pressed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    self.actions['left'] = False
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    self.actions['right'] = False
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    self.actions['up'] = False
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    self.actions['down'] = False
                if event.key == pygame.K_p:
                    self.actions['action1'] = False
                if event.key == pygame.K_o:
                    self.actions['action2'] = False
                if event.key == pygame.K_RETURN:
                    self.actions['start'] = False

    def run(self):
        while self.running:
            self.get_events()

            # delta time
            self.dt = self.clock.tick() / 1000
            pygame.display.set_caption('{0:.2f}'.format(self.clock.get_fps()))

            # update
            self.update()

            # draw
            self.draw()

    def update(self):
        self.display_surface.fill('darkgoldenrod4')
        self.state_stack[-1].update(self.dt, self.actions)

    def draw(self):
        self.state_stack[-1].draw()
        # render frame
        pygame.display.update()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
    pygame.quit()
