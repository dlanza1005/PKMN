import math
from Sprites import sprites
from GameData import game_data

# This class should:
#   -create an instance of a pokemon given certain information. retrieve from base, retrieve from instance (saved) data, calculate, or generate anything thats not specified.
#   -contain all of the data needed for the pokemon including sprites.
#   -be able to collapse the entire pokemon object into a string or dict or something, to send to the save file. also, be able to re-instantiate the pokemon exactly as it was
#   -functions to heal, gain xp, grow level, learn moves, evolve, faint,
class Pokemon: # one instance of this class is one instance of a Pokemon.
    def __init__(self, base_data, instance_data):
        ## to do:
        # _ fix order of pokemon sprites compared to the pokemon data
        # _ create a set list of pokemon parameters to be generated or loaded from instance_data
        # _ create a way to load and save instances of pokemon using a dictionary or string or json file

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
        self.LearnedMoves = self.parse_moves(base_data.get('Moves'))
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
        self.moves = self.get_initial_moves()
        self.pokeball = instance_data.get('pokeball','pokeball')
        self.item = instance_data.get('item', None) 

        self.Front_Sprite = sprites.FrontSprites[int(self.RegionalNumbers)-1] # game.data.sprites.FrontSprites[int(self.RegionalNumbers)-1]
        self.Back_Sprite = sprites.BackSprites[int(self.RegionalNumbers)-1] # game.data.sprites.BackSprites[int(self.RegionalNumbers)-1]
        self.Box_Sprite = sprites.BoxSprites[int(self.RegionalNumbers)-1] # game.data.sprites.BoxSprites[int(self.RegionalNumbers)-1] 
             



    def parse_moves(self,moves_string):
        # Split the string by commas
        parts = moves_string.split(',')
        # Initialize an empty dictionary to store moves
        moves_dict = {}
        # Iterate through the list, stepping by 2 to get pairs of (level, move)
        for i in range(0, len(parts) - 1, 2):
            level = int(parts[i])
            move = parts[i + 1]
            moves_dict[level] = move
        return moves_dict
        
    def reset_battle_stats(self):
        # use the 'current' stats for buffs and debuffs in battle.
        self.current_attack = self.attack
        self.current_defense = self.defense
        self.current_spatk = self.spatk
        self.current_spdef = self.spdef
        self.current_speed = self.speed
            
    def generate_pokemon(species, instance_data): # add instance data for your own pkmn
        # Create a new Pokemon of the specified species and level
        base_data = game_data.pokemon_data['by_name'][species]
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
        # iterates through the dict of learnable moves. if the pokemon meets the level criteria, add that move to a list.
        # afterward, pick the last 4 moves on the list as the default pick for wild pokemon
        moves = []
        for level in self.LearnedMoves:
            if self.level >= level:
                moves.append(self.LearnedMoves[level])
        return moves[-4:]

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