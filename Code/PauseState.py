import pygame
from GameState import GameState



class PauseState(GameState):
    def __init__(self, game):
        self.game=game
        print("Pause State!")
        self.option_selected = 0
        self.options = ["POKEDEX","POKEMON","BAG","AR GEAR","SAVE","OPTIONS","QUIT"]
        self.colors = [(50,50,50),(255,255,255)] # option colors
        self.X = int(self.game.W*3/4)  
        self.Y = int(self.game.H/30)  
        self.W = int((self.game.W*1/4)-(self.game.H/30))     
        self.H = int(self.game.H - 2*(self.game.H/30))

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.option_selected = (self.option_selected + 1) % len(self.options)  # Cycle through options
                elif event.key == pygame.K_UP:
                    self.option_selected = (self.option_selected - 1) % len(self.options)  # Cycle through options
                elif event.key == pygame.K_z:
                    self.game.pop_state() #          switch_state(self, state, args)
                elif event.key == pygame.K_x:
                    if self.option_selected == 0:
                        self.game.switch_state("PokedexState", None)  #        self.game.switch_state(state, args)
                    elif self.option_selected == 1:
                        self.game.switch_state("PartyState", None) # return PartyState(game)
                    elif self.option_selected == 2:
                        self.game.switch_state("BagState", None)
                    elif self.option_selected == 3:
                        self.game.switch_state("ARGearState", None)#return ARGearState(game)
                    elif self.option_selected == 4:
                        self.game.switch_state("SaveState", None)#return SaveState(game)
                    elif self.option_selected == 5:
                        self.game.switch_state("OptionsState", None)# return OptionsState(game)
                    elif self.option_selected == 6:
                        self.game.switch_state("QuitState", None)#return QuitState(game)                    
                    else:
                        return None  # Otherwise, do nothing
        return None

    def update(self):
        # update where the selector arrow is displayed?
        return None

    def draw(self, screen):
        # Draw the menu options, highlighting the one that's selected

        pygame.draw.rect(screen,(150,150,150),(self.X, self.Y, self.W, self.H)) # (600,20,180,560) 
        
        # MAKE THIS NICERLY CODED
        #menu = [game.font.render("", True, self.colors[0]),game.font.render("", True, self.colors[0]),game.font.render("", True, self.colors[0]),game.font.render("", True, self.colors[0]),game.font.render("", True, self.colors[0]),game.font.render("", True, self.colors[0]),game.font.render("", True, self.colors[0])]
        menu = [None, None, None, None, None, None, None]
        for i in range(0,len(self.options)):
            if self.option_selected == i:
                menu[i] = self.game.font.render(self.options[i], True, self.colors[1])
            else:
                menu[i] = self.game.font.render(self.options[i], True, self.colors[0])
            screen.blit(menu[i], (self.X+self.Y, 2*self.Y+int(i*self.H/7)))     # (80*i))) # self.H/7