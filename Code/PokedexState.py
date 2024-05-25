import pygame
from GameState import GameState
from GameState import PopState
from GameData import game_data
from SaveData import save_data

class PokedexState(GameState):
    def __init__(self, game):
        super().__init__(game)
        print("pokedex")
        self.bg = pygame.transform.scale(pygame.image.load('bg_list_over_search.png'), (int(512*1.5625), int(384*1.5625)))
        self.selected = 1 # ID number selected and shown
        self.List_slots = ["-----","-----","-----","-----","-----","-----","-----","-----","-----","-----"]
        # data to load:
        # pokemon seen, pokemon caught, name, sprite, flavor text,...
        #print(game.data.pokemon_data['1'])
        
    def UpdateList(self):
        self.List_slots[0] = game_data.pokemon_data[str(self.selected+0)]['Name']
        self.List_slots[1] = game_data.pokemon_data[str(self.selected+1)]['Name']
        self.List_slots[2] = game_data.pokemon_data[str(self.selected+2)]['Name']
        self.List_slots[3] = game_data.pokemon_data[str(self.selected+3)]['Name']
        self.List_slots[4] = game_data.pokemon_data[str(self.selected+4)]['Name']
        self.List_slots[5] = game_data.pokemon_data[str(self.selected+5)]['Name']
        self.List_slots[6] = game_data.pokemon_data[str(self.selected+6)]['Name']
        self.List_slots[7] = game_data.pokemon_data[str(self.selected+7)]['Name']
        self.List_slots[8] = game_data.pokemon_data[str(self.selected+8)]['Name']
        self.List_slots[9] = game_data.pokemon_data[str(self.selected+9)]['Name']

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected+1) % len(game_data.pokemon_data)
                elif event.key == pygame.K_UP:
                    self.selected = (self.selected-1) if (self.selected != 1) else len(game_data.pokemon_data)-len(self.List_slots)
                elif event.key == pygame.K_LEFT:
                    self.selected = max(0,(self.selected-4)) # change this to scroll 1 page - 1 entry
                elif event.key == pygame.K_RIGHT:
                    self.selected = min(150,(self.selected+4)) # change this to scroll 1 page - 1 entry
                elif event.key == pygame.K_z:
                    raise PopState # return PauseState(game) 
                elif event.key == pygame.K_x:
                    pass
        return None

    def update(self):
        # update where the selector arrow is displayed
        self.UpdateList()
        return None

    def draw(self, screen):
        # Draw!
        screen.fill((230, 230, 230))
        screen.blit(self.bg, (0,0))
        Selected_name = game.font.render('Current Pokemon!', True, (255, 255, 255))  # White text
        #List_slots = ["-----","-----","-----","-----","-----","----","-----","-----","-----","-----"]
        List_names = [game.font.render(NAME, True, (30, 30, 30)) for NAME in self.List_slots]
        for i in range(0,len(List_names)):
            screen.blit(List_names[i], (500, 40+52*i)) # 80
        screen.blit(Selected_name, (40, 40))