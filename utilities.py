import pygame

def draw_text(txt, size, x, y, color, screen):
    font = pygame.font.SysFont(None, size)
    text = font.render(txt, True, color) 

    # Position the text on the screen
    text_rect = text.get_rect()
    text_rect.center = x, y

    # Draw the text on the screen
    screen.blit(text, text_rect)