import pygame

class ImageButton:
    def __init__(self, x, y, image_path):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_hovered = False
        self.is_clicked = False

    def draw(self, screen):
        if self.is_hovered:
            # Add hover effect here (e.g., change image color, scale, etc.)
            pass
        if self.is_clicked:
            # Add click effect here (e.g., change image color, scale, etc.)
            pass
        screen.blit(self.image, self.rect)

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
                    print("Button Clicked!")
                    # Perform desired action here
                self.is_clicked = False
