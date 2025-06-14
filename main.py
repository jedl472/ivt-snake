import pygame
import random

pygame.init()

SCREEN_SIZE = (1280, 720)
GAME_SURFACE_OFSET = (0, 0)
GAME_FPS = 60

screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

game_surface = pygame.Surface(SCREEN_SIZE)

pygame.draw.rect(game_surface, "aqua", pygame.Rect(SCREEN_SIZE[0]/2-50, SCREEN_SIZE[1]/2-50, 100, 100))

def lerp(a, b, t):
    return a + (b - a) * t 


class player(pygame.sprite.Sprite): 
    pass

class Animation():
    def __init__(self, initial_pos, target_pos, duration):
        self.init_pos = [initial_pos[0], initial_pos[1]]
        self.target_pos = [target_pos[0], target_pos[1]]
        self.duration = duration

        self.pos = self.init_pos
        
        self.phase = 0

    def update_linear(self):
        step = (int((target_pos[0] - initial_pos[0])/duration), int((target_pos[1] - initial_pos[1])/duration))

        if self.phase < self.duration:
            self.pos[0] += step[0]
            self.pos[1] += step[1]

            self.phase += 1

    def update_lerp(self):
        print("update: ", self.phase/self.duration, lerp(self.init_pos[0], self.target_pos[0], self.phase/self.duration), "pos: ", self.pos)
        if self.phase < self.duration:
            self.pos[0] = lerp(self.init_pos[0], self.target_pos[0], self.phase/self.duration)
            self.pos[1] = lerp(self.init_pos[1], self.target_pos[1], self.phase/self.duration)

            self.phase += 1

class Animation_shake(Animation):
    def __init__(self, initial_pos, offset_range)

screen_animation = Animation((0, 0), (200, 200), 200)

while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Do logical updates here.
    # ...
    screen_animation.update_lerp()
    GAME_SURFACE_OFSET = screen_animation.pos

    screen.fill("black")
    screen.blit(game_surface, GAME_SURFACE_OFSET)

    # Render the graphics here.
    # ...

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(GAME_FPS)   
