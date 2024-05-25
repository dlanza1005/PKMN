import pygame

from GameState import GameState

class BagState(GameState):
    def __init__(self, game):
        super().__init__(game)
        print("bag")
        self.bg = "D:\MyPythonShit\GithubPKMN\BagScreens\\bg_m.png"
        self.pocket = 0
        self.pocket_contents = []
        self.cursor_location = 0

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_LEFT:
                    if self.pocket <= 0:
                        self.pocket = 4
                    else:
                        self.pocket = self.pocket-1
                elif event.key == pygame.K_RIGHT:
                    self.pocket = (self.pocket+1) % 5
                elif event.key == pygame.K_z:
                    OverworldState(game).draw(game.screen) # if you exit this screen, PauseState is underneath, and overworld is under that. so it needs a frame from overworld i guess..? i mean isnt the alternative to have it drawing every state at all times? no, because its a state stack. i just need to pop the states as needed...
                    raise PopState
                elif event.key == pygame.K_x:
                    pass
        return None

    def update(self):
        # update where the selector arrow is displayed
        return None

    def draw(self, screen):
        # Draw!
        screen.fill([50,50,100])
        screen.blit(self.bg, (-40, 100))  # draws the image at the top-left corner
        pygame.draw.rect(screen,(200,180,130),(30,30,50,50)) # pokeball as bag icon dingbat..?
        pygame.draw.rect(screen,(200,180,130),(90,30,290,50)) # pocket name
        pygame.draw.rect(screen,(220,220,220),(20,350,400,220)) # item description
        pygame.draw.rect(screen,(200,180,130),(390,20,390,560)) # pocket list bg
        pygame.draw.rect(screen,(220,220,200),(400,50,370,500)) # pocket list front
        pygame.draw.rect(screen,(220,220,220),(185,90,5,5))
        pygame.draw.rect(screen,(220,220,220),(210,90,5,5))
        pygame.draw.rect(screen,(220,220,220),(235,90,5,5))
        pygame.draw.rect(screen,(220,220,220),(260,90,5,5))
        pygame.draw.rect(screen,(220,220,220),(285,90,5,5))
        
        if self.pocket==0:
            pygame.draw.rect(screen,(220,30,30),(180,85,15,15))
        elif self.pocket==1:
            pygame.draw.rect(screen,(220,30,30),(205,85,15,15))
        elif self.pocket==2:
            pygame.draw.rect(screen,(220,30,30),(230,85,15,15))
        elif self.pocket==3:
            pygame.draw.rect(screen,(220,30,30),(255,85,15,15))
        elif self.pocket==4:
            pygame.draw.rect(screen,(220,30,30),(280,85,15,15))  
        else:
            pass
        #print(self.pocket)