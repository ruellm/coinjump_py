import math
from animated_image import AnimatedImage
from image_object import ImageObject
import globals
from utilities import draw_text

JUMP_HEIGHT = 600

class JumpingItem:
    def __init__(self):
        self.jumpHeight = JUMP_HEIGHT

        self.halfPI = math.pi / 2
     
        self.jumpHangTime = 1.0
     
        self.jumpSinWaveSpeed = self.halfPI / self.jumpHangTime

        self.jumpSinWavePos = 0
        self.fallMultiplyer = 1.5
        self.grounded = True

        # TODO: Set Base Y!!! 
        # Y =  600 --> Outside of the screens
        self._baseY = globals.screen_height
        self._Y = self._baseY
        self._X = 0

        self.type = 0
        self.fnHitBase = None

        self.didjump = False
        self._width = 50
        self._height = 50

        self.dead = False
        self.spriteList = []
        self.spriteIdx = 0

        self.fnExplodeDone = None
        self.score = 0
        self.alpha = 1.0
        self.alive = True
        self.cx = 0
        self.cy = 0
        self.diff = 0
        self.diff_0 = 0
        self.diff_1 = 0

        self.scale_width = 1
        self.scale_height = 1
        
    def Load(self):
        if self.type == 0 :
            idle = AnimatedImage()
            idle.Load("images/coin_spin.png")

            idle.Set(16, 24.0, True)
            idle._frameWidth = 30   
            
            self.spriteList.append(idle)
            self.spriteList.append(idle)

            self.scale_width = 2
            self.scale_height = 2
            
        else:
            idle = ImageObject()
            idle.Load("images/bomb.png")
        
            self.explode = AnimatedImage()
            self.explode.Load("images/bomb-explode.png")  
            self.explode.Set(7, 20.0, False)
            self.explode._frameWidth = 40  

            self.spriteList.append(idle)
            self.spriteList.append(self.explode)
        
            self.scale_width = 0.8
            self.scale_height = 0.8
            
        # The score per Gem
        scorelist = [2, -1]
        self.score = scorelist[self.type]

    def Update(self, elapsed):
        self.JumpUpdate(elapsed)
        if self.spriteIdx == 1:
            if self.alpha > 0: 
                ALPHA_STEP = 15
                RSZ_STEP = 2

                self.alpha = self.alpha - (ALPHA_STEP * elapsed)
                self.scale_width = self.scale_width + (RSZ_STEP * elapsed)
                self.scale_height = self.scale_height + (RSZ_STEP * elapsed)
            else:
                self.alpha = 0
                self.alive = False
                if self.fnExplodeDone and  (self.type == 1 and self.explode._done) :
                    self.fnExplodeDone(self)
        else:
            self.cx = self._X + (self._width * self.scale_width)/2
            self.cy = self._X + (self._height * self.scale_height)/2

        self.spriteList[self.spriteIdx]._alpha = self.alpha
        self.spriteList[self.spriteIdx].Update(elapsed)

    def Hit(self):
        self.spriteIdx = 1

    def Draw(self, screen):
        self._X = self.cx - ((self._width * self.scale_width)/2)
        self._y = self.cy - ((self._height * self.scale_height)/2)

        self.spriteList[self.spriteIdx]._x = self._X
        self.spriteList[self.spriteIdx]._y = self._Y
        self.spriteList[self.spriteIdx].alpha = self.alpha
        self.spriteList[self.spriteIdx].scale_width = self.scale_width
        self.spriteList[self.spriteIdx].scale_height = self.scale_height
        self.spriteList[self.spriteIdx].Draw(screen)

        if self.spriteIdx == 1 :
            if self.type == 0:
                draw_text("+2", 50, self.cx, self._Y + self._height/2, (255,255,255), screen)
            else:
                draw_text("-1", 50, self.cx, self._Y + self._height/2, (255,0,0), screen)

    def JumpUpdate(self, elapsed):
        if not self.grounded:
            # the last position on the sine wave
            lastHeight = self.jumpSinWavePos

            # the new position on the sine wave
            self.jumpSinWavePos += self.jumpSinWaveSpeed * elapsed;

            # we have fallen off the bottom of the sine wave, so continue falling
            # at a predetermined speed
            if self.jumpSinWavePos >= math.pi :
                self._Y += self.jumpHeight / self.jumpHangTime * self.fallMultiplyer * elapsed
            else:
                self._Y -= (math.sin(self.jumpSinWavePos) - math.sin(lastHeight)) * self.jumpHeight
  
        # we have hit the ground
        if self.IsGround():
            self.grounded = True
            self.jumpSinWavePos = 0
            self._Y = self._baseY
            self._isFalling = False
            if self.fnHitBase != None and self.didjump:
                self.fnHitBase(self)
        
        elif self.grounded: # otherwise we are falling
            self.grounded = False
            # starting falling down the sine wave (i.e. from the top)
            self.jumpSinWavePos = self.halfPI
            
    def Jump(self):
        if self.IsGround():
            self.grounded = False
            self.jumpSinWavePos = 0
            self.didjump = True

    def IsGround(self) -> bool:
        if self._Y < self._baseY:
            return False
        
        return True