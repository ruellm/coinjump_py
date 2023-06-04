import pygame
import globals
from button import Button
from game_state import GameState
from utilities import draw_text
from animated_image import AnimatedImage

font_size = 50

class MenuState:
    def __init__(self):
        self.font = pygame.font.SysFont(None, font_size)  # Use the default system font
        pos_x = (globals.screen_width // 2) - 100
        pos_y = (globals.screen_height // 2) - 25
        self.start_button = Button(pos_x, pos_y, 
                                   200, 50, pygame.Color("blue"), pygame.Color("lightblue"), pygame.Color("darkblue"),
                                    "Start Game", pygame.Color("white"), self.font, self.start_button_clicked)
        # self.bomb = AnimatedImage()
        # self.bomb.Load("images/bomb-explode.png")
        # self.bomb.Set(7, 20, True)
        # self.bomb._frameWidth = 40

        # self.coin = AnimatedImage()
        # self.coin.Load("images/coin_spin.png")
        # self.coin.Set(16, 24.0, True)
        # self.coin._framewidth = 30

    def Initialize(self):
        return 0

    def shut_down(self):
        return 0
    
    def Update(self, elapsed):
        # self.bomb.Update(elapsed)
        # self.coin.Update(elapsed)
        pass
    
    def Draw(self, screen):    
        
        draw_text("Coin catch (Demo)", 50,
                  globals.screen_width // 2, (globals.screen_height // 2) - 100, 
                  (255, 255, 255), screen)
        
        draw_text("How to play: Catch the jumping numbers", 30,
                globals.screen_width // 2, (globals.screen_height // 2) - 50, 
                (255,255,255), screen)

        draw_text("Demo version 1.0", 35,
                globals.screen_width-110, (globals.screen_height) - 50, 
                (255,255,255), screen)
        
        self.start_button.draw(screen)

        # self.bomb._x = 100
        # self.bomb._y = 100
        # self.bomb.Draw(screen)

        # self.coin._x = 100
        # self.coin._y = 100
        # self.coin.Draw(screen)

    def start_button_clicked(self):
        globals.current_state = GameState()
        globals.current_state.Initialize()

    def handle_event(self, event):
        self.start_button.handle_event(event)