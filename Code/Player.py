import pygame
from NPC import NPC
from Sprites import sprites


class Player(NPC):
    def __init__(self, game, area, position, direction, moving=False): #self, area?         
        super().__init__(game, area, position, direction) # , game, area, position, direction
        self.game = game
        self.PX = self.game.save.PIXEL_SIZE
        self.W = self.PX*16*15 # (number of screen pixels per game pixel) * (16 game pixels per tile) * (screen is 15 tiles wide)
        self.H = self.PX*16*11 # (number of screen pixels per game pixel) * (16 game pixels per tile) * (screen is ~11 tiles tall)
        self.sprites = sprites.NPCSprites[game.save.PLAYER_SPRITES]
        self.sprites = [pygame.transform.scale(image, (16*self.PX, 22*self.PX)) for image in self.sprites]
        self.party = []
        self.boxed_pokemon = []

    def draw(self, screen):
        W = 16 * self.PX # tile width
        H = 22 * self.PX # tile height
        screen.blit(self.current_sprite, (int((self.W/2)-(W/2)), int((self.H/2)-((W)/2))-(H-W)))     #  int((self.H/2)-(H/2))

    def handle_input(self, direction):
        if direction in ["U", "D", "L", "R"] and not self.moving:
            self.direction = direction
            self.moving = True

###########################################
# collision detection should be stored in NPC class!
    
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