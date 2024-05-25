import pygame
from GameState import GameState
from GameState import PopState

class OptionsState(GameState):
    def __init__(self, game):
        super().__init__(game) # why am i initializing the game class here? that seems incorrect..
        self.SCREEN_WIDTH_IN_BLOCKS = 15
        self.SCREEN_HEIGHT_IN_BLOCKS = 11 # it looks like the screen is 11 blocks tall but the top and bottom are half blocks
        self.PIXEL_SIZE = 2  # NUMBER OF SCREEN PIXELS PER GAME SPRITE PIXEL. load from options file.
        # SCREEN_WIDTH = PIXEL_SIZE*16*15
        self.SCREEN_WIDTH = self.SCREEN_WIDTH_IN_BLOCKS*16*self.PIXEL_SIZE
        self.SCREEN_HEIGHT = self.SCREEN_HEIGHT_IN_BLOCKS*16*self.PIXEL_SIZE
        print("options")

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

###########################################################
# maybe include this info in the options state:
###########################################################

############ screen size:
# self.screen = pygame.display.set_mode((800, 600))
#       -need to keep the 3/4 ratio

############ clock speed:
# self.clock = pygame.time.Clock()

############ font and font size? (therefore also menu sizes?)
# self.font = pygame.font.Font("pokemon_pixel_font.ttf", 38) # try different font variables, fonts, sizes,...