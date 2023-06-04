import pygame
import globals
from button import Button
import cv2
import numpy as np
from hand_detector import HandDetector
from jumping_item import JumpingItem

from timer import Timer
from collections import namedtuple
import random
import math
from utilities import draw_text

POINTS_PER_CIRCLE = 2
POINTS_PER_MISTAKE = 1
TOTAL_GAME_SECONDS = 60
BALLS_COUNT = 2

MAX_DIMENSION = 500 # max dimension for too close detection

def boxCollide(rect1, rect2) ->bool :
    return (rect1.x < rect2.x + rect2.w and
        rect1.x + rect1.w > rect2.x and
        rect1.y < rect2.y + rect2.h and
        rect1.h + rect1.y > rect2.y)

class GameState:
    def __init__(self):
        font_size = 50
        self.font = pygame.font.SysFont(None, font_size)  # Use the default system font
        self.hand_detector = HandDetector()

        self.render_width = globals.screen_width
        self.render_height = globals.screen_height
        self.top_padding = 0
        self.left_padding = 0

        pos_x = (globals.screen_width // 2) - 100
        pos_y = (globals.screen_height // 2) + 70
        self.play_again = Button(pos_x, pos_y, 
                                   200, 50, pygame.Color("blue"), pygame.Color("lightblue"), pygame.Color("darkblue"),
                                    "Play Again", pygame.Color("white"), self.font, self.play_again_clicked)
        
    def Initialize(self):
        self.cap = cv2.VideoCapture(0)

        self.score = 0
        self.globalTimer = Timer()
        self.globalTimer.Start()
        self.endGame = False
        
        self.ballList = []
    
    def removeItem(self, item):
        if item in self.ballList:
            self.ballList.remove(item)

    def shut_down(self):
        self.cap.release()
        self.cv2.destroyAllWindows()

    def Update(self, elapsed):
        self.globalTimer.Update()

        self.globalTimerLeft = math.floor(TOTAL_GAME_SECONDS - self.globalTimer._elapsed)
        if self.globalTimerLeft <= 0:
            self.endGame = True
            self.globalTimer.Stop()

        bunos_max = 3
        lack = bunos_max - len(self.ballList)
        m = 0
        while not self.endGame and m < lack:
            chance = random.randint(0, 100)
            if chance % 7 != 0:
                continue
            type = random.randint(0, BALLS_COUNT-1)
            x_loc =  random.randint(0, self.render_width)
            
            item = JumpingItem()
            item._X = self.left_padding + x_loc
            item._y = self.render_height
            item.type = type
            item.fnHitBase = self.hitBase
            item.Load()
            item.Jump()

            self.ballList.append(item)
            m += 1

        for ball in self.ballList:
            ball.Update(elapsed)
            if ball is None:
                break
       
            if self.hand_detector.is_hand_inside_rectangle(ball._X, ball._Y, ball._width, ball._height):
                ball.Hit()
                if ball.type == 0:
                    self.score += POINTS_PER_CIRCLE
                else :
                    self.score -= POINTS_PER_MISTAKE
                    if self.score <= 0:
                        self.score = 0
        
    def ExplodeDOne(self, item):
        self.score += item.score
        self.removeItem(item)

    def hitBase(self, item):
        self.removeItem(item)

    def Draw(self, screen):
        ret, frame = self.cap.read()
        if not ret:
            return
        
        frame = self.capture_frame()
        if frame is None:
           return

        frame = self.hand_detector.detect_hand(frame)

        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(frame, (0, 0))

        for ball in self.ballList:
            ball.Draw(screen)

        if len(self.hand_detector.bboxes) > 0 :
            bbox = self.hand_detector.bboxes[0]
            width = bbox.x_max - bbox.x_min
            height = bbox.y_max - bbox.y_min

            if width > MAX_DIMENSION or height > MAX_DIMENSION :
                draw_text("Player too close to Camera", 80,
                  globals.screen_width // 2, 50, 
                  (100,0,0), screen)
                
        draw_text("Score : " + str(self.score), 50,
                  self.left_padding, 100, (255,255,255), screen)
        
        draw_text("Time : " + str(self.globalTimerLeft), 50,
                  globals.screen_width - 250, 100, (255,255,255), screen)

        draw_text("Demo version 1.0", 35,
                globals.screen_width-110, (globals.screen_height) - 50, 
                (255,255,255), screen)

        if self.endGame:
            draw_text("Game Over", 100,
                  globals.screen_width // 2, globals.screen_height // 2, 
                  (0, 255, 0), screen)
            self.play_again.draw(screen)

    def capture_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Calculate aspect ratios
        frame_ratio = frame.shape[1] / frame.shape[0]
        screen_ratio = globals.screen_width / globals.screen_height

        if frame_ratio > screen_ratio:
            # Frame is wider, adjust height to fit screen
            new_height = int(globals.screen_width / frame_ratio)
            frame_resized = cv2.resize(frame_rgb, (globals.screen_width, new_height))
            top_padding = int((globals.screen_height - new_height) / 2)
            frame_padded = cv2.copyMakeBorder(frame_resized, top_padding, top_padding, 0, 0, cv2.BORDER_CONSTANT)
            self.render_height = new_height
            self.top_padding = top_padding
        else:
            # Frame is taller, adjust width to fit screen
            new_width = int(globals.screen_height * frame_ratio)
            frame_resized = cv2.resize(frame_rgb, (new_width, globals.screen_height))
            left_padding = int((globals.screen_width - new_width) / 2)
            frame_padded = cv2.copyMakeBorder(frame_resized, 0, 0, left_padding, left_padding, cv2.BORDER_CONSTANT)
            self.render_width = new_width
            self.left_padding = left_padding

        return frame_padded
    


    def handle_event(self, event):
       self.play_again.handle_event(event)
    
    def play_again_clicked(self):
        self.Initialize()