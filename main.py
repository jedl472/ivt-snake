import pygame
import random

from effects import *
import ui
import global_settings

pygame.init()

screen = pygame.display.set_mode(global_settings.SCREEN_SIZE)
clock = pygame.time.Clock()

game_surface = pygame.Surface(global_settings.SCREEN_SIZE)
game_surface.set_colorkey((0, 0, 0)) # vsechno cerne se nebude blitovat (v podstate alfa kanal, ale rychlejsi a jednoudsi)

debug_font = pygame.font.Font("src/fonts/arial.ttf", 20)


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
        self.speed = 5 #framy, cim vetsi tim pomalejsi
        self.speedCountdown = 0

        self.dashCountdown = 0
        self.dashDuration = global_settings.GAME_FPS /2

        self.reference_pos = ((self.snake[-1][0] + (self.scale/2), self.snake[-1][1] + (self.scale/2)))

        self.skin = pygame.Surface((self.scale,self.scale))
        self.skin.fill((255, 255, 255))
        self.head = pygame.Surface((self.scale, self.scale))
        self.head.fill((200, 200, 200))

        self.particle_system_manager = Temporary_gameobject_manager()
        self.animation_manager = Temporary_gameobject_manager()

        self.items = [] # list poddružených objektů
    
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
            self.animation_manager.add(Animation_shake((0, 0), 40, 3), self.dashDuration)
        
        if self.dashCountdown != 0:
            if (self.dashDuration * 2/8) < self.dashCountdown < self.dashDuration:
                self.speed = 0
                self.particle_system_manager.add(Particle_system(game_surface, self.reference_pos, direction=self.direction, spawn_cooldown=1/60), 2)

            elif 0 < self.dashCountdown < self.dashDuration * 2/8:
                self.speed = 1000

            self.dashCountdown -= 1
        else:
            self.speed = 5


    

screen_animation = Animation_shake((0, 0), 100, 5)
screen_animation.kill()
screen_animation_isActive = False

main_menu = ui.Main_menu()

player = Player()
# player = pygame.sprite.GroupSingle()
# player.add(Player())

test_particle_system = Particle_system(game_surface, (100, 100), direction=([0, 1]))

while True:
    # Process player inputs.
    for event in pygame.event.get():
        player.eventUpdate(event)
        main_menu.eventUpdate(event)

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if screen_animation_isActive == True:
                    screen_animation_isActive = False
                    screen_animation.kill()
                else:
                    screen_animation_isActive = True
                    screen_animation.isActive = True
            if event.key == pygame.K_p:
                player.particle_system_manager.add(Particle_system(game_surface, player.reference_pos), 5)


            if event.key == pygame.K_x:
                main_menu.active = not main_menu.active
                

        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     player.particle_system_manager.add(Particle_system(game_surface, event.pos), 5)
                


    screen.fill("black") # cerna
    screen.blit(game_surface, global_settings.GAME_SURFACE_OFSET)
    screen.blit(main_menu.surface, (0, 0))
    game_surface.fill("black") # cerna

    global_settings.GAME_SURFACE_OFSET = screen_animation.pos
    screen_animation.update()

    player.update()
    main_menu.update()

    #FPS - TODO: pridat do debug surface
    score_surface = debug_font.render(f"FPS: {clock.get_fps()}", True, "White")
    screen.blit(score_surface, (20 , 20))

    test_particle_system.update()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(global_settings.GAME_FPS)  
