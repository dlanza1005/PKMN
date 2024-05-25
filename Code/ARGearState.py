import pygame
from GameState import GameState

class ARGearState(GameState):
    def __init__(self, game):
        super().__init__(game)
        print("AR Gear")

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_LEFT:
                    pass
                elif event.key == pygame.K_RIGHT:
                    pass
                elif event.key == pygame.K_z:
                    raise PopState
                elif event.key == pygame.K_x:
                    pass
        return None

    def update(self):
        # update where the selector arrow is displayed
        return None

    def draw(self, screen):
        # Draw!
        pygame.draw.rect(screen,(150,150,150),(50,0,20,30))