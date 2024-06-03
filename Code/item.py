from Sprites import sprites
from GameData import game_data

class Item: # items as structured to be used in the Bag screen, which is most common.
    def __init__(self, data):
        self.item_id = int(data["item_id"])
        self.internal_name = data["internal_name"]
        self.display_name = data["display_name"]
        self.plural_name = data["plural_name"]
        self.pocket_id = int(data["pocket_id"])
        self.price = int(data["price"])
        self.description = data["description"]
        self.field_usage = int(data["field_usage"])
        self.battle_usage = int(data["battle_usage"])
        self.battle_target = int(data["battle_target"])
        self.Item_Icon = sprites.Item_Icons[self.item_id]

def generate_item(name):
    data = game_data.items[name]
    return Item(data)

    # i forget what this was for. was it for converting to save?
    #def __str__(self):
        #return f"{self.display_name}: {self.description}"


# item_id, internal_name, display_name, plural_name, pocket_id, price, description, field_usage, battle_usage, battle_target