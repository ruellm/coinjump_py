import pygame
from animator import Animator
import globals

class AnimatedImage:
    def __init__(self):
        self._frameCount = 1.0
        self._currentFrame = 0
        self._frameWidth = 0
        self._bLoop = True
        self._fnCallback = None

        self._animator = Animator()
        self.called = False
        self._done = False

        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0
        self.image = None
        self.scale_width = 1
        self.scale_height = 1
        self.alpha = 1
       # self.transparent_surface = pygame.Surface((globals.screen_width, globals.screen_height), pygame.SRCALPHA)


    def Load(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self._width = self.rect.width
        self._height = self.rect.height

    def Set(self, frameCount, fps, loop):
        self._bLoop = loop
        self._animator.Set(fps)
        self._frameCount = frameCount
        self._frameWidth = self.rect.width / frameCount
    
    def Update(self, elapsed):
        if self._animator.Update(elapsed):
            self._currentFrame += 1
            if self._bLoop:
                self._currentFrame %= self._frameCount
            elif self._currentFrame >= self._frameCount:
                self._currentFrame = self._frameCount - 1
                if self._fnCallback is not None:
                    if self._bLoop == False and self.called == False :
                        self._fnCallback()
                        self.called = True
                        self._done = True
    
    def Draw(self, screen):
        sourceX = self._frameWidth * self._currentFrame

        scaled_width, scaled_height = self._frameWidth * self.scale_width, self._height * self.scale_width
        source_rect = pygame.Rect(sourceX, 0, self._frameWidth, self._height)
        dest_rect = pygame.Rect(self._x , self._y, scaled_width, scaled_height)
        self.image.set_alpha(self.alpha * 255)
        #self.transparent_surface.fill((0, 0, 0, 0))  # Clear the transparent surface
        screen.blit(pygame.transform.scale(self.image.subsurface(source_rect), (scaled_width, scaled_height)), dest_rect)
       # screen.blit(self.transparent_surface, dest_rect)