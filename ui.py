import pygame

import global_settings

pygame.font.init()

font_nadpis = pygame.font.Font("src/fonts/LeagueSpartan-Bold.ttf", 70)
font_podnadpis = pygame.font.Font("src/fonts/LeagueSpartan-Bold.ttf", 30)

font_tlacitka = pygame.font.Font("src/fonts/LeagueSpartan-Bold.ttf", 50)

font_score = pygame.font.Font("src/fonts/LeagueSpartan-Bold.ttf", 20)


img_menu = pygame.image.load("src/main_screen.png")
img_menu.set_colorkey((0, 0, 0))


class Main_menu:
    def __init__(self, startButtonPressed=None, active=False):
        self.active = active

        self.startButtonPressed = startButtonPressed

        self.surface = pygame.Surface(global_settings.SCREEN_SIZE)
        self.surface.set_colorkey((0, 0, 0))

        self.buttons = pygame.sprite.Group()

        self.buttons.add(Button(self.surface, ((global_settings.SCREEN_SIZE[0]/2)-(250/2), 300), (250, 100), label="START", onClick=startButtonPressed))
    
    def eventUpdate(self, event):
        for i in self.buttons.sprites():
            i.eventUpdate(event)
            

    def imageUpdate(self):
        if self.active:
            self.surface.fill("black")
            self.surface.blit(img_menu, (0, 0))

            # pygame.draw.rect(self.surface, "white", (40, 40, global_settings.SCREEN_SIZE[0]-80, global_settings.SCREEN_SIZE[1]-80), 5)
            
            buffer_surface = font_nadpis.render(f"Hra na IVT", True, "White")
            self.surface.blit(buffer_surface, ((global_settings.SCREEN_SIZE[0]-buffer_surface.get_width())/2, 50)) # uzitecny kus kodu co vycentruje surface
            buffer_surface = font_podnadpis.render(f"Nejakej efekt? jakoze bum", True, "aqua")
            self.surface.blit(buffer_surface, ((global_settings.SCREEN_SIZE[0]-buffer_surface.get_width())/2, 130)) # uzitecny kus kodu co vycentruje surface
            self.buttons.update()
            self.buttons.draw(self.surface)

            self.surface.blit(img_menu, (0, 0))
            
        else:
            self.surface.fill("black")

    def update(self):
        self.imageUpdate()




class Button(pygame.sprite.Sprite):
    def __init__(self, target_surface, position, size, onClick=None, label="<button>"):
        super().__init__()
        self.target_surface = target_surface

        self.position = position
        self.size = size
        self.label = label

        self.onClick = onClick

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect(midbottom=position)

        self.collider_rect = self.rect

    def update(self):
        self.collider_rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        if not self.collider_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.target_surface, "white", (self.position[0], self.position[1], self.size[0], self.size[1]), 5)

            buffer_surface = font_tlacitka.render(self.label, True, "White")
            self.target_surface.blit(buffer_surface, (self.position[0] + (self.size[0]/2) - (buffer_surface.get_size()[0]/2), self.position[1] + (self.size[1]/2) - (buffer_surface.get_size()[1]/2)))       
        else:
            pygame.draw.rect(self.target_surface, "white", (self.position[0], self.position[1], self.size[0], self.size[1]))
            pygame.draw.rect(self.target_surface, "black", (self.position[0], self.position[1], self.size[0], self.size[1]), 5)


            buffer_surface = font_tlacitka.render(self.label, True, "black")
            self.target_surface.blit(buffer_surface, (self.position[0] + (self.size[0]/2) - (buffer_surface.get_size()[0]/2), self.position[1] + (self.size[1]/2) - (buffer_surface.get_size()[1]/2))) 
        
        # self.image.blit(self.target_surface, (0, 0))

    def eventUpdate(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.collider_rect.collidepoint(pygame.mouse.get_pos()):
                self.onClick()


class Score_overlay:
    def __init__(self, active=False):
        self.active = active
        
        self.surface = pygame.Surface(global_settings.SCREEN_SIZE)
        self.surface.set_colorkey((0, 0, 0))

    def update(self, scores):
        if self.active:
            buffer_surface = font_nadpis.render(f"P1: {scores[0]}", True, "White")
            self.surface.blit(buffer_surface, (50, 50))

            buffer_surface = font_nadpis.render(f"P2: {scores[1]}", True, "White")
            self.surface.blit(buffer_surface, (global_settings.SCREEN_SIZE[0] - 50 - buffer_surface.get_size()[0], 50))
        else:
            self.surface.fill("black")
