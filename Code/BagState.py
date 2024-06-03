import pygame
from GameState import GameState
import Item
from collections import Counter

class BagState(GameState):
    def __init__(self, game):
        self.game = game
        self.bg_img = "D:\MyPythonShit\GithubPKMN\BagScreens\\bg_m.png"
        self.bg = pygame.transform.scale(pygame.image.load(self.bg_img), (self.game.W, self.game.H))
        self.S = self.game.save.PIXEL_SIZE
        self.BagFont = pygame.font.Font(self.game.save.FONT, int(self.game.font_size*1.625))
        self.DescriptionFont = pygame.font.Font(self.game.save.FONT, int(self.game.font_size*1))
        self.pocket = 0
        self.pocket_names = ["Items", "Medicine", "Poke Balls", "TMs & HMs", "Key Items"]
        self.bag = self.game.save.BAG
        self.pocket_lists = self.sort_pockets()
        self.scroll = 0
        self.cursor = 0
        
    # 1 - Items
    # 2 - Medicine
    # 3 - Poke Balls
    # 4 - TMs & HMs
    # 5 - Berries
    # x - Mail      (ignore this one.)
    # 6 - Battle Items
    # 7 - Key Items

    def sort_pockets(self):
        # Create separate lists for each bag pocket
        pocket_lists = [[] for _ in range(8)]
        for item in self.bag:
            item_obj = Item.generate_item(item)
            pocket_lists[item_obj.pocket_id - 1].append(item)

        # Count duplicates using Counter for each pocket
        for pocket_id, pocket_items in enumerate(pocket_lists):
            item_counts = Counter(item for item in pocket_items)
            print(item_counts)
            #print(item_counts)
            # Remove duplicates and represent item quantity in the output
            pocket_lists[pocket_id] = [[Item.generate_item(item), count] for item, count in item_counts.items()]   #

        return pocket_lists


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.cursor < 7 and self.cursor < len(self.pocket_lists[self.pocket])-1:
                        self.cursor = self.cursor+1
                    elif len(self.pocket_lists[self.pocket]) > 8 and self.cursor == 7:
                        self.scroll = min(self.scroll+1, len(self.pocket_lists[self.pocket])-8)
                elif event.key == pygame.K_UP:
                    if self.cursor > 0:
                        self.cursor = self.cursor-1
                    elif len(self.pocket_lists[self.pocket]) > 8 and self.cursor == 0:
                        self.scroll = max(self.scroll-1, 0)
                elif event.key == pygame.K_LEFT:
                    self.pocket = (self.pocket-1) % len(self.pocket_names)
                    self.cursor = 0
                    self.scroll = 0
                elif event.key == pygame.K_RIGHT:
                    self.pocket = (self.pocket+1) % len(self.pocket_names)
                    self.cursor = 0
                    self.scroll = 0
                elif event.key == pygame.K_z:
                    self.game.pop_state() 
                elif event.key == pygame.K_x:
                    pass
        return None

    def update(self):
        # update where the selector arrow is displayed
        return None

    def draw(self, screen):
        # Draw!
        screen.fill([50,50,100])
        screen.blit(self.bg, (0, 0))  # draws the image at the top-left corner

        # draw the marker that designates which pocket the player is currently looking at
        pocket_positions = [(42*self.S, 30*self.S),
                    (50*self.S, 30*self.S),
                    (58*self.S, 30*self.S),
                    (66*self.S, 30*self.S),
                    (74*self.S, 30*self.S)]
        
        if 0 <= self.pocket < len(pocket_positions):
            pygame.draw.rect(screen, (220, 30, 30), (pocket_positions[self.pocket][0], pocket_positions[self.pocket][1], 5*self.S, 5*self.S))


        # blit the name of the pocket the player is looking at at the top left corner of the screen
        slot_positions = [(120*self.S, 19*self.S),
                          (120*self.S, (19+18*1)*self.S),
                          (120*self.S, (19+18*2)*self.S),
                          (120*self.S, (19+18*3)*self.S),
                          (120*self.S, (19+18*4)*self.S),
                          (120*self.S, (19+18*5)*self.S),
                          (120*self.S, (19+18*6)*self.S),
                          (120*self.S, (19+18*7)*self.S)]
        
        #i=0 # i is the index of the slot in the bag
        for i, slot in enumerate(self.pocket_lists[self.pocket][self.scroll:self.scroll+8]):
            slot_surface_names = self.BagFont.render(slot[0].internal_name, True, [220,220,210])
            screen.blit(slot_surface_names, [slot_positions[i][0]+self.S, slot_positions[i][1]+self.S])
            slot_surface_names = self.BagFont.render(slot[0].internal_name, True, [40,40,40])
            screen.blit(slot_surface_names, slot_positions[i])
            #slot_surface_quantities = self.game.BagFont.render( "x"  + str(slot.quantity), True, [50,50,50])
            #screen.blit(slot_surface_quantities, [214*self.S, slot_positions[i][1]])
        
        # blit the name of the pocket in the top left corner of the screen
        pocket_name_surface = self.BagFont.render(self.pocket_names[self.pocket], True, [40,40,40])
        screen.blit(pocket_name_surface, (34*self.S, 9*self.S))

        # blit the cursor to the left of the item name
        cursor_position = (113*self.S, (23+18*self.cursor)*self.S)
        # the cursor is BagScreens/cursor.png
        cursor_img = pygame.transform.scale(pygame.image.load("D:\MyPythonShit\GithubPKMN\BagScreens\cursor.png"), (6*self.S, 10*self.S))
        screen.blit(cursor_img, cursor_position)

        # transform the item image to the correct size and blit it to the screen at the location 
        #print(self.pocket_lists[self.pocket])
        if len(self.pocket_lists[self.pocket]) > 0:
            item_img = pygame.transform.scale(self.pocket_lists[self.pocket][self.scroll+self.cursor][0].Item_Icon, (25*self.S, 25*self.S))
            screen.blit(item_img, (7*self.S, 81*self.S))
        
        # blit the item description to the screen
        if len(self.pocket_lists[self.pocket]) > 0:
            item_description = self.pocket_lists[self.pocket][self.scroll+self.cursor][0].description
            lines = []
            current_line = ""
            max_width = 100*self.S  # maximum width for the description
            pygame.draw.rect(screen, (220, 30, 30), (7*self.S, 115*self.S, max_width, 5*self.S))
            for word in item_description.split():
                if self.BagFont.render(current_line, True, [40, 40, 40]).get_rect().width <= max_width: # len(current_line) + len(word)
                    current_line += word + " " 
                else:
                    lines.append(current_line)
                    current_line = word + " "
            lines.append(current_line)

            for i, line in enumerate(lines):
                item_description_surface = self.DescriptionFont.render(line, True, [40, 40, 40])
                screen.blit(item_description_surface, (7 * self.S, (115 + 13 * i) * self.S))