# David Lanza
# GPT-4 7-15-2023
# starting by asking gpt how to structure a game,
# so i can manage the structure and "glue" and
# asked gpt to design smaller pieces

import time
import csv
import pygame
import json
import math
import pytmx
import random





class Move: 
    ## change this to take parameters:
    ## base data, instance data?
    def __init__(self, id, internal_name, name, function_code, base_damage, type, category, accuracy, total_pp, 
                 effect_chance, target, priority, flags, description):
        self.id = id
        self.internal_name = internal_name
        self.name = name
        self.function_code = function_code
        self.base_damage = int(base_damage)
        self.type = type
        self.category = category
        self.accuracy = int(accuracy)
        self.total_pp = int(total_pp)
        self.effect_chance = int(effect_chance)
        self.target = target
        self.priority = int(priority)
        self.flags = flags
        self.description = description

    def create_moves(move_data):
        move_objects = {}
        for id, data in move_data.items():
            move = Move(id, **data)
            move_objects[id] = move
        return move_objects


class Game:   ###############    MAIN CLASS!
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("pokemon_pixel_font.ttf", 38) # try different font variables, fonts, sizes,...
        self.running = True
        self.state_stack = []
        self.data = GameData()
        self.save = SaveData()
        self.player = Player(self, self.save.PLAYER_AREA, self.save.PLAYER_POS, self.save.PLAYER_DIRECTION) # pass game and save data into here...

        
        
        self.wild_pokemon = []
        self.TEST_OPPONENT = []         
        
        self.my_save_data = None
        #self.load_game("save_data.json")
        ## load player position and area
        ## load list of game checkpoints, and which were reached
        ## load player team, player box storage
        ## load player preferences
        ## load bag items
        ## 
        
        

        self.state_stack.append(TitleScreenState(self))

        
    #def generate_pokemon(self, species, level, item=None, instance_data=None): # add instance data for your own pkmn
        ## Create a new Pokemon of the specified species and level
        #base_data = self.data.pokemon_data[species]
        #new_pokemon = Pokemon(base_data, self.data.sprites, level, item)
        #return new_pokemon    
        

    def push_state(self, state):
        self.state_stack.append(state)

    def pop_state(self):
        return self.state_stack.pop()

    def switch_state(self, state):
        if self.state_stack:
            self.state_stack.pop()
        self.state_stack.append(state)

    # Create a method to load wild Pokemon and opposing teams from game data
    #def load_encounter(self, encounter_data):
    #    self.wild_pokemon = [Pokemon.from_dict(d) for d in encounter_data['wild_pokemon']]
    #    self.opposing_team = [Pokemon.from_dict(d) for d in encounter_data['opposing_team']]    


    def run(self):
        while self.running and self.state_stack:
            state = self.state_stack[-1] # is -1 the last index?
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            try:
                next_state = state.handle_events(events)
                if next_state is not state and next_state is not None:  # if state wants to switch to a new state
                    self.push_state(next_state)
            except PopState:  # if state wants to exit
                self.pop_state()
            state.update()
            [state.draw(self.screen) for state in self.state_stack] # trying to draw the overworld when in the pause screen.
            pygame.display.flip()
            time.sleep(.05) ## this is dt, store it in the game options or save data class
        pygame.quit()



class GameData:
    def __init__(self):
        self.pokemon_data = self.load_pokemon_data('PBS/pokemon.txt')
        self.move_data = self.load_move_data('PBS/moves.txt')
        self.abilities_data = self.load_abilities_data('PBS/abilities.txt')
        self.sprites = Sprites()
        self.items = ItemLoader.load_items('PBS/items.txt')

        
    def load_pokemon_data(self, filename):
        pokemon_data = {'by_number': {}, 'by_name': {}}
        with open(filename) as file:
            for line in file:
                if line.strip() and line[0] != '#':  # Ignore blank lines and comments
                    if line.startswith('['):  # New Pokemon entry
                        PokedexNumber = line.strip('[]\n')
                        current_pokemon_data = {}
                        pokemon_data['by_number'][PokedexNumber] = current_pokemon_data
                    else:  # Data for current Pokemon
                        key, value = map(str.strip, line.split('='))
                        current_pokemon_data[key] = value
                        if key == 'InternalName':
                            pokemon_data['by_name'][value] = current_pokemon_data
        return pokemon_data    
    
    def load_move_data(self, filename):
        move_data = {}
        with open(filename, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                #print(row)
                id = row[0]
                move_data[id] = {
                    'InternalName': row[1],
                    'Name': row[2],
                    'FunctionCode': row[3],
                    'BaseDamage': row[4],
                    'Type': row[5],
                    'Category': row[6],
                    'Accuracy': row[7],
                    'TotalPP': row[8],
                    'EffectChance': row[9],
                    'Target': row[10],
                    'Priority': row[11],
                    'Flags': row[12],
                    'Description': row[13]
                }
        return move_data
    
    def load_abilities_data(self, filename):
        ## need to fix and remove the line breaks and special characters in this text file.
        abilities_data = {}
        with open(filename) as file:
            for line in file:
                ability = line.split(',')
                abilities_data[ability[1]]=ability
        return abilities_data
    
    def load_item_data(self, filename):
        pass
    
    
class SaveData:
    def __init__(self, filename = None):
        ## if filename is not None: call load_data() to open filename.txt and load these save items. 
        ## __init__ this class with default values for a new game!
        ## maybe if filename is None, name a new save file with the date-time in the name so that it can't overwrite an old file?
        self.TILE_ZOOM = 1.5 # control the size of the window by specifying how big the tiles are. sprites are 16x16 px. Can we use 1.5? or must it be an integer?
        self.TEXTBOX_BORDER = None # this should correlate with the decorative text box border. "None" will be pygame.draw.rect, others we will implement later..
        self.GAME_SPEED = .05 # seconds between frames
        self.PLAYER_AREA = TiledMap('pilot_town.tmx') # specific map file that the player was in when they last saved the game
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
        self.TILE_ZOOM = 1.5 
        self.TEXTBOX_BORDER = None 
        self.GAME_SPEED = .05 
        self.PLAYER_AREA = TiledMap('pilot_town.tmx') 
        self.PLAYER_POS = [50,50] 
        self.PLAYER_DIRECTION = "D" 
        self.PLAYER_SPRITES = game.data.sprites.NPCSprites[1] 
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


class Pokemon: # one instance of this class is one instance of a Pokemon.
    def __init__(self, base_data, instance_data):
        ## need to do for this class:
        ## -change to this structure: self.PROPERTY = instance_data.get('Property',base_data.get('Property'))
        ## goal: 
        ## this class is finished when i can generate any level wild pokemon of any species, catch it, change it with battle or something, and load it back from save.
        # base_data: 
        # https://essentialsengine.miraheze.org/wiki/Defining_a_species
        self.internal_name = base_data.get('InternalName') # species
        self.name = instance_data.get('Name',self.internal_name) # nickname
        self.type1 = base_data.get('Type1')
        self.type2 = base_data.get('Type2', None)
        self.base_stats = base_data.get('BaseStats').split(',')
        self.base_stats = [int(x) for x in self.base_stats] # HP / Attack / Defense / Speed / Special Attack / Special Defense 
        self.gender_rate = base_data.get('GenderRate')
        self.growth_rate = base_data.get('GrowthRate')
        self.base_exp = base_data.get('BaseEXP') # used to calculate how much XP you gain when defeating this pokemon
        self.effort_points = base_data.get('EffortPoints').split(',')
        self.effort_points = [int(x) for x in self.effort_points]
        self.rareness = base_data.get('Rareness')
        self.happiness = instance_data.get('Happiness',base_data.get('Happiness'))
        #     ?
        self.Abilities = base_data.get('Abilities')
        self.HiddenAbility = base_data.get('HiddenAbility')
        self.LearnedMoves = base_data.get('Moves')
        self.EggMoves = base_data.get('EggMoves',"") # or should it be None rather than ""?
        
        self.Height = base_data.get('Height')
        self.Weight = base_data.get('Weight')
        self.Color = base_data.get('Color')
        self.Shape = base_data.get('Shape')
        self.RegionalNumbers = base_data.get('RegionalNumbers')
        self.Kind = base_data.get('Kind')
        self.Pokedex = base_data.get('Pokedex')
        self.Evolutions = base_data.get('Evolutions', None)
        self.IV = instance_data.get('IV','0,0,0,0,0,0').split(',')
        self.IV = [int(x) for x in self.IV]
        self.EV = instance_data.get('EV','0,0,0,0,0,0').split(',')
        self.EV = [int(x) for x in self.EV]
        self.ability_index = instance_data.get('Ability_Index',1) # randbetween(1,num_abilities) else choose a random 1 from the viable options
        #self.ability = ability[self.ability_index]
        self.gender = instance_data.get('Gender','choose randomly from gender choices')
        self.nature = instance_data.get('Nature','1.1,1,1,1,1,.9').split(',')
        self.nature = [float(x) for x in self.nature]
        self.shiny = instance_data.get('Shiny', 'choose from random chance of shiny')
        self.form = instance_data.get('Form',0)
        self.happiness = instance_data.get('Happiness')
        self.StepsToHatch = instance_data.get('stepstohatch',base_data.get('stepstohatch',0))
        
        self.level = int(instance_data.get('Level'))
        self.calc_stats()
        self.reset_battle_stats()
        self.current_HP = instance_data.get('currenthp',self.totalhp)
        
        self.status = instance_data.get('status', 'NONE')
        self.status_count = int(instance_data.get('status_count','0'))


        # this should look up the info from instance_data and create up to 4 Move objects using the provided data. 
        # otherwise it should take the 4 last learned moves and instantiate those with full PP        
        self.moves = []
        self.pokeball = instance_data.get('pokeball','pokeball')
        self.item = instance_data.get('item', None) 
        

        self.Front_Sprite = game.data.sprites.FrontSprites[int(self.RegionalNumbers)-1]
        self.Back_Sprite = game.data.sprites.BackSprites[int(self.RegionalNumbers)-1]
        self.Box_Sprite = game.data.sprites.BoxSprites[int(self.RegionalNumbers)-1] 
             
        ## to do:
        # _ fix order of pokemon sprites compared to the pokemon data
        # X make it so i can create a pokemon object by giving the name rather than the number
        # X maybe make it so i can create a pokemon with as much info as i want, passed into the function input

        
    def reset_battle_stats(self):
        # use the 'current' stats for buffs and debuffs in battle.
        self.current_attack = self.attack
        self.current_defense = self.defense
        self.current_spatk = self.spatk
        self.current_spdef = self.spdef
        self.current_speed = self.speed
            
    def generate_pokemon(species, instance_data): # add instance data for your own pkmn
        # Create a new Pokemon of the specified species and level
        base_data = game.data.pokemon_data['by_name'][species]
        new_pokemon = Pokemon(base_data, instance_data)
        return new_pokemon    
    
    def calc_stats(self):
        # recalculate the stats using level, EV, IV, etc. upon generation, leveling, use of certain items, evolution, etc.
        self.totalhp = math.floor(0.01 * (2 * self.base_stats[0] + self.IV[0] + math.floor(0.25 * self.EV[0])) * self.level) + self.level + 10 
        self.attack = math.floor((math.floor(0.01 * (2 * self.base_stats[1] + self.IV[1] + math.floor(0.25 * self.EV[1])) * self.level) + 5) * self.nature[1])
        self.defense = math.floor((math.floor(0.01 * (2 * self.base_stats[2] + self.IV[2] + math.floor(0.25 * self.EV[2])) * self.level) + 5) * self.nature[2])
        self.spatk = math.floor((math.floor(0.01 * (2 * self.base_stats[3] + self.IV[3] + math.floor(0.25 * self.EV[3])) * self.level) + 5) * self.nature[3])
        self.spdef = math.floor((math.floor(0.01 * (2 * self.base_stats[4] + self.IV[4] + math.floor(0.25 * self.EV[4])) * self.level) + 5) * self.nature[4])
        self.speed = math.floor((math.floor(0.01 * (2 * self.base_stats[5] + self.IV[5] + math.floor(0.25 * self.EV[5])) * self.level) + 5) * self.nature[5])        
    
    def get_initial_moves(self):
        # This method should return the list of moves that a wild Pokemon of this species
        # and level should know. You will need to implement this.
        pass

    def get_initial_experience(self):
        # This method should return the amount of experience that a wild Pokemon of this
        # species and level should have. You will need to implement this.
        pass
    
    # Create a method that generates a dictionary from a Pokemon
    def to_dict(self):
        return self.__dict__    
    
    def evolve(self):
        pass# ask gpt some interesting ways to phrase questions so that it understands better. if you put a slash between words does it automatically understand that i mean the .. common  aspects of those words..?
        
    
    def gain_exp(self,EXP):
        pass
    # check if this amount of experience gets you to the next level.
    # if so, call gain_level(self)
    
    def gain_level(self):
        pass
    # recalculate stats
    # check if pokemon learns a move or evolves.
    
    def heal(self):
        pass
    # pokemon center heal: hp, status, PP
    
    
    def Test(self):
        pass # print or display all of the info for the pokemon
    
    
    # test:
    # charmander = Pokemon(base_data, Sprites, 5, instance_data=None, item="ORANBERRY")
    # instance_data = nickname, xp, ev, happiness, abilities, moves, nature, level, item, 
    # current_hp,

class Item:
    def __init__(self, item_id, internal_name, display_name, plural_name, pocket_id, price, description, field_usage, battle_usage, battle_target):
        self.item_id = int(item_id)
        self.internal_name = internal_name
        self.display_name = display_name
        self.plural_name = plural_name
        self.pocket_id = int(pocket_id)
        self.price = int(price)
        self.description = description
        self.field_usage = int(field_usage)
        self.battle_usage = int(battle_usage)
        self.battle_target = int(battle_target)

    #def __str__(self):
        #return f"{self.display_name}: {self.description}"

class ItemLoader:
    @staticmethod
    def load_items(filename):
        items = {}
        with open(filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                # Assuming the first column of each row is the item ID
                internal_name = row[1]
                items[internal_name] = {
                    "item_id": row[0],
                    "internal-name": row[1],
                    "display_name": row[2],
                    "plural_name": row[3],
                    "pocket_id": row[4],
                    "price": row[5],
                    "description": row[6],
                    "field_usage": row[7], # ???
                    "battle_usage": row[8], # ???
                    "battle_target": row[9], # ???
                }
        return items

        

class GameState:
    def __init__(self, game):
        pass

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

class PopState(Exception):
    def __init__(self):
        print("*pop!*")
    
class TitleScreenState(GameState):
    def __init__(self, game):
        super().__init__(game)
        print("Title Screen")
        self.title_image = pygame.image.load('title_image.png')  # replace with your image path
        

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    return OverworldState(game)  # Go to the overworld if the first option is selected
                else:
                    return None  # Otherwise, do nothing
        return None

    def update(self):
        # update game state
        pass

    def draw(self, screen):
        # draw the title screen
        screen.fill((70,30,0))
        screen.blit(self.title_image, (-40, 100))  # draws the image at the top-left corner




        
class PauseState(GameState):
    def __init__(self, game):
        super().__init__(game)
        # Add any specific variables for this state
        print("Pause State!")
        self.option_selected = 0
        self.options = ["POKEDEX","POKEMON","BAG","AR GEAR","SAVE","OPTIONS","QUIT"]
        self.colors = [(50,50,50),(255,255,255)] # option colors

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.option_selected = (self.option_selected + 1) % len(self.options)  # Cycle through options
                elif event.key == pygame.K_UP:
                    self.option_selected = (self.option_selected - 1) % len(self.options)  # Cycle through options
                elif event.key == pygame.K_z:
                    raise PopState #return None #OverworldState()
                elif event.key == pygame.K_x:
                    if self.option_selected == 0:
                        return PokedexState(game)  # 
                    elif self.option_selected == 1:
                        return PartyState(game)
                    elif self.option_selected == 2:
                        return BagState(game)
                    elif self.option_selected == 3:
                        return ARGearState(game)
                    elif self.option_selected == 4:
                        return SaveState(game)
                    elif self.option_selected == 5:
                        return OptionsState(game)
                    elif self.option_selected == 6:
                        return QuitState(game)                    
                    else:
                        return None  # Otherwise, do nothing
        return None

    def update(self):
        # update where the selector arrow is displayed?
        return None

    def draw(self, screen):
        # Draw the menu options, highlighting the one that's selected
        pygame.draw.rect(screen,(150,150,150),(600,20,180,560))
        
        # MAKE THIS NICERLY CODED
        #menu = [game.font.render("", True, self.colors[0]),game.font.render("", True, self.colors[0]),game.font.render("", True, self.colors[0]),game.font.render("", True, self.colors[0]),game.font.render("", True, self.colors[0]),game.font.render("", True, self.colors[0]),game.font.render("", True, self.colors[0])]
        menu = [None, None, None, None, None, None, None]
        for i in range(0,len(self.options)):
            if self.option_selected == i:
                menu[i] = game.font.render(self.options[i], True, self.colors[1])
            else:
                menu[i] = game.font.render(self.options[i], True, self.colors[0])
            screen.blit(menu[i], (620, 40+(80*i)))
        

class PokedexState(GameState):
    def __init__(self, game):
        super().__init__(game)
        print("pokedex")
        self.bg = pygame.transform.scale(pygame.image.load('bg_list_over_search.png'), (int(512*1.5625), int(384*1.5625)))
        self.selected = 1 # ID number selected and shown
        self.List_slots = ["-----","-----","-----","-----","-----","-----","-----","-----","-----","-----"]
        # data to load:
        # pokemon seen, pokemon caught, name, sprite, flavor text,...
        #print(game.data.pokemon_data['1'])
        
    def UpdateList(self):
        self.List_slots[0] = game.data.pokemon_data[str(self.selected+0)]['Name']
        self.List_slots[1] = game.data.pokemon_data[str(self.selected+1)]['Name']
        self.List_slots[2] = game.data.pokemon_data[str(self.selected+2)]['Name']
        self.List_slots[3] = game.data.pokemon_data[str(self.selected+3)]['Name']
        self.List_slots[4] = game.data.pokemon_data[str(self.selected+4)]['Name']
        self.List_slots[5] = game.data.pokemon_data[str(self.selected+5)]['Name']
        self.List_slots[6] = game.data.pokemon_data[str(self.selected+6)]['Name']
        self.List_slots[7] = game.data.pokemon_data[str(self.selected+7)]['Name']
        self.List_slots[8] = game.data.pokemon_data[str(self.selected+8)]['Name']
        self.List_slots[9] = game.data.pokemon_data[str(self.selected+9)]['Name']

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected+1) % len(game.data.pokemon_data)
                elif event.key == pygame.K_UP:
                    self.selected = (self.selected-1) if (self.selected != 1) else len(game.data.pokemon_data)-len(self.List_slots)
                elif event.key == pygame.K_LEFT:
                    self.selected = max(0,(self.selected-4)) # change this to scroll 1 page - 1 entry
                elif event.key == pygame.K_RIGHT:
                    self.selected = min(150,(self.selected+4)) # change this to scroll 1 page - 1 entry
                elif event.key == pygame.K_z:
                    raise PopState # return PauseState(game) 
                elif event.key == pygame.K_x:
                    pass
        return None

    def update(self):
        # update where the selector arrow is displayed
        self.UpdateList()
        return None

    def draw(self, screen):
        # Draw!
        screen.fill((230, 230, 230))
        screen.blit(self.bg, (0,0))
        Selected_name = game.font.render('Current Pokemon!', True, (255, 255, 255))  # White text
        #List_slots = ["-----","-----","-----","-----","-----","----","-----","-----","-----","-----"]
        List_names = [game.font.render(NAME, True, (30, 30, 30)) for NAME in self.List_slots]
        for i in range(0,len(List_names)):
            screen.blit(List_names[i], (500, 40+52*i)) # 80
        screen.blit(Selected_name, (40, 40))


class PartyState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.selected = 0
        print("party")
        
        self.bg_img = pygame.transform.scale(pygame.image.load('PartyScreens/bg.png'), (800, 600))
         # 1.5625
        self.slot1_bg = pygame.transform.scale(pygame.image.load(  \
            'PartyScreens/panel_round.png'), (int(156*1.5625), int(98*1.5625))) # slot 1 on the left is bigger than the rest
        
        self.slots_bg = pygame.transform.scale(pygame.image.load( \
            'PartyScreens/panel_rect.png'), (int(288*1.5625), int(48*1.5625))) # blue panel bg for slots with pokemon in them
        
        self.slot1_s_bg = pygame.transform.scale(pygame.image.load( \
            'PartyScreens/panel_round_sel.png'), (int(156*1.5625), int(98*1.5625))) # slot 1 when selected
        
        self.slots_s_bg = pygame.transform.scale(pygame.image.load( \
            'PartyScreens/panel_rect_sel.png'), (int(288*1.5625), int(48*1.5625)))  # other slots when selected
        
        self.icon_ball = pygame.transform.scale(pygame.image.load( \
            'PartyScreens/icon_ball.png'), (int(44*1.5625), int(56*1.5625))) # closed pokeball icon
        
        self.icon_s_ball = pygame.transform.scale(pygame.image.load( \
            'PartyScreens/icon_ball_sel.png'), (int(44*1.5625), int(56*1.5625))) # open pokeball icon, for when selected
        
        self.healthbar = pygame.transform.scale(pygame.image.load( \
            'PartyScreens/overlay_hp_back.png'), (int(138*1.5625), int(14*1.5625))) # image of an empty healthbar
        
        self.cancel = pygame.transform.scale(pygame.image.load( \
            'PartyScreens/icon_cancel.png'), (int(112*1.5625), int(36*1.5625))) # image of an empty healthbar
        
        self.cancel_s = pygame.transform.scale(pygame.image.load( \
            'PartyScreens/icon_cancel_sel.png'), (int(112*1.5625), int(36*1.5625))) # image of an empty healthbar
        
        
        self.party = []
        self.party_images = []
        self.slot_icons = []
        for i in range(0,len(game.player.party)):
            self.party.append(game.player.party[i])
            self.party_images.append(self.party[i].Box_Sprite)
            self.slot_icons.append(pygame.transform.scale(self.party_images[i], (int(38*1.5625), int(38*1.5625))))
            


    def handle_events(self, events):
        num_pokemon = len(self.party)  # Assuming you have a list called pokemon_list
    
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.selected == 0:
                        self.selected=6
                    elif self.selected < num_pokemon-1:  # Only increment if below the number of actual Pokemon
                        self.selected += 1
                    elif self.selected == 6:
                        self.selected = 0
                    else:
                        self.selected = 6  # Wrap around to the first Pokemon
    
                elif event.key == pygame.K_UP:
                    if self.selected==6:
                        self.selected=num_pokemon-1
                    elif self.selected > 0:
                        self.selected -= 1
                    else:
                        self.selected = 6#num_pokemon-1  # Wrap around to the last Pokemon or cancel button
    
                elif event.key == pygame.K_LEFT:
                    self.selected = 0
    
                elif event.key == pygame.K_RIGHT:
                    if self.selected == 0 and num_pokemon > 1:
                        self.selected = 1
    
                elif event.key == pygame.K_z:
                    raise PopState 
    
                elif event.key == pygame.K_x:
                    if self.selected == 6:  # If Cancel button (which is one past the last Pokemon)
                        raise PopState 
                    else:
                        return PartyDetailState(game, self.selected)  # Enter party detail state for this Pokemon
    
        return None
    


    def update(self): # ?
        return None

    def drawSlot(self, screen, slot):
        if slot==0:
            if self.selected == 0:
                screen.blit(self.slot1_s_bg, (28, 95))
                screen.blit(self.icon_s_ball, (10, 70)) # need open pokeball icon
            else:
                screen.blit(self.slot1_bg, (28, 95))
                screen.blit(self.icon_ball, (10, 70))
            screen.blit(self.healthbar, (54, 187))  # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(104,193,150,9))
            pygame.draw.rect(screen,[140,220,150],(104,193,150,3))       
            slot_name1 = game.font.render("Test1", True, [230,230,230])
            screen.blit(slot_name1, (100,140))   
            slot_lv1 = game.font.render("Test1", True, [230,230,230])
            screen.blit(slot_lv1, (100,170))  
            slot_hp1 = game.font.render("Test1", True, [230,230,230])
            screen.blit(slot_hp1, (160,210))
            screen.blit(self.slot_icons[0], (50,100)) # 1
            
        elif slot==1:
            if self.selected == 1:
                screen.blit(self.slots_s_bg, (347, 46))
                screen.blit(self.icon_s_ball, (317, 40))
            else:
                screen.blit(self.slots_bg, (347, 46))
                screen.blit(self.icon_ball, (317, 40))
            screen.blit(self.healthbar, (575, 70)) # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(625,76,150,9))
            pygame.draw.rect(screen,[140,220,150],(625,76,150,3))  
            slot_name2 = game.font.render("Test2", True, [230,230,230])
            screen.blit(slot_name2, (450,70))       
            slot_lv2 = game.font.render("Test2", True, [230,230,230])
            screen.blit(slot_lv2, (450,100))     
            slot_hp2 = game.font.render("Test2", True, [230,230,230])
            screen.blit(slot_hp2, (700,100))
            screen.blit(self.slot_icons[1], (330,70)) # 2
            
        elif slot==2:
            if self.selected == 2:
                screen.blit(self.slots_s_bg, (347, 141))
                screen.blit(self.icon_s_ball, (317, 135))
            else:
                screen.blit(self.slots_bg, (347, 141))
                screen.blit(self.icon_ball, (317, 135))
            screen.blit(self.healthbar, (575, 165)) # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(625,171,150,9))
            pygame.draw.rect(screen,[140,220,150],(625,171,150,3))    
            slot_name3 = game.font.render("Test3", True, [230,230,230])
            screen.blit(slot_name3, (450,165))    
            slot_lv3 = game.font.render("Test3", True, [230,230,230])
            screen.blit(slot_lv3, (450,195))            
            slot_hp3 = game.font.render("Test3", True, [230,230,230])
            screen.blit(slot_hp3, (700,195))
            screen.blit(self.slot_icons[2], (330,165)) # 3
            
        elif slot==3:
            if self.selected == 3:
                screen.blit(self.slots_s_bg, (347, 235))
                screen.blit(self.icon_s_ball, (317, 229))
            else:
                screen.blit(self.slots_bg, (347, 235))
                screen.blit(self.icon_ball, (317, 229))
            screen.blit(self.healthbar, (575, 259)) # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(625,265,150,9))
            pygame.draw.rect(screen,[140,220,150],(625,265,150,3))    
            slot_name4 = game.font.render("Test4", True, [230,230,230])
            screen.blit(slot_name4, (450,259))   
            slot_lv4 = game.font.render("Test4", True, [230,230,230])
            screen.blit(slot_lv4, (450,289))         
            slot_hp4 = game.font.render("Test4", True, [230,230,230])
            screen.blit(slot_hp4, (700,289))
            screen.blit(self.slot_icons[3], (330,260)) # 4
            
        elif slot==4:
            if self.selected == 4:
                screen.blit(self.slots_s_bg, (347, 328))
                screen.blit(self.icon_s_ball, (317, 322))
            else:
                screen.blit(self.slots_bg, (347, 328))
                screen.blit(self.icon_ball, (317, 322))
            screen.blit(self.healthbar, (575, 352)) # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(625,358,150,9))
            pygame.draw.rect(screen,[140,220,150],(625,358,150,3))     
            slot_name5 = game.font.render("Test5", True, [230,230,230])
            screen.blit(slot_name5, (450,352))      
            slot_lv5 = game.font.render("Test5", True, [230,230,230])
            screen.blit(slot_lv5, (450,382))     
            slot_hp5 = game.font.render("Test5", True, [230,230,230])
            screen.blit(slot_hp5, (700,382))
            screen.blit(self.slot_icons[4], (330,355)) # 5
            
        elif slot==5:
            if self.selected == 5:
                screen.blit(self.slots_s_bg, (347, 421))
                screen.blit(self.icon_s_ball, (317, 415))
            else:
                screen.blit(self.slots_bg, (347, 421))
                screen.blit(self.icon_ball, (317, 415))
            screen.blit(self.healthbar, (575, 445)) # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(625,451,150,9))
            pygame.draw.rect(screen,[140,220,150],(625,451,150,3))   
            slot_name6 = game.font.render("Test6", True, [230,230,230])
            screen.blit(slot_name6, (450,445))             
            slot_lv6 = game.font.render("Test6", True, [230,230,230])
            screen.blit(slot_lv6, (450,475))  
            slot_hp6 = game.font.render("Test6", True, [230,230,230])
            screen.blit(slot_hp6, (700,475))   
            screen.blit(self.slot_icons[5], (330,450)) # 6   
            
        elif slot==6:
            if self.selected == 6:
                screen.blit(self.cancel_s, (617, 514))
                screen.blit(self.icon_s_ball, (587, 501))
            else:
                screen.blit(self.cancel, (617, 514))
                screen.blit(self.icon_ball, (587, 501))
                
    def draw(self, screen):
        numPK = len(game.player.party) # number of pokemon in your party
        screen.blit(self.bg_img, (0, 0))
        for i in range(0,numPK):
            self.drawSlot(screen, i)
        self.drawSlot(screen,6)




class BagState(GameState):
    def __init__(self, game):
        super().__init__(game)
        # D:\MyPythonShit\GPT Pokemon\Graphics\Pictures\Bag
        print("bag")
        self.bg = "D:\MyPythonShit\GPT Pokemon\Graphics\Pictures\Bag\bg_m.png"
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
                    OverworldState(game).draw(game.screen)
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

class SaveState(GameState):
    def __init__(self, game):
        super().__init__(game)
        print("SAVE")

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
                    pass
                elif event.key == pygame.K_x:
                    pass
        return None

    def update(self):
        # update where the selector arrow is displayed
        return None

    def draw(self, screen):
        # Draw!
        pygame.draw.rect(screen,(150,150,150),(50,0,20,30))

class OptionsState(GameState):
    def __init__(self, game):
        super().__init__(game)
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

class PartyDetailState(GameState):
    def __init__(self, game, index, card=0):
        super().__init__(game)
        self.selected = index
        self.pkmn = game.player.party[self.selected]
        self.bg1 = pygame.transform.scale(pygame.image.load('PartyScreens/bg_1.png'), (int(512*1.5625), int(384*1.5625)))
        self.bg2 = pygame.transform.scale(pygame.image.load('PartyScreens/bg_2.png'), (int(512*1.5625), int(384*1.5625)))
        self.bg3 = pygame.transform.scale(pygame.image.load('PartyScreens/bg_3.png'), (int(512*1.5625), int(384*1.5625)))
        self.bg4 = pygame.transform.scale(pygame.image.load('PartyScreens/bg_4.png'), (int(512*1.5625), int(384*1.5625)))
        self.bg5 = pygame.transform.scale(pygame.image.load('PartyScreens/bg_5.png'), (int(512*1.5625), int(384*1.5625)))
        print("party detail")
        self.pkmnSprite = pygame.transform.scale(self.pkmn.Front_Sprite, (int(80*2.5*1.5625), int(80*2.5*1.5625)))
        # card is the left/right switching info cards.
        self.card = card


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected+1)%len(game.player.party)
                    game.pop_state()
                    return PartyDetailState(game, self.selected,self.card)
                elif event.key == pygame.K_UP:
                    self.selected = self.selected-1 if self.selected>0 else len(game.player.party)-1
                    game.pop_state()
                    return PartyDetailState(game, self.selected,self.card)
                elif event.key == pygame.K_LEFT:
                    self.card = self.card-1 if self.card>0 else 3
                    game.pop_state()
                    return PartyDetailState(game, self.selected,self.card)
                elif event.key == pygame.K_RIGHT:
                    self.card = (self.card+1) % 4
                    game.pop_state()
                    return PartyDetailState(game, self.selected,self.card)
                elif event.key == pygame.K_z:
                    raise PopState #return PauseState()
                elif event.key == pygame.K_x:
                    pass
        return None

    def update(self):
        # update where the selector arrow is displayed
        return None

    def draw(self, screen):
        # Draw!
        if self.card==0:
            screen.fill((0, 0, 100))
            screen.blit(self.bg1, (0,0))
            level = game.font.render(str(self.pkmn.level), True, (100, 100, 100))  # White text
            screen.blit(level, (272, 545))             
            level = game.font.render(str(self.pkmn.level), True, (255, 255, 255))  # White text
            screen.blit(level, (270, 543))   
            name = game.font.render(self.pkmn.name, True, (100, 100, 100))  # White text
            screen.blit(name, (32, 402))                   
            name = game.font.render(self.pkmn.name, True, (255, 255, 255))  # White text
            screen.blit(name, (30, 400))
            
        elif self.card==1:
            #screen.fill((100, 0, 0))
            screen.blit(self.bg2, (0,0))
            level = game.font.render(str(self.pkmn.level), True, (100, 100, 100))  # White text
            screen.blit(level, (272, 545))             
            level = game.font.render(str(self.pkmn.level), True, (255, 255, 255))  # White text
            screen.blit(level, (270, 543))   
            name = game.font.render(self.pkmn.name, True, (100, 100, 100))  # White text
            screen.blit(name, (32, 402))                   
            name = game.font.render(self.pkmn.name, True, (255, 255, 255))  # White text
            screen.blit(name, (30, 400))   
            
            hp = game.font.render(str(self.pkmn.current_HP) + "  /  " + str(self.pkmn.totalhp), True, (50, 50, 50))  # White text
            screen.blit(hp, (460, 180))        
            attack = game.font.render(str(self.pkmn.attack), True, (50, 50, 50))  # White text
            screen.blit(attack, (460, 230))
            defense = game.font.render(str(self.pkmn.defense), True, (50, 50, 50))  # White text
            screen.blit(defense, (460, 280))
            spatt = game.font.render(str(self.pkmn.spatk), True, (50, 50, 50))  # White text
            screen.blit(spatt, (730, 180))
            spdef = game.font.render(str(self.pkmn.spdef), True, (50, 50, 50))  # White text
            screen.blit(spdef, (730, 230))
            spd = game.font.render(str(self.pkmn.speed), True, (50, 50, 50))  # White text
            screen.blit(spd, (730, 280))      
            
        elif self.card==2:
            #screen.fill((0, 100, 0))
            screen.blit(self.bg3, (0,0))
            level = game.font.render(str(self.pkmn.level), True, (100, 100, 100))  # White text
            screen.blit(level, (272, 545))             
            level = game.font.render(str(self.pkmn.level), True, (255, 255, 255))  # White text
            screen.blit(level, (270, 543))   
            name = game.font.render(self.pkmn.name, True, (100, 100, 100))  # White text
            screen.blit(name, (32, 402))                   
            name = game.font.render(self.pkmn.name, True, (255, 255, 255))  # White text
            screen.blit(name, (30, 400))            
        elif self.card==3:
            #screen.fill((100, 0, 100))
            screen.blit(self.bg4, (0,0))    
            level = game.font.render(str(self.pkmn.level), True, (100, 100, 100))  # White text
            screen.blit(level, (272, 545))             
            level = game.font.render(str(self.pkmn.level), True, (255, 255, 255))  # White text
            screen.blit(level, (270, 543))   
            name = game.font.render(self.pkmn.name, True, (100, 100, 100))  # White text
            screen.blit(name, (32, 402))                   
            name = game.font.render(self.pkmn.name, True, (255, 255, 255))  # White text
            screen.blit(name, (30, 400))            
        elif self.card==4:
            #screen.fill((100, 0, 100))
            screen.blit(self.bg5, (0,0))      
            level = game.font.render(str(self.pkmn.level), True, (100, 100, 100))  # White text
            screen.blit(level, (272, 545))             
            level = game.font.render(str(self.pkmn.level), True, (255, 255, 255))  # White text
            screen.blit(level, (270, 543))   
            name = game.font.render(self.pkmn.name, True, (100, 100, 100))  # White text
            screen.blit(name, (32, 402))                   
            name = game.font.render(self.pkmn.name, True, (255, 255, 255))  # White text
            screen.blit(name, (30, 400))            
        screen.blit(self.pkmnSprite, (15,90))


class BattleState(GameState):
    def __init__(self, player, opponent):
        super().__init__(game)
        self.party = player.party
        self.opponent_team = opponent
        self.current_player_pokemon = self.party[0]
        self.current_opponent_pokemon = self.opponent_team[0]
        self.turn_order = []  # This will be used to determine who attacks first in each turn
        pokemon_font = pygame.font.Font(None, 36)
        self.text_box = [] # Textbox()
        self.running = True
        self.battlestack = [] # 
        
        self.bg = pygame.transform.scale(pygame.image.load("grass_bg.png"), (int(800), int(600)))
        self.opponent_base = pygame.transform.scale(pygame.image.load("path_base1.png"), (int(256*1.5625), int(128*1.5625))) 
        self.opponent_data_box = pygame.transform.scale(pygame.image.load("databox_normal_foe.png"), (int(260*1.5625), int(62*1.5625))) 
        self.player_data_box = pygame.transform.scale(pygame.image.load("databox_normal.png"), (int(260*1.5625), int(84*1.5625)))
    
    def draw_opp_health(self, screen, pkmn):
        location = [210,87]
        hp = pkmn.current_HP/pkmn.totalhp
        if hp<.1:
            color = [[200,60,50],[220,150,150]]
        elif hp<.5:
            color = [[200,200,50],[220,220,150]]
        else:
            color = [[60,200,50],[140,220,150]]
        pygame.draw.rect(screen,color[0],(location[0],location[1],150*hp,7))
        pygame.draw.rect(screen,color[1],(location[0],location[1],150*hp,3))      
        
    def draw_player_health(self, screen, pkmn):
        location = [588,363]
        hp = pkmn.current_HP/pkmn.totalhp
        if hp<.1:
            color = [[200,60,50],[220,150,150]]
        elif hp<.5:
            color = [[200,200,50],[220,220,150]]
        else:
            color = [[60,200,50],[140,220,150]]        
        pygame.draw.rect(screen,[60,200,50],(location[0],location[1],150,6))
        pygame.draw.rect(screen,[140,220,150],(location[0],location[1],150,3))       
        
    def handle_events(self, events):
        # Handle events, such as player input. This will likely be a complex method
        # and will involve checking the current state of the battle to determine
        # what actions are available, and then acting on the player's input.
        while self.running:
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            #self.screen.fill((0, 0, 0))  # fill screen with black
            self.draw(game.screen)
            #pygame.display.flip()

        ## GPT4's answer when i told it to organize the info i found on the battle system into a usable form
        # Initialize an empty list for the action queue
        action_queue = []
        
        # Add actions to action_queue based on player choices
        # ...
        
        # Sort the action queue
        def sort_action_queue(action_queue):
            # Handle switches, Pursuit, rotations first
            # Handle Mega Evolution flag
            # Sort by move priority
            action_queue.sort(key=lambda x: x.move.priority, reverse=True)
            # Handle Quick Claw, Quick Draw, Custap Berry
            # Handle Full Incense, Lagging Tail, Stall
            # Handle Mycelium Might
            # Sort by Speed Stat (consider Trick Room)
            if trick_room_effect:
                action_queue.sort(key=lambda x: x.pokemon.speed)
            else:
                action_queue.sort(key=lambda x: x.pokemon.speed, reverse=True)
            # Handle ties
        # Execute actions in the sorted action_queue
        def execute_actions(action_queue):
            for action in action_queue:
                action.execute()

    ########################################
    
    ########################################


    def start_battle(self):
        pass # maybe eliminate (self) here? load pokemon, reset battle stats,
             # instantiate health bars, sprites, textbox,... print text, animate pokemon, etc.
    

    def calculate_damage(self, attacking_pokemon, defending_pokemon, move):
        # Logic to calculate damage dealt by a move
        damage = (((((2*level/5)+2)*power*attack/defense)/50)*burn*screen*targets*weather*FF+2)*stockpile*critical*doubleDamage*charge*HH*STAB*Type*random
        return damage

    def apply_damage(self, defending_pokemon, damage):
        # Apply damage to a Pokemon, taking into account health limits
        pass

    def check_for_fainted(self):
        # Check if a Pokemon has fainted and handle switching out
        pass

    def check_for_end_of_battle(self):
        # Check if all Pokemon on one side have fainted
        pass
    
    def execute_turn(self):
        # Execute each Pokemon's move in the correct order
        pass



    def update(self):
        # Update the state of the battle. This could involve things like applying
        # damage, checking if a Pokemon has fainted, handling switches, etc.
        #battle.calculate_turn_order()
        #battle.execute_turn()
        #battle.check_for_fainted()
        #battle.check_for_end_of_battle() 
        pass

    # def draw(self, screen):
        # Draw the battle screen. This would involve drawing the backgrounds, the
        # player and opponent sprites, the health bars of the Pokemon, etc.
    

    def draw(self, screen):
        screen.fill((255, 255, 255))  # Fill the screen with baked beans
        screen.blit(self.bg, (0, 0))
        # Set up some fonts
        
        # draw background
        # draw health bars
        screen.blit(self.opponent_data_box, (25, 25))
        self.draw_opp_health(screen, self.opponent_team[0])
        screen.blit(self.player_data_box, (375, 300))
        self.draw_player_health(screen, self.party[0]) # 360
             
        # draw sprites
        screen.blit(self.opponent_team[0].Front_Sprite, (550, 50))
        screen.blit(self.party[0].Back_Sprite, (50, 350))
        # draw effects
        # draw textbox
        pygame.display.flip()
    
        #1-start battle
        #2-abilities like Intimidate
        #2-weather
        #3-choose your move or action
        #4-calculate move priority (note that some abilities affect some move priorities)
        #5-pursuit?
        #5-quick claw, custap berry, o-powers
        #6-switch pokemon,rotating, using items, escaping battle, charging msg for focus punch, beak blast, shell trap
        #7-execute moves
        
        #?-note that X is asleep or X woke up
        
        
    


class TextboxState(GameState):
    def __init__(self, message, screen_width, screen_height, font):
        self.message = message
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font        
        self.border = 40
        self.lines = self.split_message_into_lines(message, font)
        #print(self.lines)
        self.current_line = 0
        self.text_typing_index = 0
        self.typing_speed = 50  # ms per character
        self.fast_typing_speed = 5  # ms per character
        self.is_typing_fast = False
        self.last_typing_time = pygame.time.get_ticks()
        self.fin_flag = False
        self.border_style = pygame.transform.scale(pygame.image.load('choice 1.png'), (int(48*1.5625), int(48*1.5625)))

        self.box_height = screen_height // 3
        self.box_rect = pygame.Rect(0, screen_height - self.box_height, screen_width, self.box_height)
        
    def draw_box_rect(self, screen, rect):
        # The assumption is that the border's width and height are both 10 pixels
        BORDER_SIZE = 24
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        
        # Corners
        top_left = self.border_style.subsurface((0, 0, BORDER_SIZE, BORDER_SIZE))
        top_right = self.border_style.subsurface((self.border_style.get_width() - BORDER_SIZE, 0, BORDER_SIZE, BORDER_SIZE))
        bottom_left = self.border_style.subsurface((0, self.border_style.get_height() - BORDER_SIZE, BORDER_SIZE, BORDER_SIZE))
        bottom_right = self.border_style.subsurface((self.border_style.get_width() - BORDER_SIZE, self.border_style.get_height() - BORDER_SIZE, BORDER_SIZE, BORDER_SIZE))
        
        # Edges
        top = self.border_style.subsurface((BORDER_SIZE, 0, self.border_style.get_width() - 2*BORDER_SIZE, BORDER_SIZE))
        bottom = self.border_style.subsurface((BORDER_SIZE, self.border_style.get_height() - BORDER_SIZE, self.border_style.get_width() - 2*BORDER_SIZE, BORDER_SIZE))
        left = self.border_style.subsurface((0, BORDER_SIZE, BORDER_SIZE, self.border_style.get_height() - 2*BORDER_SIZE))
        right = self.border_style.subsurface((self.border_style.get_width() - BORDER_SIZE, BORDER_SIZE, BORDER_SIZE, self.border_style.get_height() - 2*BORDER_SIZE))
        
        # Center (this will be repeated to fill the inside of the box)
        center = self.border_style.subsurface((BORDER_SIZE, BORDER_SIZE, self.border_style.get_width() - 2*BORDER_SIZE, self.border_style.get_height() - 2*BORDER_SIZE))
        
        # Draw corners
        screen.blit(top_left, (x, y))
        screen.blit(top_right, (x + w - BORDER_SIZE, y))
        screen.blit(bottom_left, (x, y + h - BORDER_SIZE))
        screen.blit(bottom_right, (x + w - BORDER_SIZE, y + h - BORDER_SIZE))
        
        # Draw edges
        for i in range(BORDER_SIZE, w - BORDER_SIZE, top.get_width()):
            screen.blit(top, (x + i, y))
            screen.blit(bottom, (x + i, y + h - BORDER_SIZE))
        for i in range(BORDER_SIZE, h - BORDER_SIZE, left.get_height()):
            screen.blit(left, (x, y + i))
            screen.blit(right, (x + w - BORDER_SIZE, y + i))
        
        # Fill center
        for i in range(BORDER_SIZE, w - BORDER_SIZE, center.get_width()):
            for j in range(BORDER_SIZE, h - BORDER_SIZE, center.get_height()):
                screen.blit(center, (x + i, y + j))

    def split_message_into_lines(self, message, font):
        # Split the message into words and then reconstruct the lines based on the font width
        words = message.split(" ")
        lines = []
        current_line = []
        for word in words:
            if font.size(' '.join(current_line + [word]))[0] > (self.screen_width-self.border*2):
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
        lines.append(' '.join(current_line))
        return lines
    

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                #if self.fin_flag:
                    #game.pop_state()
                if self.is_text_finished_typing():
                    self.advance_to_next_line()
                else:
                    self.is_typing_fast = True
            # get keys pressed
            # if X is pressed, self.is_typing_fast = True
            # else: self.is_typing_fast = False

    def is_text_finished_typing(self):
        return self.text_typing_index >= len(self.lines[max(self.current_line-1,0)])

    def advance_to_next_line(self):
        self.text_typing_index = 0
        self.current_line += 1
        if self.current_line >= len(self.lines):
            # You could pop this state from the stack to return to the underlying state
            #self.fin_flag = True
            game.pop_state()
            pass

    #def update(self): # , dt) old
        #current_time = pygame.time.get_ticks()
        #typing_speed = self.fast_typing_speed if self.is_typing_fast else self.typing_speed
        #if current_time - self.last_typing_time > typing_speed:
            #if not self.is_text_finished_typing():
                #self.text_typing_index += 1
                #self.last_typing_time = current_time
                
    def update(self): 
        #print(self.lines[self.current_line][:self.text_typing_index])
        #print(self.text_typing_index)
        speed1 = 1
        speed2 = 3
        if self.is_typing_fast:
            speed = speed2
        else:
            speed = speed1   
            #print(self.is_text_finished_typing())
        if not self.is_text_finished_typing():
            self.text_typing_index += speed

    def draw(self, screen):
        #pygame.draw.rect(screen, (255, 255, 255), self.box_rect)
        self.draw_box_rect(screen, self.box_rect)
        # Compute the starting position for the text
        x = self.border
        y1 = self.screen_height - self.box_height + self.border
        y2 = y1 + int(self.screen_height/6)-self.border/2

        # Display the current line
        
        if self.current_line == 0:
            line1_text = self.lines[self.current_line][:self.text_typing_index]
            line1_text = line1_text + "_"
            line2_text = ""
           
        else:
            line1_text = self.lines[self.current_line-1]
            line2_text = self.lines[self.current_line][:self.text_typing_index]
            line2_text = line2_text + "_"



        line1_surf = self.font.render(line1_text, True, (0, 0, 0))
        screen.blit(line1_surf, (x, y1))
        
        line2_surf = self.font.render(line2_text, True, (0, 0, 0))
        screen.blit(line2_surf, (x, y2))   

        ## If there's a next line, display it too
        #if self.current_line + 1 < len(self.lines):
            #next_line_text = self.lines[self.current_line + 1]
            #text_surface = self.font.render(next_line_text, True, (0, 0, 0))
            #screen.blit(text_surface, (x, y + self.font.get_height()))

        # Display the underscore if needed
        #if self.current_line + 1 < len(self.lines) or not self.is_text_finished_typing():
            #underscore_surface = self.font.render("_", True, (0, 0, 0))
            #screen.blit(underscore_surface, (x + self.font.size(line1_text)[0], y))



class OverworldState(GameState):
    def __init__(self, game):
        super().__init__(game)
        # Initialize player, NPC positions etc. here
        print("overworld state")
        self.current_area = game.player.area ######################################### TiledMap('pilot_town.tmx') 
        # load player position, player object, npc positions and objects, items
        # self.pos = game.player.position #[25,20] # use this to get map offset?
        self.TempSurf = pygame.Surface((800, 600))
        self.arrow_stack = []
        self.NPCs = []
        self.NPCs.append(NPC(game, game.player.area, [76,71],"D"))
    
    def handle_events(self, events): 
        # clean the arrow key inputs and call self.player.handle_input at the right times, 
        # i.e. after taking a step if the button is still held down, etc.
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    game.player.handle_input("D")
                    #print("D")
                elif event.key == pygame.K_UP:
                    game.player.handle_input("U")
                    #print("U")
                elif event.key == pygame.K_LEFT:
                    game.player.handle_input("L")
                    #print("L")
                elif event.key == pygame.K_RIGHT:
                    game.player.handle_input("R")
                    #print("R")
                elif event.key == pygame.K_x:
                    pass # self.player.handle_input("x")
                elif event.key == pygame.K_z:
                    pass # self.player.handle_input("z")? do i need this here?
                elif event.key == pygame.K_b:
                    return BattleState(game.player, game.TEST_OPPONENT)    ######################             
                elif event.key == pygame.K_p:
                    return PauseState(game)
                elif event.key == pygame.K_t:
                    msg = "This is a public service announcement, this is only a test. Peter Piper Picked a Peck of Pickled Peppers. Oh Potatoes and Molasses!!"
                    return TextboxState(msg, 800, 600, game.font)                
                else:
                    pass
        if keys[pygame.K_DOWN] and game.player.direction=="D":
            game.player.handle_input("D")
            #print("d")
        elif keys[pygame.K_UP] and game.player.direction=="U":
            game.player.handle_input("U")
            #print("u")
        elif keys[pygame.K_LEFT] and game.player.direction=="L":
            game.player.handle_input("L")
            #print("l")
        elif keys[pygame.K_RIGHT] and game.player.direction=="R":
            game.player.handle_input("R")
            #print("r")
        else:
            game.player.handle_input("*")                


    def update(self):
        # Update player and NPC sprites if walking, update NPC locations, update map position, etc.
        game.player.update() 
        # check doors?
        self.new_area(game.player.area.check_doors(game.player.position))
        for NPC in self.NPCs:
            NPC.update()


    def draw(self, screen):
        # Draw the game world
        screen.fill((0, 0, 0))  # Fill the screen with black before drawing
        self.TempSurf.fill((0, 0, 0))
        game.player.area.draw_map(self.TempSurf, game.player.position) # need self.pos because it draws the local tiles
        for NPC in self.NPCs:
            NPC.draw(self.TempSurf, game.player.position)
        screen.blit(self.TempSurf, (0,0))
        game.player.draw(screen)
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
            game.player.area = TiledMap(area) 
            self.NPCs = []
            game.player.position = pos
            game.player.direction = direction
            # fade in
            # make the player walk 1 space through the door.. or walk to the center of the elevator and turn around.. etc.
    
        
class Sprites:
    def __init__(self):
        self.Front_Sprites_File = "FrontSprites.png" # 80x80 sprites, arranged 18x28
        self.Back_Sprites_File = "BackSprites.png"
        self.NPC_Sprites_File = "NPC_sprites.png"
        self.Box_Sprites_File = "Box_sprites.png"
        self.front_size = (125,125) # (80,80)
        self.back_size = (100,100) # (64,64)
        self.tile_size = (16,16)
        self.NPC_size = (16,22)
        self.Box_size = (38,38)
        
        self.Front_Spritesheet = pygame.transform.scale(pygame.image.load(self.Front_Sprites_File).convert_alpha(), (int(2240*1.5625), int(1440*1.5625)))  
        self.FrontSprites = self.load_sprites(self.Front_Spritesheet,self.front_size) 
        self.FrontSprites = [item for sublist in self.FrontSprites for item in sublist]
        
        self.Back_Spritesheet = pygame.transform.scale(pygame.image.load(self.Back_Sprites_File).convert_alpha(), (int(1600*1.5625), int(1024*1.5625)))  
        self.BackSprites = self.load_sprites(self.Back_Spritesheet,self.back_size)        
        self.BackSprites = [item for sublist in self.BackSprites for item in sublist]
        
        self.NPC_Spritesheet = pygame.image.load(self.NPC_Sprites_File).convert_alpha()
        self.NPCSprites = self.load_sprites(self.NPC_Spritesheet,self.NPC_size)
        
        self.Box_Spritesheet = pygame.image.load(self.Box_Sprites_File).convert_alpha()
        self.BoxSprites = self.load_sprites(self.Box_Spritesheet,self.Box_size)#[0]
        self.BoxSprites = [item for sublist in self.BoxSprites for item in sublist]


    def load_sprites(self,spritesheet,sprite_size):
        sprites = []
        #print(spritesheet.get_height())
        #print(spritesheet.get_width())
        for y in range(0, spritesheet.get_height(), sprite_size[1]):
            row = []
            for x in range(0, spritesheet.get_width(), sprite_size[0]):
                sprite = spritesheet.subsurface(pygame.Rect(x, y, sprite_size[0], sprite_size[1]))
                row.append(sprite)
            sprites.append(row)
        return sprites
    
    def character_sprites(self,spritesheet,sprite_size,row):
        # it appears to be 2 frames per sprite,
        # and the player takes 1 step per grid tile.
        size = spritesheet.get_size()
        # Create a list of lists to hold the frames. Each sublist will
        # represent a direction of movement.
        frames = []
    
        for i in range(4):  # For each direction...
            direction_frames = []
            for j in range(WALK_FRAMES):  # For each frame...
                # Subsurface the sprite sheet to get the frame.
                rect = pygame.Rect(j * sprite_size[0], i * sprite_size[1], sprite_size[0], sprite_size[1])
                frame = sprite_sheet.subsurface(rect)
                direction_frames.append(frame)
            frames.append(direction_frames)
        return frames    


class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.print_layer_info()


    def draw_map(self, TempSurf, pos): # draw onto TempSurf
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    if abs(pos[0]-x) < 50 and abs(pos[0]-x) >= 0 and abs(pos[1]-y) < 38 and abs(pos[1]-y) >= 0: # 50, 38
                        TempSurf.blit(image, ((x-pos[0]+25) * self.tmxdata.tilewidth, (y-pos[1]+20) * self.tmxdata.tileheight))
        
  
    def print_layer_info(self):
        for i, layer in enumerate(self.tmxdata.layers):
            if hasattr(layer, 'tiles'):  # Check if the layer is a tile layer
                pass #print(f"Layer number: {i}, Layer name: {layer.name}")        

    def check_collision(self, x, y, layer=1, direction = "*"):
        """Returns True if the tile at (x, y) in the specified layer is a wall."""
        if direction=="U":
            y=y-1
        elif direction=="D":
            y=y+1
        elif direction=="L":
            x=x-1
        elif direction=="R":
            x=x+1
        else:
            pass
        try:
            tile = self.tmxdata.get_tile_properties(x-25, y-20, layer)
            if tile is not None:
                return True
        except Exception as e:
            pass
        # also check for NPCs and other things!
        #print("no collision found")
        return False
    
    def check_doors(self, pos):
        for obj in self.tmxdata.objects: # does self.tmxdata.objects exist by default?
            if obj.name == "door":
                x, y, width, height = obj.x/16, obj.y/16, obj.width, obj.height
                # Check if your player's position intersects with this rectangle
                if pos[0] >= x and pos[0] < (x+obj.width/16) and pos[1] >= y and pos[1] < (y+obj.height/16):
                    #print("DOOR!!")
                    area_info = {}
                    area_info["area"] = obj.properties['door']  
                    stance = obj.properties['stance'].split(',')
                    #print(stance)
                    area_info["pos"] = [int(stance[0]),int(stance[1])] # save this in the map file..
                    area_info["direction"] = stance[2]
                    area_info["NPC_List"] = []
                    return area_info
        return None
    
    def check_actions(self, x, y, layer=2, direction = "*"):
        """Returns True if the tile at (x, y) in the specified layer is a wall."""
        if direction=="U":
            y=y-1
        elif direction=="D":
            y=y+1
        elif direction=="L":
            x=x-1
        elif direction=="R":
            x=x+1
        else:
            pass
        try:
            for obj in self.tmxdata.objects: # does self.tmxdata.objects exist by default?
                if obj.name == "door":
                    x, y, width, height = obj.x/16, obj.y/16, obj.width, obj.height
                    # Check if your player's position intersects with this rectangle
                    if pos[0] >= x and pos[0] < (x+obj.width/16) and pos[1] >= y and pos[1] < (y+obj.height/16):
                        area_info = {}
                        area_info["area"] = obj.properties['door']  
                        stance = obj.properties['stance'].split(',')
                        area_info["pos"] = [int(stance[0]),int(stance[1])] # save this in the map file..
                        area_info["direction"] = stance[2]
                        area_info["NPC_List"] = []
                        return area_info
                    elif pos[0] >= x and pos[0] < (x+obj.width/16) and pos[1] >= y and pos[1] < (y+obj.height/16):
                        pass # check for items, messages, functions, etc. and NPCs as well.
                    else:
                        pass
            return None
        except Exception as e:
            pass
        # also check for NPCs and other things!
        #print("no collision found")
        return None        
        # also check for NPCs and other things!
        #print("no collision found")
        #return None   

    def check_grass(self, pos):
        for obj in self.tmxdata.objects: # does self.tmxdata.objects exist by default?
            if obj.name == "grass":
                x, y, width, height = obj.x/16, obj.y/16, obj.width, obj.height
                # Check if your player's position intersects with this rectangle
                if pos[0] >= x and pos[0] < (x+obj.width/16) and pos[1] >= y and pos[1] < (y+obj.height/16):
                    if random.random() > .1:
                        print("BATTLE!!!")
                        #print(obj.properties)
                        #area_info = {}
                        #area_info["area"] = obj.properties['door']  
                        #stance = obj.properties['stance'].split(',')
                        #print(stance)
                        #area_info["pos"] = [int(stance[0]),int(stance[1])] # save this in the map file..
                        #area_info["direction"] = stance[2]
                        #area_info["NPC_List"] = []
                        #return area_info
        return None

class NPC:
    def __init__(self, game, area, position, direction, name=None): # self, current area?
        self.game = game
        self.position = position
        self.direction = direction
        self.area = area   # map
        self.speed = .25
        self.moving = False
        self.walk = ["D","D","D","D","L","L","U","U","U","U","R","R"]
        self.walk_count = 0
        self.sprites = game.data.sprites.NPCSprites[3]
        self.frame_counter = 0
        self.sprite_update_rate = 2   
        self.sprite_index = 0
        self.anim_sprites = [0,3,0,4]
        self.current_sprite = self.sprites[self.sprite_index]

    def execute_walk(self, walk):
        self.direction = self.walk[self.walk_count]
        self.moving = True
        self.walk_count = self.walk_count+1
        if self.walk_count > len(self.walk)-1:
            self.walk_count=0

     
    def turn(self,direction):
        if direction == "U":
            self.anim_sprites = [1,5,1,6]
        elif direction == "D":
            self.anim_sprites = [0,3,0,4]
        elif direction == "L":
            self.anim_sprites = [2,7,2,8]
        elif direction == "R":    
            self.anim_sprites = [10,9,10,11]
        else:
            pass   
        self.sprite_index = 0
        self.current_sprite = self.sprites[self.anim_sprites[self.sprite_index]]
      
    
    def move_towards_next_tile(self,direction): 
        if direction == "U" and self.moving:
            self.position[1] = self.position[1]-self.speed
        elif direction == "D" and self.moving:
            self.position[1] = self.position[1]+self.speed
        elif direction == "L" and self.moving:
            self.position[0] = self.position[0]-self.speed
        elif direction == "R" and self.moving:
            self.position[0] = self.position[0]+self.speed
        else:
            pass
        self.frame_counter += 1
        if self.frame_counter >= self.sprite_update_rate:
            self.sprite_index = (self.sprite_index + 1) % 4
            self.current_sprite = self.sprites[self.anim_sprites[self.sprite_index]]
            self.frame_counter = 0

    
    def draw(self, TempSurf,player_pos):
        W = 16 # tile width
        H = 22 # tile height
        POS = ((self.position[0]-player_pos[0])*self.area.tmxdata.tilewidth, (self.position[1]-player_pos[1])*self.area.tmxdata.tileheight-(H-W))
        TempSurf.blit(self.current_sprite, POS) #(400, 300))
    
    def reached_center_of_tile(self):
        if ((self.position[0]%1==0) and (self.position[1]%1==0)):
            return True
        else:
            return False    
            
    
    def update(self): ########################################################################
        # moving and COLLISION DETECTION!
        if not self.reached_center_of_tile():
            # if the character is moving and not yet at the center of a tile, keep moving.
            self.move_towards_next_tile(self.direction)
            if self.reached_center_of_tile():
                self.moving = False
        elif self.reached_center_of_tile():
            self.execute_walk(self.walk)#######################
            self.turn(self.direction)
            if (not self.area.check_collision(self.position[0],self.position[1],direction=self.direction)) and (self.direction in ["U","D","L","R"]) and self.moving:
                self.move_towards_next_tile(self.direction)
            else:
                self.moving = False    
    
    #def update(self): ########################################################################
        ## moving and COLLISION DETECTION!
        #if not self.reached_center_of_tile():
            #pass # keep moving and animating
        #else:
            #pass # if self.direction in [u,d,l,r]:
                   ##  turn(direction)
                      ## if no collisions(direction)
                          ## 
    
    
    
    
class Player(NPC):
    def __init__(self, game, area, position, direction, moving=False): #self, area?         
        super().__init__(game, area, position, direction) # , game, area, position, direction
        self.sprites = game.data.sprites.NPCSprites[game.save.PLAYER_SPRITES]
        self.party = []
        self.boxed_pokemon = []        

    def draw(self, screen):
        W = 16 # tile width
        H = 22 # tile height
        screen.blit(self.current_sprite, (400, 300+2*(H-W)))

    def handle_input(self, direction):
        if direction in ["U", "D", "L", "R"] and not self.moving:
            self.direction = direction
            self.moving = True

    #def update(self): 
        ## moving and COLLISION DETECTION!
        #direc = self.direction
        #if not self.reached_center_of_tile():
            ## if the character is moving and not yet at the center of a tile, keep moving.
            #self.move_towards_next_tile(direc)
            #if self.reached_center_of_tile():
                #direc = "*"
                #self.moving = False
        #elif self.reached_center_of_tile():
            #self.turn(direc)
            #if (not self.area.check_collision(self.position[0]+25,self.position[1]+20,direction=direc)) and (direc in ["U","D","L","R"]) and self.moving:
                #self.move_towards_next_tile(direc)
            #else:
                #self.moving = False
    
    def update(self): 
        # moving and COLLISION DETECTION!
        if not self.reached_center_of_tile():
            # if the character is moving and not yet at the center of a tile, keep moving.
            self.move_towards_next_tile(self.direction)
            if self.reached_center_of_tile():
                self.moving = False
        elif self.reached_center_of_tile():
            self.turn(self.direction)
            if (not self.area.check_collision(self.position[0]+25,self.position[1]+20,direction=self.direction)) and (self.direction in ["U","D","L","R"]) and self.moving:
                self.move_towards_next_tile(self.direction)
            else:
                self.moving = False    
            


game = Game()


# Create Pokemon objects
bulbasaur1_instance = {'Level':5}
bulbasaur1 = Pokemon.generate_pokemon('BULBASAUR', bulbasaur1_instance)  # Level 5 Bulbasaur

charmander1_instance = {'Level':5}
charmander1 = Pokemon.generate_pokemon('CHARMANDER', charmander1_instance)  # Level 5 Charmander

squirtle1_instance = {'Level':5}
squirtle1 = Pokemon.generate_pokemon('SQUIRTLE', squirtle1_instance) # Level 5 Squirtle

bulbasaur2_instance = {'Level':4}
bulbasaur2 = Pokemon.generate_pokemon('BULBASAUR', bulbasaur2_instance)  # Level 4 Bulbasaur

charmander2_instance = {'Level':4}
charmander2 = Pokemon.generate_pokemon('CHARMANDER', charmander2_instance)  # Level 4 Charmander

# Add Bulbasaur to the player's party and Charmander to the opponent's party
game.player.party.append(bulbasaur1)
game.player.party.append(charmander1)
game.player.party.append(squirtle1) 
game.TEST_OPPONENT.append(bulbasaur2)     
game.TEST_OPPONENT.append(charmander2)


#print(game.data.items['REPEL'])




game.run()
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