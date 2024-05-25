import pygame
import time
from TiledMap import TiledMap
from GameState import PopState
from GameData import game_data # is this needed here..?
from SaveData import save_data
from TitleScreenState import TitleScreenState
from Player import Player
from ARGearState import ARGearState
from BagState import BagState
from BattleState import BattleState
from OptionsState import OptionsState
from OverworldState import OverworldState
from PartyDetailState import PartyDetailState
from PartyState import PartyState
from PauseState import PauseState
from TextboxState import TextboxState
from PokedexState import PokedexState
from TiledMap import TiledMap
from NPC import NPC


# this class should:
#   -create the game window
#   -initialize the game data, save data,
#   -manage the state stack
#   -direct control input to the state classes


class Game:   ###############    MAIN CLASS!
    def __init__(self):
        self.save = save_data
        self.W = self.save.PIXEL_SIZE*16*15 # (number of screen pixels per game pixel) * (16 game pixels per tile) * (screen is 15 tiles wide)
        self.H = self.save.PIXEL_SIZE*16*11 # (number of screen pixels per game pixel) * (16 game pixels per tile) * (screen is ~11 tiles tall)
        # self.screen = pygame.display.set_mode((self.W, self.H))
        # self.clock = pygame.time.Clock()
        # self.dt = .05

        self.font_size = self.save.FONT_SIZE*self.save.PIXEL_SIZE
        self.font = pygame.font.Font(self.save.FONT, self.font_size) # make it self.save.FONT_SIZE * self.save.PIXEL_SIZE ... but where to store the variables so that they update when the player changes the settings?
        self.running = True
        self.state_stack = []
        
        self.player = Player(self, TiledMap(self, self.save.PLAYER_AREA), self.save.PLAYER_POS, self.save.PLAYER_DIRECTION) # pass game and save data into here...

        
        
        self.wild_pokemon = []
        self.TEST_OPPONENT = []

        
        

        self.state_stack.append(TitleScreenState(self))

        
    #def generate_pokemon(self, species, level, item=None, instance_data=None): # add instance data for your own pkmn
        ## Create a new Pokemon of the specified species and level
        #base_data = self.data.pokemon_data[species]
        #new_pokemon = Pokemon(base_data, self.data.sprites, level, item)
        #return new_pokemon    
        

    def push_state(self, state, args):
        #self.state_stack.append(state)
        if state == "TitleScreenState":
            self.state_stack.append(TitleScreenState(self))
        elif state == "OverworldState":
            self.state_stack.append(OverworldState(self, args[0], args[1], args[2]))     #   state[1:])) # area, player_pos, player_dir):
        elif state == "PauseState":
            self.state_stack.append(PauseState(self))
        elif state == "PartyState":
            self.state_stack.append(PartyState(self))
        elif state == "PartyDetailState":
            self.state_stack.append(PartyDetailState(args))
        elif state == "PokedexState":
            self.state_stack.append(PokedexState(self))
        elif state == "ARGearState":
            self.state_stack.append(ARGearState(self))
        elif state == "BagState":
            self.state_stack.append(BagState(self))
        elif state == "TextboxState":
            self.state_stack.append(TextboxState(self, args))
        elif state == "BattleState":
            self.state_stack.append(BattleState(self, args[0], args[1])) # game, player, opponent

    def pop_state(self):
        return self.state_stack.pop()

    def switch_state(self, state, args):
        if self.state_stack:
            self.state_stack.pop()
        self.push_state(state, args)


    # Create a method to load wild Pokemon and opposing teams from game data
    #def load_encounter(self, encounter_data):
    #    self.wild_pokemon = [Pokemon.from_dict(d) for d in encounter_data['wild_pokemon']]
    #    self.opposing_team = [Pokemon.from_dict(d) for d in encounter_data['opposing_team']]    


    def run(self, screen, dt):
        while self.running and self.state_stack:
            state = self.state_stack[-1] # is -1 the last index?
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            state.handle_events(events)
            # if next_state is not None:  # if state wants to switch to a new state 
            #     if next_state == "TitleScreenState":
            #         self.push_state(TitleScreenState())
            #     elif next_state == "OverworldState":
            #         self.push_state(OverworldState()) # area, player_pos, player_dir):
            #     elif next_state == "PauseState":
            #         self.push_state(PauseState())
            #     elif next_state == "PartyState":
            #         self.push_state(PartyState())
            #     elif next_state == "PartyDetailState":
            #         self.push_state(PartyDetailState())
            #     elif next_state == "PokedexState":
            #         self.push_state(PokedexState())
            #     elif next_state == "ARGearState":
            #         self.push_state(ARGearState())
            #     elif next_state == "BagState":
            #         self.push_state(BagState())
            #     elif next_state == "TextboxState":
            #         self.push_state(TextboxState())
            #     elif next_state == "PopState":
            #         self.push_state(PopState())
                #next_state = None # is this right to put here?
            state.update()
            [state.draw(screen) for state in self.state_stack] # trying to draw the overworld when in the pause screen.
            pygame.display.flip()
            time.sleep(dt) ## this is dt, store it in the game options or save data class
        pygame.quit()


#######################################################
#######################################################


# game = Game


# # Create Pokemon objects
# bulbasaur1_instance = {'Level':5}
# bulbasaur1 = Pokemon.generate_pokemon('BULBASAUR', bulbasaur1_instance)  # Level 5 Bulbasaur

# charmander1_instance = {'Level':5}
# charmander1 = Pokemon.generate_pokemon('CHARMANDER', charmander1_instance)  # Level 5 Charmander

# squirtle1_instance = {'Level':15}
# squirtle1 = Pokemon.generate_pokemon('SQUIRTLE', squirtle1_instance) # Level 15 Squirtle

# bulbasaur2_instance = {'Level':4}
# bulbasaur2 = Pokemon.generate_pokemon('BULBASAUR', bulbasaur2_instance)  # Level 4 Bulbasaur

# charmander2_instance = {'Level':4}
# charmander2 = Pokemon.generate_pokemon('CHARMANDER', charmander2_instance)  # Level 4 Charmander

# # Add Bulbasaur to the player's party and Charmander to the opponent's party
# game.player.party.append(bulbasaur1)
# game.player.party.append(charmander1)
# game.player.party.append(squirtle1) 
# game.TEST_OPPONENT.append(bulbasaur2)     
# game.TEST_OPPONENT.append(charmander2)


# #print(game.data.items['REPEL'])




# game.run()
# pygame.quit()