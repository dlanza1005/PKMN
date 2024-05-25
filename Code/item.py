from Sprites import Sprites

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
        # ItemIcons

    # i forget what this was for. was it for converting to save?
    #def __str__(self):
        #return f"{self.display_name}: {self.description}"


