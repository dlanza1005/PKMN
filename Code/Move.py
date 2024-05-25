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