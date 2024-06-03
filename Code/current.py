# David Lanza
# GPT-4  
# 7-15-2023
# starting by asking gpt how to structure a game,
# so i can manage the structure and "glue" and
# asked gpt to design smaller pieces


import pygame
pygame.init()

from SaveData import save_data
W = save_data.PIXEL_SIZE*16*15 # (number of screen pixels per game pixel) * (16 game pixels per tile) * (screen is 15 tiles wide)
H = int(save_data.PIXEL_SIZE*16*11.25) # (number of screen pixels per game pixel) * (16 game pixels per tile) * (screen is ~11 tiles tall)
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
dt = .05

from Game import Game
from Pokemon import Pokemon


# initialization
# create game, load state from save, create game objects, etc.

game = Game()


# Create Pokemon objects
bulbasaur1_instance = {'Level':5,"Nickname":"Barbara"}
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

# Add pokemon to the player and opponent's parties
game.player.party.append(bulbasaur1)
game.player.party.append(charmander1)
game.player.party.append(squirtle1) 
game.player.party.append(pidgey1)
game.player.party.append(rattata1) 
game.player.party.append(pikachu1) 
game.TEST_OPPONENT.append(bulbasaur2)     
game.TEST_OPPONENT.append(charmander2)


# # create items and add them to the bag
# potion = Item.generate_item('POTION')
# game.save.BAG.append(potion)
# game.save.BAG.append(potion)
# game.save.BAG.append(potion)
# game.save.BAG.append(potion)
# game.save.BAG.append(potion)

# repel = Item.generate_item('REPEL')
# game.save.BAG.append(repel)

# honey = Item.generate_item('HONEY')
# game.save.BAG.append(honey)

# nugget = Item.generate_item('NUGGET')
# game.save.BAG.append(nugget)

# heartscale = Item.generate_item('HEARTSCALE')
# game.save.BAG.append(heartscale)

# softsand = Item.generate_item('SOFTSAND')
# game.save.BAG.append(softsand)

# oranberry = Item.generate_item('ORANBERRY')
# game.save.BAG.append(oranberry)

# pokeball = Item.generate_item('POKEBALL')
# game.save.BAG.append(pokeball) 
# game.save.BAG.append(pokeball)
# game.save.BAG.append(pokeball) 
# game.save.BAG.append(pokeball)
# game.save.BAG.append(pokeball)

# yellowshard = Item.generate_item('YELLOWSHARD')
# game.save.BAG.append(yellowshard)

# redshard = Item.generate_item('REDSHARD')
# game.save.BAG.append(redshard)

# blueshard = Item.generate_item('BLUESHARD')
# game.save.BAG.append(blueshard)

game.save.BAG.append("POTION")
game.save.BAG.append("POTION")
game.save.BAG.append("POTION")
game.save.BAG.append("POTION")
game.save.BAG.append("POTION")
game.save.BAG.append("REPEL")
game.save.BAG.append("HONEY")
game.save.BAG.append("NUGGET")
game.save.BAG.append("HEARTSCALE")
game.save.BAG.append("SOFTSAND")
game.save.BAG.append("ORANBERRY")
game.save.BAG.append("POKEBALL")
game.save.BAG.append("POKEBALL")
game.save.BAG.append("POKEBALL")
game.save.BAG.append("POKEBALL")
game.save.BAG.append("POKEBALL")
game.save.BAG.append("YELLOWSHARD")
game.save.BAG.append("REDSHARD")
game.save.BAG.append("BLUESHARD")
game.save.BAG.append("GREENSHARD")
game.save.BAG.append("SUPERPOTION")

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

# add a way to load the game from a save file, and save the game to a save file. this will be the first step in creating a save/load system.
# remove garbage comments and code. keep the code clean and organized.
# use copilot to clean up PartyState
