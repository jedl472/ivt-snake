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


class Temporary_gameobject_manager:
    # PRO DOCASNE GAMEOBJEKTY:
    # musi mit: kill (vrati hodnotu framu za jak dlouho bude kilnute, plati hlavne aby fungoval particle system)
    #           update (protoze duvody)

    def __init__(self):
        self.content = [] # content[object, life_countdown]

    def add(self, obj, life):
        self.content.append([obj, life, 0]) # posledni byte je nastaveny na 0 pokud objekt zije, jinak slouzi jako cooldown k zabiti

    def update(self):
        # print("update: ")
        for i in range(len(self.content)):
            # print(self.content[i])
            if self.content[i][1] == 0:
                if self.content[i][2] != 0:
                    self.content[i] = -1
                else:
                    self.content[i][1] = self.content[i][0].kill()
                    self.content[i][2] = 1 # objekt ceka na zabiti
            elif self.content[i][1] != 0:
                self.content[i][0].update()
                self.content[i][1] -= 1


        self.content = [value for value in self.content if value != -1]
        
            


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

    

temp_obj_manager = Temporary_gameobject_manager()


screen_animation = Animation_shake((0, 0), 100, 5)
screen_animation.end()

sample_particle_system = Particle_system(game_surface, (100, 100))

screen_animation_isActive = False
player = Player()
# player = pygame.sprite.GroupSingle()
# player.add(Player())

while True:
    # Process player inputs.
    for event in pygame.event.get():
        player.eventUpdate(event)

        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit
            if event.key == pygame.K_SPACE:
                if screen_animation_isActive == True:
                    screen_animation_isActive = False
                    screen_animation.end()
                else:
                    screen_animation_isActive = True
                    screen_animation.isActive = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            temp_obj_manager.add(Particle_system(game_surface, event.pos), 10)

                

    # Do logical updates here.
    # ...
    player.movementUpdate()
    temp_obj_manager.update()

    GAME_SURFACE_OFSET = screen_animation.pos

    screen.fill("black")
    screen.blit(game_surface, GAME_SURFACE_OFSET)
    game_surface.fill("black")

    # Render the graphics here.
    # ...
    player.imageUpdate()
    screen_animation.update()
    # sample_particle_system.position = (player.snake[-1])

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(GAME_FPS)  

    print("FPS:", clock.get_fps())
