

class GameState:
    def __init__(self, game):
        pass

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

class PopState(Exception):
    def __init__(self):
        print("*pop!*")