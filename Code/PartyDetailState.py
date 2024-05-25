import pygame
from GameState import GameState

class PartyDetailState(GameState):
    def __init__(self, game, index, card=0):
        self.selected = index
        self.pkmn = game.player.party[self.selected]
        self.bg1 = pygame.transform.scale(pygame.image.load('PartyScreens/bg_1.png'), (int(512*1.5625), int(384*1.5625)))
        self.bg2 = pygame.transform.scale(pygame.image.load('PartyScreens/bg_2.png'), (int(512*1.5625), int(384*1.5625)))
        self.bg3 = pygame.transform.scale(pygame.image.load('PartyScreens/bg_3.png'), (int(512*1.5625), int(384*1.5625)))
        self.bg4 = pygame.transform.scale(pygame.image.load('PartyScreens/bg_4.png'), (int(512*1.5625), int(384*1.5625)))
        self.bg5 = pygame.transform.scale(pygame.image.load('PartyScreens/bg_5.png'), (int(512*1.5625), int(384*1.5625)))
        print("party detail")
        self.pkmnSprite = pygame.transform.scale(self.pkmn.Front_Sprite, (int(80*2.5*1.5625), int(80*2.5*1.5625)))
        # card is the left/right switching info cards.
        self.card = card


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected+1)%len(game.player.party)
                    game.pop_state()
                    return PartyDetailState(game, self.selected,self.card)
                elif event.key == pygame.K_UP:
                    self.selected = self.selected-1 if self.selected>0 else len(game.player.party)-1
                    game.pop_state()
                    return PartyDetailState(game, self.selected,self.card)
                elif event.key == pygame.K_LEFT:
                    self.card = self.card-1 if self.card>0 else 3
                    game.pop_state()
                    return PartyDetailState(game, self.selected,self.card)
                elif event.key == pygame.K_RIGHT:
                    self.card = (self.card+1) % 4
                    game.pop_state()
                    return PartyDetailState(game, self.selected,self.card)
                elif event.key == pygame.K_z:
                    raise PopState #return PauseState()
                elif event.key == pygame.K_x:
                    pass
        return None

    def update(self):
        # update where the selector arrow is displayed
        return None

    def draw(self, screen):
        # Draw!
        if self.card==0:
            screen.fill((0, 0, 100))
            screen.blit(self.bg1, (0,0))
            level = game.font.render(str(self.pkmn.level), True, (100, 100, 100))  # White text
            screen.blit(level, (272, 545))             
            level = game.font.render(str(self.pkmn.level), True, (255, 255, 255))  # White text
            screen.blit(level, (270, 543))   
            name = game.font.render(self.pkmn.name, True, (100, 100, 100))  # White text
            screen.blit(name, (32, 402))                   
            name = game.font.render(self.pkmn.name, True, (255, 255, 255))  # White text
            screen.blit(name, (30, 400))
            
        elif self.card==1:
            #screen.fill((100, 0, 0))
            screen.blit(self.bg2, (0,0))
            level = game.font.render(str(self.pkmn.level), True, (100, 100, 100))  # White text
            screen.blit(level, (272, 545))             
            level = game.font.render(str(self.pkmn.level), True, (255, 255, 255))  # White text
            screen.blit(level, (270, 543))   
            name = game.font.render(self.pkmn.name, True, (100, 100, 100))  # White text
            screen.blit(name, (32, 402))                   
            name = game.font.render(self.pkmn.name, True, (255, 255, 255))  # White text
            screen.blit(name, (30, 400))   
            
            hp = game.font.render(str(self.pkmn.current_HP) + "  /  " + str(self.pkmn.totalhp), True, (50, 50, 50))  # White text
            screen.blit(hp, (460, 180))        
            attack = game.font.render(str(self.pkmn.attack), True, (50, 50, 50))  # White text
            screen.blit(attack, (460, 230))
            defense = game.font.render(str(self.pkmn.defense), True, (50, 50, 50))  # White text
            screen.blit(defense, (460, 280))
            spatt = game.font.render(str(self.pkmn.spatk), True, (50, 50, 50))  # White text
            screen.blit(spatt, (730, 180))
            spdef = game.font.render(str(self.pkmn.spdef), True, (50, 50, 50))  # White text
            screen.blit(spdef, (730, 230))
            spd = game.font.render(str(self.pkmn.speed), True, (50, 50, 50))  # White text
            screen.blit(spd, (730, 280))      
            
        elif self.card==2:
            #screen.fill((0, 100, 0))
            screen.blit(self.bg3, (0,0))
            level = game.font.render(str(self.pkmn.level), True, (100, 100, 100))  # White text
            screen.blit(level, (272, 545))             
            level = game.font.render(str(self.pkmn.level), True, (255, 255, 255))  # White text
            screen.blit(level, (270, 543))   
            name = game.font.render(self.pkmn.name, True, (100, 100, 100))  # White text
            screen.blit(name, (32, 402))                   
            name = game.font.render(self.pkmn.name, True, (255, 255, 255))  # White text
            screen.blit(name, (30, 400))            
        elif self.card==3:
            #screen.fill((100, 0, 100))
            screen.blit(self.bg4, (0,0))    
            level = game.font.render(str(self.pkmn.level), True, (100, 100, 100))  # White text
            screen.blit(level, (272, 545))             
            level = game.font.render(str(self.pkmn.level), True, (255, 255, 255))  # White text
            screen.blit(level, (270, 543))   
            name = game.font.render(self.pkmn.name, True, (100, 100, 100))  # White text
            screen.blit(name, (32, 402))                   
            name = game.font.render(self.pkmn.name, True, (255, 255, 255))  # White text
            screen.blit(name, (30, 400))            
        elif self.card==4:
            #screen.fill((100, 0, 100))
            screen.blit(self.bg5, (0,0))      
            level = game.font.render(str(self.pkmn.level), True, (100, 100, 100))  # White text
            screen.blit(level, (272, 545))             
            level = game.font.render(str(self.pkmn.level), True, (255, 255, 255))  # White text
            screen.blit(level, (270, 543))   
            name = game.font.render(self.pkmn.name, True, (100, 100, 100))  # White text
            screen.blit(name, (32, 402))                   
            name = game.font.render(self.pkmn.name, True, (255, 255, 255))  # White text
            screen.blit(name, (30, 400))            
        screen.blit(self.pkmnSprite, (15,90))