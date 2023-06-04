import pygame
import pygame.camera
import pygame.image
import sys
from menu_state import MenuState
import time
import globals

BLACK = (0, 0, 0)

def main():
    pygame.init()
    pygame.camera.init()

    screen_info = pygame.display.Info()
    width, height = screen_info.current_w, screen_info.current_h

    screen = pygame.display.set_mode((width, height))
    globals.screen_width = width
    globals.screen_height = height
    
    globals.current_state = MenuState()
    globals.current_state.Initialize()

    last_time = time.time()
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                globals.current_state.shut_down()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
            globals.current_state.handle_event(event)

         # Clear the screen
        screen.fill(BLACK)
        current_time = time.time()
        elapsed = (current_time - last_time)
        last_time = current_time

        globals.current_state.Update(elapsed)
        globals.current_state.Draw(screen)

        pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()
