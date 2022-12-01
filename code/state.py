
class State:
    def __init__(self, game) -> None:
        self.game = game
        self.prev_state = None
    
    def update(self, dt):
        pass

    def draw(self):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self)

    def exit_state(self):
        self.game.state_stack.pop()