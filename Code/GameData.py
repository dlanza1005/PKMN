import csv

# this class should:
#   -load the data from the PBS text files, and fill in the proper data structures


class GameData:
    def __init__(self):
        self.pokemon_data = self.load_pokemon_data('PBS/pokemon.txt')
        self.move_data = self.load_move_data('PBS/moves.txt')
        self.abilities_data = self.load_abilities_data('PBS/abilities.txt')
        self.item_data = 0
        self.items = self.load_item_data('PBS/items.txt')
        self.types = self.load_types_data('PBS/types.txt')
        
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
    
    def load_types_data(self,filename):
        PKMNtypes = {}
        with open(filename, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            for row in reader:
                # 
                pass
        return PKMNtypes

game_data = GameData()