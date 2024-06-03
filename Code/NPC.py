import pytmx
import pygame
from Sprites import sprites

class NPC:
    def __init__(self, game, area, position, direction, name=None): # self, current area?
        self.game = game
        self.position = position
        self.direction = direction
        self.PX = self.game.save.PIXEL_SIZE
        self.area = area   # map
        self.speed = .25*self.PX
        self.moving = False
        self.walk = ["D","D","D","D","L","L","U","U","U","U","R","R"]
        self.walk_count = 0
        self.sprites = sprites.NPCSprites[3]
        self.sprites = [pygame.transform.scale(image, (16*self.PX, 22*self.PX)) for image in self.sprites]
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

    
    def draw(self, TempSurf, player_pos):
        W = 16 # tile width
        H = 22 # tile height
        POS = ((self.position[0]-player_pos[0])*self.area.tmxdata.tilewidth, ((self.position[1]-player_pos[1])*self.area.tmxdata.tileheight-(H-W)))
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