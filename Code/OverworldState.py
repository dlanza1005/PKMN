import pygame
from GameState import GameState
from SaveData import save_data
from TiledMap import TiledMap
# from BattleState import BattleState
# from PauseState import PauseState
# from TextboxState import TextboxState
from NPC import NPC


class OverworldState(GameState):
    def __init__(self, game, area, player_pos, player_dir):
        # Initialize player, NPC positions etc. here
        print("overworld state")
        self.game = game
        self.player_pos = player_pos
        self.player_dir = player_dir
        self.current_area = area 
        
        # load player position, player object, npc positions and objects, items
        # self.pos = game.player.position #[25,20] # use this to get map offset?
        self.PX = self.game.save.PIXEL_SIZE
        self.W = self.PX*16*15 # (number of screen pixels per game pixel) * (16 game pixels per tile) * (screen is 15 tiles wide)
        self.H = self.PX*16*11 # (number of screen pixels per game pixel) * (16 game pixels per tile) * (screen is ~11 tiles tall)
        self.TempSurf = pygame.Surface((self.W, self.H)) # take size info from save_data
        self.arrow_stack = []
        self.NPCs = []
        self.NPCs.append(NPC(game, game.player.area, [76,71],"D")) # take NPC info from TiledMap, right? 

    def handle_events(self, events): 
        # clean the arrow key inputs and call self.player.handle_input at the right times, 
        # i.e. after taking a step if the button is still held down, etc.
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.game.player.handle_input("D")
                    #print("D")
                elif event.key == pygame.K_UP:
                    self.game.player.handle_input("U")
                    #print("U")
                elif event.key == pygame.K_LEFT:
                    self.game.player.handle_input("L")
                    #print("L")
                elif event.key == pygame.K_RIGHT:
                    self.game.player.handle_input("R")
                    #print("R")
                elif event.key == pygame.K_x:
                    pass # self.player.handle_input("x")
                elif event.key == pygame.K_z:
                    pass # self.player.handle_input("z")? do i need this here?
                elif event.key == pygame.K_b:
                    return ["BattleState", self.game.TEST_OPPONENT]    ######################             
                elif event.key == pygame.K_p:
                    self.game.push_state("PauseState",None)
                elif event.key == pygame.K_t:
                    msg = "This is a public service announcement, this is only a test. Peter Piper Picked a Peck of Pickled Peppers. Oh Potatoes and Molasses!!"
                    self.game.push_state("TextboxState", [msg, 800, 600, self.game.font])
                else:
                    pass
        if keys[pygame.K_DOWN] and self.game.player.direction=="D":
            self.game.player.handle_input("D")
            #print("d")
        elif keys[pygame.K_UP] and self.game.player.direction=="U":
            self.game.player.handle_input("U")
            #print("u")
        elif keys[pygame.K_LEFT] and self.game.player.direction=="L":
            self.game.player.handle_input("L")
            #print("l")
        elif keys[pygame.K_RIGHT] and self.game.player.direction=="R":
            self.game.player.handle_input("R")
            #print("r")
        else:
            self.game.player.handle_input("*")                


    def update(self):
        # Update player and NPC sprites if walking, update NPC locations, update map position, etc.
        self.game.player.update() 
        # check doors?
        self.new_area(self.game.player.area.check_doors(self.game.player.position))
        for NPC in self.NPCs:
            NPC.update()


    def draw(self, screen):
        # Draw the game world
        screen.fill((0, 0, 0))  # Fill the screen with black before drawing
        self.TempSurf.fill((0, 0, 0))
        self.game.player.area.draw_map(self.TempSurf, self.game.player.position) # need self.pos because it draws the local tiles
        for NPC in self.NPCs:
            NPC.draw(self.TempSurf, self.game.player.position)
        screen.blit(self.TempSurf, (0,0))
        self.game.player.draw(screen)
        # draw NPCs in current_area
    
    def new_area(self, area_info):
        # load a new area by changing the map, player position, player direction, list of NPCs, etc.
        if area_info == None:
            return
        else:
            area = area_info["area"]
            pos = area_info["pos"]
            direction = area_info["direction"]
            NPC_List = area_info["NPC_List"]
            # fade out
            self.game.player.area = TiledMap(self.game, area) 
            self.NPCs = []
            self.game.player.position = pos
            self.game.player.direction = direction
            # fade in
            # make the player walk 1 space through the door.. or walk to the center of the elevator and turn around.. etc.
    