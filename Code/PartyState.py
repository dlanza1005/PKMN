import pygame
from GameState import GameState


class PartyState(GameState):
    def __init__(self, game):
        self.game = game
        self.selected = 0
        self.S = 0.46875*self.game.save.PIXEL_SIZE
        #.78125*self.game.save.PIXEL_SIZE # 1.5625 old number, which works for 800x600

        print("party")
        
        self.bg_img = pygame.transform.scale(pygame.image.load('PartyScreens/bg.png'), (self.game.W, self.game.H))
        print(self.game.W)
        print(self.game.H)
         # self.S
        self.slot1_bg = pygame.transform.scale(pygame.image.load('PartyScreens/panel_round.png'), (int(154*self.S), int(96*self.S))) # slot 1 on the left is bigger than the rest
        #self.slot1_bg.set_alpha(128)
        self.slot1_s_bg = pygame.transform.scale(pygame.image.load('PartyScreens/panel_round_sel.png'), (int(154*self.S), int(96*self.S))) # slot 1 when selected (156x98)
        #self.slot1_s_bg.set_alpha(128)
        self.slots_bg = pygame.transform.scale(pygame.image.load('PartyScreens/panel_rect.png'), (int(286*self.S), int(46*self.S))) # blue panel bg for slots with pokemon in them 288x48
        #self.slots_bg.set_alpha(128)
        self.slots_s_bg = pygame.transform.scale(pygame.image.load('PartyScreens/panel_rect_sel.png'), (int(286*self.S), int(46*self.S)))  # other slots when selected
        #self.slots_s_bg.set_alpha(128)
        self.icon_ball = pygame.transform.scale(pygame.image.load('PartyScreens/icon_ball.png'), (int(44*self.S), int(56*self.S))) # closed pokeball icon
        #self.icon_ball.set_alpha(128)
        self.icon_s_ball = pygame.transform.scale(pygame.image.load('PartyScreens/icon_ball_sel.png'), (int(44*self.S), int(56*self.S))) # open pokeball icon, for when selected
        #self.icon_s_ball.set_alpha(128)
        self.healthbar = pygame.transform.scale(pygame.image.load('PartyScreens/overlay_hp_back.png'), (int(138*self.S), int(14*self.S))) # image of an empty healthbar
        #self.healthbar.set_alpha(128)
        self.cancel = pygame.transform.scale(pygame.image.load('PartyScreens/icon_cancel.png'), (int(112*self.S), int(36*self.S))) # image of an empty healthbar
        #self.cancel.set_alpha(128)
        self.cancel_s = pygame.transform.scale(pygame.image.load('PartyScreens/icon_cancel_sel.png'), (int(112*self.S), int(36*self.S))) # image of an empty healthbar
        #self.cancel_s.set_alpha(128)

        self.p1_bg = [20*self.S,64*self.S] # 20,64
        self.p2_bg = [224*self.S,32*self.S]
        self.p3_bg = [224*self.S,92*self.S]
        self.p4_bg = [224*self.S,152*self.S]
        self.p5_bg = [224*self.S,212*self.S]
        self.p6_bg = [224*self.S,272*self.S]
        self.pc_bg = [394*self.S,332*self.S]

        self.p1_ball = [5*self.S,42*self.S]      # -15, -22
        self.p2_ball = [206*self.S,27*self.S]    # -18, -5
        self.p3_ball = [206*self.S,87*self.S]    # -18, -5
        self.p4_ball = [206*self.S,147*self.S]   # -18, -5
        self.p5_ball = [206*self.S,207*self.S]   # -18, -5
        self.p6_ball = [206*self.S,267*self.S]   # -18, -5
        self.pc_ball = [389*self.S,324*self.S]   # 

        # location of the pokemon sprite is self.icon#_ball_pos + (self.pkmnX, self.pkmnY)
        self.pkmnX = 2*self.S
        self.pkmnY = 8*self.S

        self.p1_hp_img = [32*self.S,126*self.S]    # 12, 62
        self.p2_hp_img = [365*self.S,47*self.S]    # 141, 15
        self.p3_hp_img = [365*self.S,107*self.S]   # 141, 15
        self.p4_hp_img = [365*self.S,167*self.S]   # 
        self.p5_hp_img = [365*self.S,227*self.S]   #
        self.p6_hp_img = [365*self.S,287*self.S]   #

        self.p1_hp_text = [90*self.S,137*self.S] #
        self.p2_hp_text = [430*self.S,57*self.S]
        self.p3_hp_text = [430*self.S,117*self.S]
        self.p4_hp_text = [430*self.S,177*self.S]
        self.p5_hp_text = [430*self.S,237*self.S]
        self.p6_hp_text = [430*self.S,297*self.S]

        self.p1_bar = [64*self.S, 130*self.S] #(104,193,150,9)
        self.p2_bar = [397*self.S, 51*self.S]
        self.p3_bar = [397*self.S, 111*self.S]
        self.p4_bar = [397*self.S, 171*self.S]
        self.p5_bar = [397*self.S, 231*self.S]
        self.p6_bar = [397*self.S, 291*self.S]

        self.p1_name = [55*self.S,90*self.S]    # 80, 41
        self.p2_name = [270*self.S,40*self.S]     # +94
        self.p3_name = [270*self.S,98*self.S]
        self.p4_name = [270*self.S,160*self.S]
        self.p5_name = [270*self.S,220*self.S]
        self.p6_name = [270*self.S,280*self.S]
        self.pc_name = [440*self.S,342*self.S]

        self.p1_lv = [85*self.S,106*self.S] #
        self.p2_lv = [285*self.S,56*self.S] # +94
        self.p3_lv = [285*self.S,116*self.S]
        self.p4_lv = [285*self.S,176*self.S]
        self.p5_lv = [285*self.S,236*self.S]
        self.p6_lv = [285*self.S,296*self.S]

        self.item1_pos = []




        self.party = []
        self.party_images = []
        self.slot_icons = []
        for i in range(0,len(game.player.party)):
            self.party.append(game.player.party[i])
            self.party_images.append(self.party[i].Box_Sprite)
            self.slot_icons.append(pygame.transform.scale(self.party_images[i], (int(50*self.S), int(50*self.S)))) # 38,38
            


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
                    self.game.pop_state() 
    
                elif event.key == pygame.K_x:
                    if self.selected == 6:  # If Cancel button (which is one past the last Pokemon)
                        self.game.pop_state() 
                    else:
                        #return PartyDetailState(game, self.selected)  # Enter party detail state for this Pokemon
                        self.game.push_state("PartyDetailState",[self.game,self.selected, 0])
    
        return None
    


    def update(self): # ?
        return None

    def drawSlot(self, screen, slot):
        if slot==0:
            if self.selected == 0:
                screen.blit(self.slot1_s_bg, (self.p1_bg[0], self.p1_bg[1])) # (28, 95)
                screen.blit(self.icon_s_ball, (self.p1_ball[0], self.p1_ball[1])) # need open pokeball icon
            else:
                screen.blit(self.slot1_bg, (self.p1_bg[0], self.p1_bg[1]))
                screen.blit(self.icon_ball, (self.p1_ball[0], self.p1_ball[1])) #  10, 70
            screen.blit(self.healthbar, (self.p1_hp_img[0], self.p1_hp_img[1]))  # needs to be linked to the pokemon!! this is just location   54, 187
            pygame.draw.rect(screen,[60,200,50],(self.p1_bar[0],self.p1_bar[1],96*self.S,7*self.S))
            pygame.draw.rect(screen,[140,220,150],(self.p1_bar[0],self.p1_bar[1],96*self.S,4*self.S))       
            slot_name1a = self.game.font.render(self.party[0].internal_name, True, [120,120,120])
            slot_name1b = self.game.font.render(self.party[0].internal_name, True, [230,230,230])
            screen.blit(slot_name1a, (self.p1_name[0]+self.S*1.5,self.p1_name[1]+self.S*1.5))   
            screen.blit(slot_name1b, (self.p1_name[0],self.p1_name[1])) 
            slot_lv1a = self.game.font.render("Lv "+str(self.party[0].level), True, [120,120,120])
            slot_lv1b = self.game.font.render("Lv "+str(self.party[0].level), True, [230,230,230])
            screen.blit(slot_lv1a, (self.p1_lv[0]+self.S*1.5,self.p1_lv[1]+self.S*1.5)) 
            screen.blit(slot_lv1b, (self.p1_lv[0],self.p1_lv[1]))  
            slot_hp1a = self.game.font.render(str(self.party[0].current_HP)+"/ "+str(self.party[0].totalhp), True, [120,120,120])
            slot_hp1b = self.game.font.render(str(self.party[0].current_HP)+"/ "+str(self.party[0].totalhp), True, [230,230,230])
            screen.blit(slot_hp1a, (self.p1_hp_text[0]+self.S*1.5,self.p1_hp_text[1]+self.S*1.5))
            screen.blit(slot_hp1b, (self.p1_hp_text[0],self.p1_hp_text[1]))
            screen.blit(self.slot_icons[0], (self.p1_ball[0]+5, self.p1_ball[1]+(25*self.S))) # 1            50,100
            
        elif slot==1:
            if self.selected == 1:
                screen.blit(self.slots_s_bg, (self.p2_bg[0], self.p2_bg[1]))
                screen.blit(self.icon_s_ball, (self.p2_ball[0], self.p2_ball[1])) #   317, 40
            else:
                screen.blit(self.slots_bg, (self.p2_bg[0], self.p2_bg[1]))
                screen.blit(self.icon_ball, (self.p2_ball[0], self.p2_ball[1]))
            screen.blit(self.healthbar, (self.p2_hp_img[0], self.p2_hp_img[1])) # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(self.p2_bar[0],self.p2_bar[1],96*self.S,7*self.S))
            pygame.draw.rect(screen,[140,220,150],(self.p2_bar[0],self.p2_bar[1],96*self.S,4*self.S))  
            # slot_name2 = self.game.font.render("name2", True, [230,230,230])
            # screen.blit(slot_name2, (450,70))       
            slot_name2a = self.game.font.render(self.party[1].internal_name, True, [120,120,120])
            slot_name2b = self.game.font.render(self.party[1].internal_name, True, [230,230,230])
            screen.blit(slot_name2a, (self.p2_name[0]+self.S*1.5,self.p2_name[1]+self.S*1.5))   
            screen.blit(slot_name2b, (self.p2_name[0],self.p2_name[1])) 
            slot_lv2a = self.game.font.render("Lv "+str(self.party[1].level), True, [120,120,120])
            slot_lv2b = self.game.font.render("Lv "+str(self.party[1].level), True, [230,230,230])
            screen.blit(slot_lv2a, (self.p2_lv[0]+self.S*1.5,self.p2_lv[1]+self.S*1.5)) 
            screen.blit(slot_lv2b, (self.p2_lv[0],self.p2_lv[1]))    
            slot_hp2a = self.game.font.render(str(self.party[1].current_HP)+"/ "+str(self.party[1].totalhp), True, [120,120,120])
            slot_hp2b = self.game.font.render(str(self.party[1].current_HP)+"/ "+str(self.party[1].totalhp), True, [230,230,230])
            screen.blit(slot_hp2a, (self.p2_hp_text[0]+self.S*1.5,self.p2_hp_text[1]+self.S*1.5))
            screen.blit(slot_hp2b, (self.p2_hp_text[0],self.p2_hp_text[1]))
            screen.blit(self.slot_icons[1], (self.p2_ball[0]+self.pkmnX, self.p2_ball[1]+self.pkmnY)) # 2
            
        elif slot==2:
            if self.selected == 2:
                screen.blit(self.slots_s_bg, (self.p3_bg[0], self.p3_bg[1]))
                screen.blit(self.icon_s_ball, (self.p3_ball[0], self.p3_ball[1]))
            else:
                screen.blit(self.slots_bg, (self.p3_bg[0], self.p3_bg[1]))
                screen.blit(self.icon_ball, (self.p3_ball[0], self.p3_ball[1]))
            screen.blit(self.healthbar, (self.p3_hp_img[0], self.p3_hp_img[1])) # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(self.p3_bar[0],self.p3_bar[1],96*self.S,7*self.S))
            pygame.draw.rect(screen,[140,220,150],(self.p3_bar[0],self.p3_bar[1],96*self.S,4*self.S))    
            #slot_name3 = self.game.font.render("name3", True, [230,230,230])
            #screen.blit(slot_name3, (450,165))  
            slot_name3a = self.game.font.render(self.party[2].internal_name, True, [120,120,120])
            slot_name3b = self.game.font.render(self.party[2].internal_name, True, [230,230,230])
            screen.blit(slot_name3a, (self.p3_name[0]+self.S*1.5,self.p3_name[1]+self.S*1.5))   
            screen.blit(slot_name3b, (self.p3_name[0],self.p3_name[1]))   
            slot_lv3a = self.game.font.render("Lv "+str(self.party[2].level), True, [120,120,120])
            slot_lv3b = self.game.font.render("Lv "+str(self.party[2].level), True, [230,230,230])
            screen.blit(slot_lv3a, (self.p3_lv[0]+self.S*1.5,self.p3_lv[1]+self.S*1.5)) 
            screen.blit(slot_lv3b, (self.p3_lv[0],self.p3_lv[1]))           
            slot_hp3a = self.game.font.render(str(self.party[2].current_HP)+"/ "+str(self.party[2].totalhp), True, [120,120,120])
            slot_hp3b = self.game.font.render(str(self.party[2].current_HP)+"/ "+str(self.party[2].totalhp), True, [230,230,230])
            screen.blit(slot_hp3a, (self.p3_hp_text[0]+self.S*1.5,self.p3_hp_text[1]+self.S*1.5))
            screen.blit(slot_hp3b, (self.p3_hp_text[0],self.p3_hp_text[1]))
            screen.blit(self.slot_icons[2], (self.p3_ball[0]+self.pkmnX, self.p3_ball[1]+self.pkmnY)) # 3
            
        elif slot==3:
            if self.selected == 3:
                screen.blit(self.slots_s_bg, (self.p4_bg[0], self.p4_bg[1]))
                screen.blit(self.icon_s_ball, (self.p4_ball[0], self.p4_ball[1]))
            else:
                screen.blit(self.slots_bg, (self.p4_bg[0], self.p4_bg[1]))
                screen.blit(self.icon_ball, (self.p4_ball[0], self.p4_ball[1]))
            screen.blit(self.healthbar, (self.p4_hp_img[0], self.p4_hp_img[1])) # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(self.p4_bar[0],self.p4_bar[1],96*self.S,7*self.S))
            pygame.draw.rect(screen,[140,220,150],(self.p4_bar[0],self.p4_bar[1],96*self.S,4*self.S))    
            slot_name4a = self.game.font.render(self.party[3].internal_name, True, [120,120,120])
            slot_name4b = self.game.font.render(self.party[3].internal_name, True, [230,230,230])
            screen.blit(slot_name4a, (self.p4_name[0]+self.S*1.5,self.p4_name[1]+self.S*1.5))   
            screen.blit(slot_name4b, (self.p4_name[0],self.p4_name[1]))   
            slot_lv4a = self.game.font.render("Lv "+str(self.party[3].level), True, [120,120,120])
            slot_lv4b = self.game.font.render("Lv "+str(self.party[3].level), True, [230,230,230])
            screen.blit(slot_lv4a, (self.p4_lv[0]+self.S*1.5,self.p4_lv[1]+self.S*1.5)) 
            screen.blit(slot_lv4b, (self.p4_lv[0],self.p4_lv[1]))                 
            slot_hp4a = self.game.font.render(str(self.party[3].current_HP)+"/ "+str(self.party[3].totalhp), True, [120,120,120])
            slot_hp4b = self.game.font.render(str(self.party[3].current_HP)+"/ "+str(self.party[3].totalhp), True, [230,230,230])
            screen.blit(slot_hp4a, (self.p4_hp_text[0]+self.S*1.5,self.p4_hp_text[1]+self.S*1.5))
            screen.blit(slot_hp4b, (self.p4_hp_text[0],self.p4_hp_text[1]))
            screen.blit(self.slot_icons[3], (self.p4_ball[0]+self.pkmnX, self.p4_ball[1]+self.pkmnY)) # 4
            
        elif slot==4:
            if self.selected == 4:
                screen.blit(self.slots_s_bg, (self.p5_bg[0], self.p5_bg[1])) 
                screen.blit(self.icon_s_ball, (self.p5_ball[0], self.p5_ball[1]))
            else:
                screen.blit(self.slots_bg, (self.p5_bg[0], self.p5_bg[1]))
                screen.blit(self.icon_ball, (self.p5_ball[0], self.p5_ball[1]))
            screen.blit(self.healthbar, (self.p5_hp_img[0], self.p5_hp_img[1])) # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(self.p5_bar[0],self.p5_bar[1],96*self.S,7*self.S))
            pygame.draw.rect(screen,[140,220,150],(self.p5_bar[0],self.p5_bar[1],96*self.S,4*self.S))     
            slot_name5a = self.game.font.render(self.party[4].internal_name, True, [120,120,120])
            slot_name5b = self.game.font.render(self.party[4].internal_name, True, [230,230,230])
            screen.blit(slot_name5a, (self.p5_name[0]+self.S*1.5,self.p5_name[1]+self.S*1.5))   
            screen.blit(slot_name5b, (self.p5_name[0],self.p5_name[1]))   
            slot_lv5a = self.game.font.render("Lv "+str(self.party[4].level), True, [120,120,120])
            slot_lv5b = self.game.font.render("Lv "+str(self.party[4].level), True, [230,230,230])
            screen.blit(slot_lv5a, (self.p5_lv[0]+self.S*1.5,self.p5_lv[1]+self.S*1.5)) 
            screen.blit(slot_lv5b, (self.p5_lv[0],self.p5_lv[1]))           
            slot_hp5a = self.game.font.render(str(self.party[4].current_HP)+"/ "+str(self.party[4].totalhp), True, [120,120,120])
            slot_hp5b = self.game.font.render(str(self.party[4].current_HP)+"/ "+str(self.party[4].totalhp), True, [230,230,230])
            screen.blit(slot_hp5a, (self.p5_hp_text[0]+self.S*1.5,self.p5_hp_text[1]+self.S*1.5))
            screen.blit(slot_hp5b, (self.p5_hp_text[0],self.p5_hp_text[1]))
            screen.blit(self.slot_icons[4], (self.p5_ball[0]+self.pkmnX, self.p5_ball[1]+self.pkmnY)) # 5
            
        elif slot==5:
            if self.selected == 5:
                screen.blit(self.slots_s_bg, (self.p6_bg[0], self.p6_bg[1]))
                screen.blit(self.icon_s_ball, (self.p6_ball[0], self.p6_ball[1]))
            else:
                screen.blit(self.slots_bg, (self.p6_bg[0], self.p6_bg[1]))
                screen.blit(self.icon_ball, (self.p6_ball[0], self.p6_ball[1]))
            screen.blit(self.healthbar, (self.p6_hp_img[0], self.p6_hp_img[1])) # needs to be linked to the pokemon!! this is just location
            pygame.draw.rect(screen,[60,200,50],(self.p6_bar[0],self.p6_bar[1],96*self.S,7*self.S))
            pygame.draw.rect(screen,[140,220,150],(self.p6_bar[0],self.p6_bar[1],96*self.S,4*self.S))   
            slot_name6a = self.game.font.render(self.party[5].internal_name, True, [120,120,120])
            slot_name6b = self.game.font.render(self.party[5].internal_name, True, [230,230,230])
            screen.blit(slot_name6a, (self.p6_name[0]+self.S*1.5,self.p6_name[1]+self.S*1.5))   
            screen.blit(slot_name6b, (self.p6_name[0],self.p6_name[1]))   
            slot_lv6a = self.game.font.render("Lv "+str(self.party[5].level), True, [120,120,120])
            slot_lv6b = self.game.font.render("Lv "+str(self.party[5].level), True, [230,230,230])
            screen.blit(slot_lv6a, (self.p6_lv[0]+self.S*1.5,self.p6_lv[1]+self.S*1.5)) 
            screen.blit(slot_lv6b, (self.p6_lv[0],self.p6_lv[1]))           
            slot_hp6a = self.game.font.render(str(self.party[5].current_HP)+"/ "+str(self.party[5].totalhp), True, [120,120,120])
            slot_hp6b = self.game.font.render(str(self.party[5].current_HP)+"/ "+str(self.party[5].totalhp), True, [230,230,230])
            screen.blit(slot_hp6a, (self.p6_hp_text[0]+self.S*1.5,self.p6_hp_text[1]+self.S*1.5))
            screen.blit(slot_hp6b, (self.p6_hp_text[0],self.p6_hp_text[1])) 
            screen.blit(self.slot_icons[5], (self.p6_ball[0]+self.pkmnX, self.p6_ball[1]+self.pkmnY)) # 6   
            
        elif slot==6:
            if self.selected == 6:
                screen.blit(self.cancel_s, (self.pc_bg[0], self.pc_bg[1])) # pc_bg
                screen.blit(self.icon_s_ball, (self.pc_ball[0], self.pc_ball[1]))
            else:
                screen.blit(self.cancel, (self.pc_bg[0], self.pc_bg[1]))
                screen.blit(self.icon_ball, (self.pc_ball[0], self.pc_ball[1]))
            cancel = self.game.font.render("CANCEL", True, [230,230,230])
            screen.blit(cancel, (self.pc_name[0],self.pc_name[1]))   
                
    def draw(self, screen):
        numPK = len(self.game.player.party) # number of pokemon in your party
        screen.blit(self.bg_img, (0, 0))
        for i in range(0,numPK):
            self.drawSlot(screen, i)
        self.drawSlot(screen,6)