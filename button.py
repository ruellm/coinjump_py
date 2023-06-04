import pygame

class Button:
    def __init__(self, x, y, width, height, color, hover_color, click_color, text, text_color, font, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.click_color = click_color
        self.text = text
        self.text_color = text_color
        self.font = font
        self.callback = callback
        self.is_hovered = False
        self.is_clicked = False

    def draw(self, screen):
        if self.is_clicked:
            pygame.draw.rect(screen, self.click_color, self.rect)
        elif self.is_hovered:
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, pygame.Color("black"), self.rect, 2)
        text_render = self.font.render(self.text, True, self.text_color)
        text_rect = text_render.get_rect(center=self.rect.center)
        screen.blit(text_render, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.is_hovered = True
            else:
                self.is_hovered = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.is_clicked = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.is_clicked and self.rect.collidepoint(event.pos):
                    self.callback()  # Call the callback function
                self.is_clicked = False