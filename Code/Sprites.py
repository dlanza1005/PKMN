import pygame
import os

class Sprites:
    def __init__(self):
        self.tile_size = (16,16)

        self.Front_Sprites_File = "FrontSprites.png" # 80x80 sprites, arranged 18x28
        self.front_size = (125,125) # (80,80)
        self.Front_Spritesheet = pygame.transform.scale(pygame.image.load(self.Front_Sprites_File).convert_alpha(), (int(2240*1.5625), int(1440*1.5625)))  
        self.FrontSprites = self.load_sprites(self.Front_Spritesheet,self.front_size) 
        self.FrontSprites = [item for sublist in self.FrontSprites for item in sublist]

        self.Back_Sprites_File = "BackSprites.png"
        self.back_size = (100,100) # (64,64)
        self.Back_Spritesheet = pygame.transform.scale(pygame.image.load(self.Back_Sprites_File).convert_alpha(), (int(1600*1.5625), int(1024*1.5625)))  
        self.BackSprites = self.load_sprites(self.Back_Spritesheet,self.back_size)        
        self.BackSprites = [item for sublist in self.BackSprites for item in sublist]

        self.NPC_Sprites_File = "NPC_sprites.png"
        self.NPC_size = (16,22)
        self.NPC_Spritesheet = pygame.image.load(self.NPC_Sprites_File).convert_alpha()
        self.NPCSprites = self.load_sprites(self.NPC_Spritesheet,self.NPC_size)

        self.Box_Sprites_File = "Box_sprites.png"
        self.Box_size = (38,38)
        self.Box_Spritesheet = pygame.image.load(self.Box_Sprites_File).convert_alpha()
        self.BoxSprites = self.load_sprites(self.Box_Spritesheet,self.Box_size)#[0]
        self.BoxSprites = [item for sublist in self.BoxSprites for item in sublist]

        self.Item_Icons_File = "ItemIcons/"
        self.Item_Icon_size = (48,48)
        self.Item_Icons = self.load_images_from_folder(self.Item_Icons_File)








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
                frame = sprite_sheet.subsurface(rect) # spritesheet?
                direction_frames.append(frame)
            frames.append(direction_frames)
        return frames    
    
    def load_images_from_folder(self,folder):
        images = []
        for filename in os.listdir(folder):
            if filename.endswith('.png'):
                image_path = os.path.join(folder, filename)
                try:
                    image = pygame.image.load(image_path)
                    images.append(image)
                except pygame.error as e:
                    print(f"Failed to load {filename}: {e}")
        return images

sprites = Sprites()

# import pygame
# import os
# import sys
# from GameData import game_data

# class Sprites:
#     def __init__(self):
#         pygame.init()
#         self.tile_size = (16,16)
#         self.FONT = "pokemon-emerald.ttf" # for troubleshooting
#         self.font = pygame.font.Font(self.FONT, 30) # for troubleshooting
#         # Set a temporary video mode to allow transformations
#         pygame.display.set_mode((1, 1), pygame.NOFRAME)

#         self.Front_Sprites_File = "FrontSprites.png" # 80x80 sprites, arranged 18x28
#         self.front_size = (125,125) # (80,80)
#         self.Front_Spritesheet = pygame.transform.scale(pygame.image.load(self.Front_Sprites_File).convert_alpha(), (int(2240*1.5625), int(1440*1.5625)))  
#         self.FrontSprites = self.load_sprites(self.Front_Spritesheet, self.front_size)
#         self.FrontSprites = [item for sublist in self.FrontSprites for item in sublist]
        
#         # Reorder the sprites here if needed
#         # Example: self.FrontSprites = self.FrontSprites[::-1]  # Reverse the list as an example

#         self.Back_Sprites_File = "BackSprites.png"
#         self.back_size = (100,100) # (64,64)
#         self.Back_Spritesheet = pygame.transform.scale(pygame.image.load(self.Back_Sprites_File).convert_alpha(), (int(1600*1.5625), int(1024*1.5625)))  
#         self.BackSprites = self.load_sprites(self.Back_Spritesheet, self.back_size)        
#         self.BackSprites = [item for sublist in self.BackSprites for item in sublist]

#         self.NPC_Sprites_File = "NPC_sprites.png"
#         self.NPC_size = (16,22)
#         self.NPC_Spritesheet = pygame.image.load(self.NPC_Sprites_File).convert_alpha()
#         self.NPCSprites = self.load_sprites(self.NPC_Spritesheet, self.NPC_size)

#         self.Box_Sprites_File = "Box_sprites.png"
#         self.Box_size = (38,38)
#         self.Box_Spritesheet = pygame.image.load(self.Box_Sprites_File).convert_alpha()
#         self.BoxSprites = self.load_sprites(self.Box_Spritesheet, self.Box_size)
#         self.BoxSprites = [item for sublist in self.BoxSprites for item in sublist]

#         self.Item_Icons_Files = "ItemIcons/"
#         self.ItemIcons = self.load_images_from_folder(self.Item_Icons_Files)

#         #print(game_data.pokemon_data["by_number"]["1"]["Name"])

#     def load_sprites(self, spritesheet, sprite_size):
#         sprites = []
#         for y in range(0, spritesheet.get_height(), sprite_size[1]):
#             row = []
#             for x in range(0, spritesheet.get_width(), sprite_size[0]):
#                 sprite = spritesheet.subsurface(pygame.Rect(x, y, sprite_size[0], sprite_size[1]))
#                 row.append(sprite)
#             sprites.append(row)
#         return sprites

#     def load_images_from_folder(self, folder):
#         images = []
#         for filename in os.listdir(folder):
#             if filename.endswith('.png'):
#                 image_path = os.path.join(folder, filename)
#                 try:
#                     image = pygame.image.load(image_path)
#                     images.append(image)
#                 except pygame.error as e:
#                     print(f"Failed to load {filename}: {e}")
#         return images

#     def display_sprites(self, sprite_list, sprite_size):
#         screen = pygame.display.set_mode((800, 600))
#         pygame.display.set_caption('Sprite Viewer')
#         clock = pygame.time.Clock()
        
#         running = True
#         index = 0

#         while running:
#             for event in pygame.event.get():
#                 if event.type == pygame.QUIT:
#                     running = False
#                 elif event.type == pygame.KEYDOWN:
#                     if event.key == pygame.K_ESCAPE:
#                         running = False
#                     else:
#                         index = (index + 1) % len(sprite_list)
            
#             screen.fill((255, 255, 255))

#             if sprite_list:
#                 sprite = sprite_list[index]
#                 screen.blit(sprite, (100, 100))
#                 nameID = self.font.render(game_data.pokemon_data["by_number"][str(index+1)]["Name"], True, [50,50,50]) # str(index+1)
#                 screen.blit(nameID, (20,20))
            
#             pygame.display.flip()

#         pygame.quit()
#         sys.exit()

# # Initialize the Sprites class and display the sprites
# sprites = Sprites()
# sprites.display_sprites(sprites.BoxSprites, sprites.Box_size)