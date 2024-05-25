#from TiledMap import TiledMap
#from Sprites import sprites

class SaveData:
    def __init__(self, filename = None):
        ## if filename is not None: call load_data() to open filename.txt and load these save items. 
        ## __init__ this class with default values for a new game!
        ## maybe if filename is None, name a new save file with the date-time in the name so that it can't overwrite an old file?
        self.PIXEL_SIZE = 3 # control the size of the window by specifying how big the tiles are. sprites are 16x16 px. Can we use 1.5? or must it be an integer?
        self.TEXTBOX_BORDER = None # this should correlate with the decorative text box border. "None" will be pygame.draw.rect, others we will implement later..
        self.FONT_SIZE = 16 # px tall if
        self.GAME_SPEED = .05 # seconds between frames
        self.FONT = "pokemon_pixel_font.ttf"

        self.PLAYER_AREA = 'pilot_town.tmx' #TiledMap('pilot_town.tmx') # specific map file that the player was in when they last saved the game
        self.PLAYER_POS = [50,50] # tile location within self.PLAYER_AREA
        self.PLAYER_DIRECTION = "R" # U, D, L, or R denoting the direction the player is facing
        self.PLAYER_SPRITES = 1 # or just store as 1.
        
        self.PARTY = [] # list of up to 6 pokemon objects.
        self.BOX_PKMN = [] # list of all pokemon objects for pokemon caught and saved in the pokemon box.
        self.BAG = [] # list of bag items
        self.POKEDEX = [] # convey which pokemon are seen or caught. maybe store this as a dictionary with values as "no data", "seen", or "caught". or store this as a list of strings where the index is the pokemon number, and the value is "X","S","C"
        self.CHECKPOINTS = [] # this could be a binary list of checkpoints in the game, which specify which points have been reached. i.e. if you have to talk to a certain person before you can advance the story, reaching that checkpoint can tell the game to remove the blockade so you can walk to the next town..
        
    def load_data(self,filename):
        # pull these values from a text file. for now theyre hard coded.
        self.PIXEL_SIZE = 3 
        self.TEXTBOX_BORDER = None 
        self.FONT_SIZE = 16
        self.GAME_SPEED = .05 
        self.FONT = "pokemon_pixel_font.ttf"

        self.PLAYER_AREA = 'pilot_town.tmx' # TiledMap('pilot_town.tmx') 
        self.PLAYER_POS = [50,50] 
        self.PLAYER_DIRECTION = "D" 
        self.PLAYER_SPRITES = 1 # sprites.NPCSprites[1] 

        self.PARTY = [] 
        self.BOX_PKMN = [] 
        self.BAG = [] 
        self.POKEDEX = [] 
        self.CHECKPOINTS = []        
    
    ## old Load code:
    #def load_my_data(filename):
        #with open('save_file.json', 'r') as f:
            #save_data = json.load(f)
        
        #player.name = save_data["player"]["name"]
        #player.x, player.y = save_data["player"]["location"]
        #player.money = save_data["player"]["money"]
        #player.play_time = save_data["player"]["play_time"]
        
        #player.party = []
        #for pokemon_data in save_data["party_pokemon"]:
            #pokemon = Pokemon(pokemon_data["species"])
            #pokemon.level = pokemon_data["level"]
            #pokemon.current_health = pokemon_data["current_health"]
            #pokemon.moves = [moves[name] for name in pokemon_data["moves"]]
            #player.party.append(pokemon)
        
        # etc. for boxed_pokemon, pokedex, inventory, world_state, rng_seed
    
    ## old Save code:
    #def save_my_data(filename):
        #save_data = {
            #"player": {
                #"name": player.name,
                #"location": (player.x, player.y),
                #"money": player.money,
                #"play_time": player.play_time,
            #},
            #"party_pokemon": [
                #{
                    #"species": pokemon.species,
                    #"level": pokemon.level,
                    #"current_health": pokemon.current_health,
                    #"moves": [move.name for move in pokemon.moves],
                    # etc.
                #} for pokemon in player.party
            #],
            # etc. for boxed_pokemon, pokedex, inventory, world_state, rng_seed
        #}
        
        #with open('save_file.json', 'w') as f:
            #json.dump(save_data, f)   

save_data = SaveData()