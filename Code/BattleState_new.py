import pygame
from Sprites import sprites

class BattleState(GameState):
    def __init__(self, game, player, opponent):
        self.game = game
        self.player_party = player.player_party
        self.opp_party = opponent
        self.current_player_pokemon = self.player_party[0]
        self.current_opponent_pokemon = self.opp_party[0]

        self.running = True
        self.state_stack = []

        self.state_stack.append(StartBattle)#orsomething
        self.run(self.game.screen)
        
    def handle_events(self, events): 
        # clean the arrow key inputs and call self.player.handle_input at the right times, 
        # i.e. after taking a step if the button is still held down, etc.
        keys = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    pass
                elif event.key == pygame.K_UP:
                    pass
                elif event.key == pygame.K_LEFT:
                    pass
                elif event.key == pygame.K_RIGHT:
                    pass
                elif event.key == pygame.K_x:
                    pass # self.player.handle_input("x")
                elif event.key == pygame.K_z:
                    pass # self.player.handle_input("z")? do i need this here?
                elif event.key == pygame.K_b:
                    pass    ######################             
                elif event.key == pygame.K_p:
                    pass
                elif event.key == pygame.K_t:
                    pass
                else:
                    pass
        if keys[pygame.K_DOWN] and self.game.player.direction=="D":
            self.game.player.handle_input("D")
            #print("d")
        elif keys[pygame.K_UP] and self.game.player.direction=="U":
            self.game.player.handle_input("U")
            #print("u")
        elif keys[pygame.K_LEFT] and self.game.player.direction=="L":
            self.game.player.handle_input("L")
            #print("l")
        elif keys[pygame.K_RIGHT] and self.game.player.direction=="R":
            self.game.player.handle_input("R")
            #print("r")
        else:
            self.game.player.handle_input("*")                

        
    def switch_state(self, state, args):
        if self.state_stack:
            self.state_stack.pop()
        self.push_state(state, args)

    def update(self):
        pass

    def draw(self):
        pass # do i need this function...??

    def run(self, screen, dt):
        while self.running and self.state_stack:
            state = self.state_stack[-1] # is -1 the last index?
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            state.handle_events(events)
            state.update()
            [state.draw(screen) for state in self.state_stack] # trying to draw the overworld when in the pause screen.
            pygame.display.flip()
            time.sleep(dt) ## this is dt, store it in the game options or save data class
        


    def draw_player_healthcard():
        pass

    def draw_opp_healthcard():
        pass




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
            action.execute() # note that these are going to be STATES and this syntax will change


    def calculate_damage(self, attacking_pokemon, defending_pokemon, move):
        # Logic to calculate damage dealt by a move
        damage = (((((2*level/5)+2)*power*attack/defense)/50)*burn*screen*targets*weather*FF+2)*stockpile*critical*doubleDamage*charge*HH*STAB*Type*random
        return damage




#######################################################################
#######################################################################

class BattleStart:
    def __init__(self, game):
        # self.intro_animation
        # self.background
        # self.player #(you)
        # self.opponent
        pass

    def handle_events(self, events):
        pass

    def update(self):
        # increment frames of animations or blit locations until they're completed,
        # and then either trigger the next one or move on to a new state.
        # makes an instance of textbox! so i have to work on that class now..
        pass

    def draw(self, screen):
        pass

#######################################################################
#######################################################################

class BattleChoices:
    def __init__(self, game):
        # self.selected = [0,0]  # [0,0]=fight, [1,1]=run, etc.
        pass

    def handle_events(self, events):
        pass # move cursor and change self.selected
             # create some sort of local version of bag and party when chosen
             # is FIGHT a new gamestate?
             # sort action queue before moving on to the next state!

    def update(self):
        pass

    def draw(self, screen):
        pass



#######################################################################
#######################################################################

class GameState:
    def __init__(self, game):
        pass

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass


#######################################################################
#######################################################################



# Class BattleState(player, opponent)


# Statestack:
# 1) X
# 2) Battle music start, fade pattern. 
# Fade in with you and opponent sliding in. I forget the exact order of events, but they depend on the type of battle
#           Leads to 3
# 3) fight, pkmn, bag, run
#           Leads where clicked
# 4) fight
#           Opens move list. Leads to 8
# 5) PartyState (pkmn)
#           Leads to an instance of PartyState on top of battlestate (primed to switch the preselected first pokemon with something.) Clicking on one brings up the confirmation to switch. But don't actually switch the party location! This state leads to (8) action sorting, right? Because this counts as your move
# 6) BagState (bag)
#           Same deal as partystate, it'll have to be some strange copy of the existing state... also, leads to 8.
# 7) run
#           If it is successful it animates, resets stats, and closes the battle
#           "can't run from a trainer battle" leads back to 3
#           "Couldn't get away" leads deviously to 8
# 8) action sorting!
#           Action queue is sorted based on speed class, items, stats, environment, whatever type effects. Each effect is a state, which get carried out unless someone faints.
# 9) you attacking
# 10) opponent attacking
# 11) opponent fainting, "will you change pokemon?" text
# 12) you fainting, "will you send out another pokemon?" text
# 13) gain xp, gain level, learn move, evolve
# 14) you switching, opponent switching?




# -move queue
# -function to prioritize moves
# -list of ongoing status effects like environment. Things that are not managed by the individual pokemon. How about spikes?
# -function to call for animations
# -functions to carry out status, damage, healing, and switching effects