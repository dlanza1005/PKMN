import random
import pytmx
import pygame


class TiledMap:
    def __init__(self, game, filename):
        self.game=game
        self.PX = self.game.save.PIXEL_SIZE
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm
        self.print_layer_info()


    # def draw_map(self, TempSurf, pos): # draw onto TempSurf
    #     for layer in self.tmxdata.visible_layers:
    #         if isinstance(layer, pytmx.TiledTileLayer):
    #             for x, y, image in layer.tiles():
    #                 if abs(pos[0]-x) < 50 and abs(pos[0]-x) >= 0 and abs(pos[1]-y) < 38 and abs(pos[1]-y) >= 0: # 50, 38
    #                     TempSurf.blit(image, ((x-pos[0]+25) * self.tmxdata.tilewidth, (y-pos[1]+20) * self.tmxdata.tileheight))
    def draw_map(self, TempSurf, pos): # draw onto TempSurf
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    if abs(pos[0]-x) < 15 and abs(pos[0]-x) >= 0 and abs(pos[1]-y) < 11 and abs(pos[1]-y) >= 0: # 50, 38
                        image = pygame.transform.scale(image, (self.tmxdata.tilewidth*self.PX, self.tmxdata.tileheight*self.PX))
                        TempSurf.blit(image, ((x-pos[0]+7) * self.tmxdata.tilewidth*self.PX, (y-pos[1]+5) * self.tmxdata.tileheight*self.PX))
        #screen.blit(self.current_sprite, (int((self.W/2)-(W/2)), int((self.H/2)-(H/2))))
  
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
