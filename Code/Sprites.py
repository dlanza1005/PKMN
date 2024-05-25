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

        # self.Attack_Sprites_file = ""

        self.Item_Icons_Files = "ItemIcons/"
        # self.item_size = (48,48)
        self.ItemIcons = self.load_images_from_folder(self.Item_Icons_Files)


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