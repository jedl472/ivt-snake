import pygame

import global_settings
import effects


class Player(pygame.sprite.Sprite): 
    def __init__(self, surface):
        super().__init__()
        self.snake = [(200, 200), (210, 200), (220, 200), (230, 200), (240, 200)]
        self.direction = [1, 0]
        self.scale = 20
        self.length = 5
        self.speed = 5 #framy, cim vetsi tim pomalejsi
        self.speedCountdown = 0

        self.dashCountdown = 0
        self.dashDuration = global_settings.GAME_FPS /2

        self.reference_pos = ((self.snake[-1][0] + (self.scale/2), self.snake[-1][1] + (self.scale/2)))

        self.skin = pygame.Surface((self.scale,self.scale))
        self.skin.fill((255, 255, 255))
        self.head = pygame.Surface((self.scale, self.scale))
        self.head.fill((200, 200, 200))

        self.particle_system_manager = effects.Temporary_gameobject_manager()
        self.animation_manager = effects.Temporary_gameobject_manager()

        self.items = [] # list poddružených objektů

        self.surface = surface
    
    def eventUpdate(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and self.direction != [1, 0]:
                self.direction = [-1, 0]
            if event.key == pygame.K_d and self.direction != [-1, 0]:
                self.direction = [1, 0]
            if event.key == pygame.K_w and self.direction != [0, 1]:
                self.direction = [0, -1]
            if event.key == pygame.K_s and self.direction != [0, -1]:
                self.direction = [0, 1]
            
            if event.key == pygame.K_UP:
                self.length += 1
            if event.key == pygame.K_DOWN:
                self.length -= 1

            if event.key == pygame.K_e:
                self.dashCountdown = self.dashDuration


    def imageUpdate(self):
        for snake_pos in self.snake[0:-1]:
            self.surface.blit(self.skin, snake_pos)
        self.surface.blit(self.head, self.snake[-1])

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

    def update(self):
        #vzhledem k tomu, ze eventUpdate potrebuje typ eventu, musí se volat oddelene
        self.reference_pos = ((self.snake[-1][0] + (self.scale/2), self.snake[-1][1] + (self.scale/2)))
        
        self.particle_system_manager.update()
        for i in range(len(self.particle_system_manager.content)):
            self.particle_system_manager.content[i][0].position = self.reference_pos


        self.animation_manager.update()
        for i in range(len(self.animation_manager.content)):
            global_settings.GAME_SURFACE_OFSET = self.animation_manager.content[i][0].pos
        

        self.movementUpdate()
        self.imageUpdate()
        self.dashUpdate()

    def dashUpdate(self):
        if self.dashCountdown == self.dashDuration:
            self.animation_manager.add(effects.Animation_shake((0, 0), 40, 3), self.dashDuration)
        
        if self.dashCountdown != 0:
            if (self.dashDuration * 2/8) < self.dashCountdown < self.dashDuration:
                self.speed = 0
                self.particle_system_manager.add(effects.Particle_system(self.surface, self.reference_pos, direction=self.direction, spawn_cooldown=1/60), 2)

            elif 0 < self.dashCountdown < self.dashDuration * 2/8:
                self.speed = 1000

            self.dashCountdown -= 1
        else:
            self.speed = 5

