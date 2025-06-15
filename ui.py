import pygame

import global_settings

pygame.font.init()

menu_font1 = pygame.font.Font("src/fonts/LeagueSpartan-Bold.ttf", 50)

class Main_menu:
    def __init__(self):
        self.active = True

        self.surface = pygame.Surface(global_settings.SCREEN_SIZE)
        self.surface.set_colorkey((0, 0, 0))
    
    def eventUpdate(self, event):
        pass

    def imageUpdate(self):
        if self.active:
            self.surface.fill("black")
            # pygame.draw.rect(self.surface, "white", (40, 40, global_settings.SCREEN_SIZE[0]-80, global_settings.SCREEN_SIZE[1]-80), 5)
            
            buffer_surface = menu_font1.render(f"Hra na IVT", True, "White")
            self.surface.blit(buffer_surface, ((global_settings.SCREEN_SIZE[0]-buffer_surface.get_width())/2, 50)) # uzitecny kus kodu co vycentruje surface
            
        else:
            self.surface.fill("black")

    def update(self):
        self.imageUpdate()



