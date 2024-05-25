from GameState import GameState
import pygame


class TextboxState(GameState):
    def __init__(self, game, message, font):
        self.message = message
        self.game = game
        self.font = font        
        self.border = 40
        self.lines = self.split_message_into_lines(message, font)
        #print(self.lines)
        self.current_line = 0
        self.text_typing_index = 0
        self.typing_speed = 50  # ms per character
        self.fast_typing_speed = 5  # ms per character
        self.is_typing_fast = False
        self.last_typing_time = pygame.time.get_ticks()
        self.fin_flag = False
        self.border_style = pygame.transform.scale(pygame.image.load('choice 1.png'), (int(48*1.5625), int(48*1.5625)))

        self.box_height = self.game.screen_height // 3
        self.box_rect = pygame.Rect(0, self.game.screen_height - self.box_height, self.game.screen_width, self.box_height)
        
    def draw_box_rect(self, screen, rect):
        # The assumption is that the border's width and height are both 10 pixels
        BORDER_SIZE = 24
        x, y, w, h = rect.x, rect.y, rect.width, rect.height
        
        # Corners
        top_left = self.border_style.subsurface((0, 0, BORDER_SIZE, BORDER_SIZE))
        top_right = self.border_style.subsurface((self.border_style.get_width() - BORDER_SIZE, 0, BORDER_SIZE, BORDER_SIZE))
        bottom_left = self.border_style.subsurface((0, self.border_style.get_height() - BORDER_SIZE, BORDER_SIZE, BORDER_SIZE))
        bottom_right = self.border_style.subsurface((self.border_style.get_width() - BORDER_SIZE, self.border_style.get_height() - BORDER_SIZE, BORDER_SIZE, BORDER_SIZE))
        
        # Edges
        top = self.border_style.subsurface((BORDER_SIZE, 0, self.border_style.get_width() - 2*BORDER_SIZE, BORDER_SIZE))
        bottom = self.border_style.subsurface((BORDER_SIZE, self.border_style.get_height() - BORDER_SIZE, self.border_style.get_width() - 2*BORDER_SIZE, BORDER_SIZE))
        left = self.border_style.subsurface((0, BORDER_SIZE, BORDER_SIZE, self.border_style.get_height() - 2*BORDER_SIZE))
        right = self.border_style.subsurface((self.border_style.get_width() - BORDER_SIZE, BORDER_SIZE, BORDER_SIZE, self.border_style.get_height() - 2*BORDER_SIZE))
        
        # Center (this will be repeated to fill the inside of the box)
        center = self.border_style.subsurface((BORDER_SIZE, BORDER_SIZE, self.border_style.get_width() - 2*BORDER_SIZE, self.border_style.get_height() - 2*BORDER_SIZE))
        
        # Draw corners
        screen.blit(top_left, (x, y))
        screen.blit(top_right, (x + w - BORDER_SIZE, y))
        screen.blit(bottom_left, (x, y + h - BORDER_SIZE))
        screen.blit(bottom_right, (x + w - BORDER_SIZE, y + h - BORDER_SIZE))
        
        # Draw edges
        for i in range(BORDER_SIZE, w - BORDER_SIZE, top.get_width()):
            screen.blit(top, (x + i, y))
            screen.blit(bottom, (x + i, y + h - BORDER_SIZE))
        for i in range(BORDER_SIZE, h - BORDER_SIZE, left.get_height()):
            screen.blit(left, (x, y + i))
            screen.blit(right, (x + w - BORDER_SIZE, y + i))
        
        # Fill center
        for i in range(BORDER_SIZE, w - BORDER_SIZE, center.get_width()):
            for j in range(BORDER_SIZE, h - BORDER_SIZE, center.get_height()):
                screen.blit(center, (x + i, y + j))

    def split_message_into_lines(self, message, font):
        # Split the message into words and then reconstruct the lines based on the font width
        words = message.split(" ")
        lines = []
        current_line = []
        for word in words:
            if font.size(' '.join(current_line + [word]))[0] > (self.screen_width-self.border*2):
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
        lines.append(' '.join(current_line))
        return lines
    

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
                #if self.fin_flag:
                    #game.pop_state()
                if self.is_text_finished_typing():
                    self.advance_to_next_line()
                else:
                    self.is_typing_fast = True
            # get keys pressed
            # if X is pressed, self.is_typing_fast = True
            # else: self.is_typing_fast = False

    def is_text_finished_typing(self):
        return self.text_typing_index >= len(self.lines[max(self.current_line-1,0)])

    def advance_to_next_line(self):
        self.text_typing_index = 0
        self.current_line += 1
        if self.current_line >= len(self.lines):
            # You could pop this state from the stack to return to the underlying state
            #self.fin_flag = True
            game.pop_state()
            pass

    #def update(self): # , dt) old
        #current_time = pygame.time.get_ticks()
        #typing_speed = self.fast_typing_speed if self.is_typing_fast else self.typing_speed
        #if current_time - self.last_typing_time > typing_speed:
            #if not self.is_text_finished_typing():
                #self.text_typing_index += 1
                #self.last_typing_time = current_time
                
    def update(self): 
        #print(self.lines[self.current_line][:self.text_typing_index])
        #print(self.text_typing_index)
        speed1 = 1
        speed2 = 3
        if self.is_typing_fast:
            speed = speed2
        else:
            speed = speed1   
            #print(self.is_text_finished_typing())
        if not self.is_text_finished_typing():
            self.text_typing_index += speed

    def draw(self, screen):
        #pygame.draw.rect(screen, (255, 255, 255), self.box_rect)
        self.draw_box_rect(screen, self.box_rect)
        # Compute the starting position for the text
        x = self.border
        y1 = self.screen_height - self.box_height + self.border
        y2 = y1 + int(self.screen_height/6)-self.border/2

        # Display the current line
        
        if self.current_line == 0:
            line1_text = self.lines[self.current_line][:self.text_typing_index]
            line1_text = line1_text + "_"
            line2_text = ""
           
        else:
            line1_text = self.lines[self.current_line-1]
            line2_text = self.lines[self.current_line][:self.text_typing_index]
            line2_text = line2_text + "_"



        line1_surf = self.font.render(line1_text, True, (0, 0, 0))
        screen.blit(line1_surf, (x, y1))
        
        line2_surf = self.font.render(line2_text, True, (0, 0, 0))
        screen.blit(line2_surf, (x, y2))   

        ## If there's a next line, display it too
        #if self.current_line + 1 < len(self.lines):
            #next_line_text = self.lines[self.current_line + 1]
            #text_surface = self.font.render(next_line_text, True, (0, 0, 0))
            #screen.blit(text_surface, (x, y + self.font.get_height()))

        # Display the underscore if needed
        #if self.current_line + 1 < len(self.lines) or not self.is_text_finished_typing():
            #underscore_surface = self.font.render("_", True, (0, 0, 0))
            #screen.blit(underscore_surface, (x + self.font.size(line1_text)[0], y))

