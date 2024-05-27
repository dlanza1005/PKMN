# David Lanza
# GPT-4 7-15-2023
# starting by asking gpt how to structure a game,
# so i can manage the structure and "glue" and
# asked gpt to design smaller pieces

#import time
#import csv
import pygame
pygame.init()
#import json
#import math
#import pytmx
#import random
from SaveData import save_data
W = save_data.PIXEL_SIZE*16*15 # (number of screen pixels per game pixel) * (16 game pixels per tile) * (screen is 15 tiles wide)
H = int(save_data.PIXEL_SIZE*16*11.25) # (number of screen pixels per game pixel) * (16 game pixels per tile) * (screen is ~11 tiles tall)
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
dt = .05


#import ARGearState
#import BagState
#import BattleState
from Game import Game
#import GameData
#import GameState
#import item
#import ItemLoader
#import Move
#import NPC
#import OptionsState
#import OverworldState
#import PartyDetailState
#import PartyState
#import PauseState
#import Player
#import PokedexState
from Pokemon import Pokemon
#import SaveData
#import SaveState



# initialization
# create game, load state from save, create game objects, etc.

game = Game()


# Create Pokemon objects
bulbasaur1_instance = {'Level':5}
bulbasaur1 = Pokemon.generate_pokemon('BULBASAUR', bulbasaur1_instance)  # Level 5 Bulbasaur

charmander1_instance = {'Level':5}
charmander1 = Pokemon.generate_pokemon('CHARMANDER', charmander1_instance)  # Level 5 Charmander

squirtle1_instance = {'Level':15}
squirtle1 = Pokemon.generate_pokemon('SQUIRTLE', squirtle1_instance) # Level 15 Squirtle

pidgey1_instance = {'Level':5}
pidgey1 = Pokemon.generate_pokemon('PIDGEY', pidgey1_instance)  # Level 5 Bulbasaur

rattata1_instance = {'Level':5}
rattata1 = Pokemon.generate_pokemon('RATTATA', rattata1_instance)  # Level 5 Charmander

pikachu1_instance = {'Level':81}
pikachu1 = Pokemon.generate_pokemon('PIKACHU', pikachu1_instance) # Level 15 Squirtle

bulbasaur2_instance = {'Level':4}
bulbasaur2 = Pokemon.generate_pokemon('BULBASAUR', bulbasaur2_instance)  # Level 4 Bulbasaur

charmander2_instance = {'Level':4}
charmander2 = Pokemon.generate_pokemon('CHARMANDER', charmander2_instance)  # Level 4 Charmander

# Add Bulbasaur to the player's party and Charmander to the opponent's party
game.player.party.append(bulbasaur1)
game.player.party.append(charmander1)
game.player.party.append(squirtle1) 
game.player.party.append(pidgey1)
game.player.party.append(rattata1) 
game.player.party.append(pikachu1) 
game.TEST_OPPONENT.append(bulbasaur2)     
game.TEST_OPPONENT.append(charmander2)


#print(game.data.items['REPEL'])




game.run(screen,dt)
pygame.quit()

##### DO LIST #####
# zoom: change all graphics sizes and locations to scale with ZOOM
# fix PartyState slot drawing function to eliminate duplicate code
# standardize or fix import of PBS data:
#   pokemon: gamedata class function to open file and populate base_data dict, class to generate pokemon instances with that dict and instance data
#   item: gamedata class function to open file and populate item dict, class to access item properties when picking the item name from the bag list or something
#   move: gamedata class function to open file and populate moves dict, class to create move instance from this and PP/PP instance data
#   types: gamedata class function to open file and populate types dict, and also associate the colored TYPE image with it. that should be enough structure to use it in the game. 
# keep graphics in a graphics folder, keep PBS in a PBS folder, keep maps in a map folder, etc.