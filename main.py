import pygame
import random

from effects import *

pygame.init()

SCREEN_SIZE = (1280, 720)
GAME_SURFACE_OFSET = (0, 0)
GAME_FPS = 60

screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

game_surface = pygame.Surface(SCREEN_SIZE)

pygame.draw.rect(game_surface, "aqua", pygame.Rect(SCREEN_SIZE[0]/2-50, SCREEN_SIZE[1]/2-50, 100, 100))




class Player(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()

        self.snake = [(200, 200), (210, 200), (220, 200), (230, 200), (240, 200)]

        self.direction = [1, 0]
        self.scale = 20
        
        self.length = 5

        self.speed = 5
        self.speedCountdown = 0

        self.skin = pygame.Surface((self.scale,self.scale))
        self.skin.fill((255, 255, 255))

        self.head = pygame.Surface((self.scale, self.scale))
        self.head.fill((200, 200, 200))
    
    def eventUpdate(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.direction = [-1, 0]
            if event.key == pygame.K_d:
                self.direction = [1, 0]
            if event.key == pygame.K_w:
                self.direction = [0, -1]
            if event.key == pygame.K_s:
                self.direction = [0, 1]
            
            if event.key == pygame.K_UP:
                self.length += 1
            if event.key == pygame.K_DOWN:
                self.length -= 1


    def imageUpdate(self):
        for snake_pos in self.snake[0:-1]:
            game_surface.blit(self.skin, snake_pos)
        game_surface.blit(self.head, self.snake[-1])

    def movementUpdate(self):
        if self.speedCountdown >= self.speed:
            if self.direction == [1, 0]:
                self.snake.append((self.snake[len(self.snake)-1][0] + self.scale , self.snake[len(self.snake)-1][1]))
            elif self.direction == [0, -1]:
                self.snake.append((self.snake[len(self.snake)-1][0] , self.snake[len(self.snake)-1][1] - self.scale))
            elif self.direction == [0, 1]:
                self.snake.append((self.snake[len(self.snake)-1][0] , self.snake[len(self.snake)-1][1] + self.scale))
            elif self.direction == [-1, 0]:        
                self.snake.append((self.snake[len(self.snake)-1][0] - self.scale , self.snake[len(self.snake)-1][1]))
            self.snake.pop(0)

            if len(self.snake) > self.length:
                self.snake.pop(0)
            if len(self.snake) < self.length:
                self.snake.insert(0, self.snake[0])
            
            self.speedCountdown = 0
        else: self.speedCountdown += 1



screen_animation = Animation_shake((0, 0), 100, 5)
screen_animation.end()

screen_animation_isActive = False
player = Player()


while True:
    # Process player inputs.
    for event in pygame.event.get():
        player.eventUpdate(event)

        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if screen_animation_isActive == True:
                    screen_animation_isActive = False
                    screen_animation.end()
                else:
                    screen_animation_isActive = True
                    screen_animation.isActive = True
                
    screen_animation.update()

    # Do logical updates here.
    # ...
    player.movementUpdate()

    GAME_SURFACE_OFSET = screen_animation.pos

    screen.fill("black")
    screen.blit(game_surface, GAME_SURFACE_OFSET)
    game_surface.fill("black")

    # Render the graphics here.
    # ...
    player.imageUpdate()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(GAME_FPS)   
