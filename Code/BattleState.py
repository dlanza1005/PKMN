import pygame
from GameState import GameState


class BattleState(GameState):
    def __init__(self, game, player, opponent):
        self.game = game
        self.party = player.party
        self.opponent_team = opponent
        self.current_player_pokemon = self.party[0]
        self.current_opponent_pokemon = self.opponent_team[0]
        self.turn_order = []  # This will be used to determine who attacks first in each turn
        pokemon_font = pygame.font.Font(None, 36)
        self.text_box = [] # Textbox()
        self.running = True
        self.battlestack = [] # 
        
        self.bg = pygame.transform.scale(pygame.image.load("grass_bg.png"), (int(800), int(600)))
        self.opponent_base = pygame.transform.scale(pygame.image.load("path_base1.png"), (int(256*1.5625), int(128*1.5625))) 
        self.opponent_data_box = pygame.transform.scale(pygame.image.load("databox_normal_foe.png"), (int(260*1.5625), int(62*1.5625))) 
        self.player_data_box = pygame.transform.scale(pygame.image.load("databox_normal.png"), (int(260*1.5625), int(84*1.5625)))
    
    def draw_opp_health(self, screen, pkmn):
        location = [210,87]
        hp = pkmn.current_HP/pkmn.totalhp
        if hp<.1:
            color = [[200,60,50],[220,150,150]]
        elif hp<.5:
            color = [[200,200,50],[220,220,150]]
        else:
            color = [[60,200,50],[140,220,150]]
        pygame.draw.rect(screen,color[0],(location[0],location[1],150*hp,7))
        pygame.draw.rect(screen,color[1],(location[0],location[1],150*hp,3))      
        
    def draw_player_health(self, screen, pkmn):
        location = [588,363]
        hp = pkmn.current_HP/pkmn.totalhp
        if hp<.1:
            color = [[200,60,50],[220,150,150]]
        elif hp<.5:
            color = [[200,200,50],[220,220,150]]
        else:
            color = [[60,200,50],[140,220,150]]        
        pygame.draw.rect(screen,[60,200,50],(location[0],location[1],150,6))
        pygame.draw.rect(screen,[140,220,150],(location[0],location[1],150,3))       
        
    def handle_events(self, events):
        # Handle events, such as player input. This will likely be a complex method
        # and will involve checking the current state of the battle to determine
        # what actions are available, and then acting on the player's input.
        while self.running:
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            #self.screen.fill((0, 0, 0))  # fill screen with black
            self.draw(game.screen)
            #pygame.display.flip()

        ## GPT4's answer when i told it to organize the info i found on the battle system into a usable form
        # Initialize an empty list for the action queue
        action_queue = []
        
        # Add actions to action_queue based on player choices
        # ...
        
        # Sort the action queue
        def sort_action_queue(action_queue):
            # Handle switches, Pursuit, rotations first
            # Handle Mega Evolution flag
            # Sort by move priority
            action_queue.sort(key=lambda x: x.move.priority, reverse=True)
            # Handle Quick Claw, Quick Draw, Custap Berry
            # Handle Full Incense, Lagging Tail, Stall
            # Handle Mycelium Might
            # Sort by Speed Stat (consider Trick Room)
            if trick_room_effect:
                action_queue.sort(key=lambda x: x.pokemon.speed)
            else:
                action_queue.sort(key=lambda x: x.pokemon.speed, reverse=True)
            # Handle ties
        # Execute actions in the sorted action_queue
        def execute_actions(action_queue):
            for action in action_queue:
                action.execute()

    ########################################
    
    ########################################


    def start_battle(self):
        pass # maybe eliminate (self) here? load pokemon, reset battle stats,
             # instantiate health bars, sprites, textbox,... print text, animate pokemon, etc.
    

    def calculate_damage(self, attacking_pokemon, defending_pokemon, move):
        # Logic to calculate damage dealt by a move
        damage = (((((2*level/5)+2)*power*attack/defense)/50)*burn*screen*targets*weather*FF+2)*stockpile*critical*doubleDamage*charge*HH*STAB*Type*random
        return damage

    def apply_damage(self, defending_pokemon, damage):
        # Apply damage to a Pokemon, taking into account health limits
        pass

    def check_for_fainted(self):
        # Check if a Pokemon has fainted and handle switching out
        pass

    def check_for_end_of_battle(self):
        # Check if all Pokemon on one side have fainted
        pass
    
    def execute_turn(self):
        # Execute each Pokemon's move in the correct order
        pass



    def update(self):
        # Update the state of the battle. This could involve things like applying
        # damage, checking if a Pokemon has fainted, handling switches, etc.
        #battle.calculate_turn_order()
        #battle.execute_turn()
        #battle.check_for_fainted()
        #battle.check_for_end_of_battle() 
        pass

    # def draw(self, screen):
        # Draw the battle screen. This would involve drawing the backgrounds, the
        # player and opponent sprites, the health bars of the Pokemon, etc.
    

    def draw(self, screen):
        screen.fill((255, 255, 255))  # Fill the screen with baked beans
        screen.blit(self.bg, (0, 0))
        # Set up some fonts
        
        # draw background
        # draw health bars
        screen.blit(self.opponent_data_box, (25, 25))
        self.draw_opp_health(screen, self.opponent_team[0])
        screen.blit(self.player_data_box, (375, 300))
        self.draw_player_health(screen, self.party[0]) # 360
             
        # draw sprites
        screen.blit(self.opponent_team[0].Front_Sprite, (550, 50))
        screen.blit(self.party[0].Back_Sprite, (50, 350))
        # draw effects
        # draw textbox
        pygame.display.flip()
    
        #1-start battle
        #2-abilities like Intimidate
        #2-weather
        #3-choose your move or action
        #4-calculate move priority (note that some abilities affect some move priorities)
        #5-pursuit?
        #5-quick claw, custap berry, o-powers
        #6-switch pokemon,rotating, using items, escaping battle, charging msg for focus punch, beak blast, shell trap
        #7-execute moves
        
        #?-note that X is asleep or X woke up
        