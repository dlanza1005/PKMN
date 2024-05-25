from GameState import GameState
#from OverworldState import OverworldState
import pygame

class TitleScreenState(GameState):
    def __init__(self, game):
        self.game = game
        print("Title Screen")
        
        self.PX = self.game.save.PIXEL_SIZE
        self.title_image = pygame.image.load('title_image.png')
        self.title_image = pygame.transform.scale(self.title_image, (self.game.W, int(self.game.H * .88)))


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:   #  area, player_pos, player_dir
                    self.game.switch_state("OverworldState", [self.game.save.PLAYER_AREA, self.game.save.PLAYER_POS, self.game.save.PLAYER_DIRECTION])
                    print("switching out of TitleScreen")
                    return
                else:
                    return None  # Otherwise, do nothing
        return None

    def update(self):
        # update game state
        pass

    def draw(self, screen):
        # draw the title screen
        screen.fill((70,30,0))
        screen.blit(self.title_image, (0, int(.13 * .5 * self.game.H)))  # draws the image at the top-left corner