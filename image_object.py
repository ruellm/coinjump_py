import pygame
import globals

class ImageObject:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._width = 0
        self._height = 0
        self.image = None
        self.scale_width = 1
        self.scale_height = 1
        self.alpha = 1
        #self.transparent_surface = pygame.Surface((globals.screen_width, globals.screen_height), pygame.SRCALPHA)
        
    def Load(self, path):
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect()
        self._width = self.rect.width
        self._height = self.rect.height
    
    def Update(self, elapsed):
        pass

    def Draw(self, screen):
        scaled_width, scaled_height = self._width * self.scale_width, self._height * self.scale_width
        source_rect = pygame.Rect(0, 0, self._width, self._height)
        dest_rect = pygame.Rect(self._x , self._y, scaled_width, scaled_height)
        self.image.set_alpha(self.alpha * 255)
        #self.transparent_surface.fill((0, 0, 0, 0))  # Clear the transparent surface
        screen.blit(pygame.transform.scale(self.image.subsurface(source_rect), (scaled_width, scaled_height)), dest_rect)
        #screen.blit(self.transparent_surface, dest_rect)