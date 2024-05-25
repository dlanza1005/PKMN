import pygame
from GameState import GameState


class PartyState(GameState):
    def __init__(self, game):
        self.game = game
        self.selected = 0
        self.S = .45*self.game.save.PIXEL_SIZE
        #.78125*self.game.save.PIXEL_SIZE # 1.5625 old number, which works for 800x600

        print("party")
        
        self.bg_img = pygame.transform.scale(pygame.image.load('PartyScreens/bg.png'), (self.game.W, self.game.H))
         # self.S
        self.slot1_bg = pygame.transform.scale(pygame.image.load('PartyScreens/panel_round.png'), (int(156*self.S), int(98*self.S))) # slot 1 on the left is bigger than the rest
        self.slot1_bg.set_alpha(128)
        self.slot1_s_bg = pygame.transform.scale(pygame.image.load('PartyScreens/panel_round_sel.png'), (int(156*self.S), int(98*self.S))) # slot 1 when selected
        self.slot1_s_bg.set_alpha(128)
        self.slots_bg = pygame.transform.scale(pygame.image.load('PartyScreens/panel_rect.png'), (int(288*self.S), int(48*self.S))) # blue panel bg for slots with pokemon in them
        self.slots_bg.set_alpha(128)
        self.slots_s_bg = pygame.transform.scale(pygame.image.load('PartyScreens/panel_rect_sel.png'), (int(288*self.S), int(48*self.S)))  # other slots when selected
        self.slots_s_bg.set_alpha(128)
        self.icon_ball = pygame.transform.scale(pygame.image.load('PartyScreens/icon_ball.png'), (int(44*self.S), int(56*self.S))) # closed pokeball icon
        self.icon_ball.set_alpha(128)
        self.icon_s_ball = pygame.transform.scale(pygame.image.load('PartyScreens/icon_ball_sel.png'), (int(44*self.S), int(56*self.S))) # open pokeball icon, for when selected
        self.icon_s_ball.set_alpha(128)
        self.healthbar = pygame.transform.scale(pygame.image.load('PartyScreens/overlay_hp_back.png'), (int(138*self.S), int(14*self.S))) # image of an empty healthbar
        self.healthbar.set_alpha(128)
        self.cancel = pygame.transform.scale(pygame.image.load('PartyScreens/icon_cancel.png'), (int(112*self.S), int(36*self.S))) # image of an empty healthbar
        self.cancel.set_alpha(128)
        self.cancel_s = pygame.transform.scale(pygame.image.load('PartyScreens/icon_cancel_sel.png'), (int(112*self.S), int(36*self.S))) # image of an empty healthbar
        self.cancel_s.set_alpha(128)
#512x384
        self.slot1_bg_pos = [8*self.game.W/200, 20*self.game.H/120]  # [28,95] for 600x800
        self.slot2_bg_pos = [.43375*self.game.W, .077*self.game.H]  # (347, 46)
        self.slot3_bg_pos = [8*self.game.W/200, 20*self.game.H/120]  # (347, 141)
        self.slot4_bg_pos = [8*self.game.W/200, 20*self.game.H/120]  # (347, 235)
        self.slot5_bg_pos = [8*self.game.W/200, 20*self.game.H/120]  # (347, 328)) 
        self.slot6_bg_pos = [8*self.game.W/200, 20*self.game.H/120]  # (347, 421)) 
        self.cancel_bg_pos= [8*self.game.W/200, 20*self.game.H/120]  # (617, 514)) 



        self.party = []
        self.party_images = []
        self.slot_icons = []
        for i in range(0,len(game.player.party)):
            self.party.append(game.player.party[i])
            self.party_images.append(self.party[i].Box_Sprite)
            self.slot_icons.append(pygame.transform.scale(self.party_images[i], (int(38*self.S), int(38*self.S))))
            


    def handle_events(self, events):
        num_pokemon = len(self.party)  # Assuming you have a list called pokemon_list
    
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if self.selected == 0:
                        self.selected=6
                    elif self.selected < num_pokemon-1:  # Only increment if below the number of actual Pokemon
                        self.selected += 1
                    elif self.selected == 6:
                        self.selected = 0
                    else:
                        self.selected = 6  # Wrap around to the first Pokemon
    
                elif event.key == pygame.K_UP:
                    if self.selected==6:
                        self.selected=num_pokemon-1
                    elif self.selected > 0:
                        self.selected -= 1
                    else:
                        self.selected = 6#num_pokemon-1  # Wrap around to the last Pokemon or cancel button
    
                elif event.key == pygame.K_LEFT:
                    self.selected = 0
    
                elif event.key == pygame.K_RIGHT:
                    if self.selected == 0 and num_pokemon > 1:
                        self.selected = 1
    
                elif event.key == pygame.K_z:
                    raise PopState 
    
                elif event.key == pygame.K_x:
                    if self.selected == 6:  # If Cancel button (which is one past the last Pokemon)
                        raise PopState 
                    else:
                        return PartyDetailState(game, self.selected)  # Enter party detail state for this Pokemon
    
        return None
    


    def update(self): # ?
        return None

    def drawSlot(self, screen, slot):
        if slot==0:
            if self.selected == 0:
                screen.blit(self.slot1_s_bg, (self.slot1_bg_pos[0], self.slot1_bg_pos[1])) # (28, 95)
                screen.blit(self.icon_s_ball, (10, 70)) # need open pokeball icon
            else:
                screen.blit(self.slot1_bg, (28, 95))
                screen.blit(self.icon_ball, (10, 70))
            screen.blit(self.healthbar, (54, 187))  # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(104,193,150,9))
            pygame.draw.rect(screen,[140,220,150],(104,193,150,3))       
            slot_name1 = self.game.font.render("Test1", True, [230,230,230])
            screen.blit(slot_name1, (100,140))   
            slot_lv1 = self.game.font.render("Test1", True, [230,230,230])
            screen.blit(slot_lv1, (100,170))  
            slot_hp1 = self.game.font.render("Test1", True, [230,230,230])
            screen.blit(slot_hp1, (160,210))
            screen.blit(self.slot_icons[0], (50,100)) # 1
            
        elif slot==1:
            if self.selected == 1:
                screen.blit(self.slots_s_bg, (self.slot2_bg_pos[0], self.slot2_bg_pos[1]))
                screen.blit(self.icon_s_ball, (317, 40))
            else:
                screen.blit(self.slots_bg, (self.slot2_bg_pos[0], self.slot2_bg_pos[1]))
                screen.blit(self.icon_ball, (317, 40))
            screen.blit(self.healthbar, (575, 70)) # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(625,76,150,9))
            pygame.draw.rect(screen,[140,220,150],(625,76,150,3))  
            slot_name2 = self.game.font.render("Test2", True, [230,230,230])
            screen.blit(slot_name2, (450,70))       
            slot_lv2 = self.game.font.render("Test2", True, [230,230,230])
            screen.blit(slot_lv2, (450,100))     
            slot_hp2 = self.game.font.render("Test2", True, [230,230,230])
            screen.blit(slot_hp2, (700,100))
            screen.blit(self.slot_icons[1], (330,70)) # 2
            
        elif slot==2:
            if self.selected == 2:
                screen.blit(self.slots_s_bg, (347, 141))
                screen.blit(self.icon_s_ball, (317, 135))
            else:
                screen.blit(self.slots_bg, (347, 141))
                screen.blit(self.icon_ball, (317, 135))
            screen.blit(self.healthbar, (575, 165)) # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(625,171,150,9))
            pygame.draw.rect(screen,[140,220,150],(625,171,150,3))    
            slot_name3 = self.game.font.render("Test3", True, [230,230,230])
            screen.blit(slot_name3, (450,165))    
            slot_lv3 = self.game.font.render("Test3", True, [230,230,230])
            screen.blit(slot_lv3, (450,195))            
            slot_hp3 = self.game.font.render("Test3", True, [230,230,230])
            screen.blit(slot_hp3, (700,195))
            screen.blit(self.slot_icons[2], (330,165)) # 3
            
        elif slot==3:
            if self.selected == 3:
                screen.blit(self.slots_s_bg, (347, 235))
                screen.blit(self.icon_s_ball, (317, 229))
            else:
                screen.blit(self.slots_bg, (347, 235))
                screen.blit(self.icon_ball, (317, 229))
            screen.blit(self.healthbar, (575, 259)) # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(625,265,150,9))
            pygame.draw.rect(screen,[140,220,150],(625,265,150,3))    
            slot_name4 = self.game.font.render("Test4", True, [230,230,230])
            screen.blit(slot_name4, (450,259))   
            slot_lv4 = self.game.font.render("Test4", True, [230,230,230])
            screen.blit(slot_lv4, (450,289))         
            slot_hp4 = self.game.font.render("Test4", True, [230,230,230])
            screen.blit(slot_hp4, (700,289))
            screen.blit(self.slot_icons[3], (330,260)) # 4
            
        elif slot==4:
            if self.selected == 4:
                screen.blit(self.slots_s_bg, (347, 328)) 
                screen.blit(self.icon_s_ball, (317, 322))
            else:
                screen.blit(self.slots_bg, (347, 328))
                screen.blit(self.icon_ball, (317, 322))
            screen.blit(self.healthbar, (575, 352)) # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(625,358,150,9))
            pygame.draw.rect(screen,[140,220,150],(625,358,150,3))     
            slot_name5 = self.game.font.render("Test5", True, [230,230,230])
            screen.blit(slot_name5, (450,352))      
            slot_lv5 = self.game.font.render("Test5", True, [230,230,230])
            screen.blit(slot_lv5, (450,382))     
            slot_hp5 = self.game.font.render("Test5", True, [230,230,230])
            screen.blit(slot_hp5, (700,382))
            screen.blit(self.slot_icons[4], (330,355)) # 5
            
        elif slot==5:
            if self.selected == 5:
                screen.blit(self.slots_s_bg, (347, 421))
                screen.blit(self.icon_s_ball, (317, 415))
            else:
                screen.blit(self.slots_bg, (347, 421))
                screen.blit(self.icon_ball, (317, 415))
            screen.blit(self.healthbar, (575, 445)) # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(625,451,150,9))
            pygame.draw.rect(screen,[140,220,150],(625,451,150,3))   
            slot_name6 = self.game.font.render("Test6", True, [230,230,230])
            screen.blit(slot_name6, (450,445))             
            slot_lv6 = self.game.font.render("Test6", True, [230,230,230])
            screen.blit(slot_lv6, (450,475))  
            slot_hp6 = self.game.font.render("Test6", True, [230,230,230])
            screen.blit(slot_hp6, (700,475))   
            screen.blit(self.slot_icons[5], (330,450)) # 6   
            
        elif slot==6:
            if self.selected == 6:
                screen.blit(self.cancel_s, (617, 514)) 
                screen.blit(self.icon_s_ball, (587, 501))
            else:
                screen.blit(self.cancel, (617, 514))
                screen.blit(self.icon_ball, (587, 501))
                
    def draw(self, screen):
        numPK = len(self.game.player.party) # number of pokemon in your party
        screen.blit(self.bg_img, (0, 0))
        for i in range(0,numPK):
            self.drawSlot(screen, i)
        self.drawSlot(screen,6)