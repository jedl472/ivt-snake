import pygame
import random
import math

import global_settings
import effects
import utils


class Player(pygame.sprite.Sprite): 
    def __init__(self, surface, start_position=160, keymap=[pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_e, pygame.K_SPACE], opponent_player=None):
        super().__init__()
        self.surface = surface
        
        self.start_position = start_position
        self.keymap = keymap

        self.opponent_player = opponent_player

        self.snake = [(start_position, start_position), (start_position + 10, start_position), (start_position + 20, start_position), (start_position + 30, start_position), (start_position + 40, start_position)]
        self.direction = [1, 0]
        self.scale = 20
        self.length = 5
        self.speed = 5 #framy, cim vetsi tim pomalejsi
        self.speedCountdown = 0

        self.battery = 6 # promenna co obsahuje kolik ma hrac nabyto na provadeni akci jako strileni nebo dash
                         # vypocitava se pomoci ni renderovani hrace

        self.battery_to_segments = 3 # RO, obsahuje kolik battery je na jeden segment hada

        self.dashCountdown = 0
        self.dashDuration = 20
        
        self.surpressMovementUpdate = False
        self.movementUpdateLock = False # RO

        self.dead = False
        self.deathAnimationCountdown = 0
        self.deathAnimationSpeed = utils.fsm(13)

        self.reference_pos = ((self.snake[-1][0] + (self.scale/2), self.snake[-1][1] + (self.scale/2)))
        
        self.default_color_skin = (255, 255, 255)
        self.default_color_head = (200, 200, 200)

        self.skin = pygame.Surface((self.scale,self.scale))
        self.skin.fill(self.default_color_skin)
        self.head = pygame.Surface((self.scale, self.scale))
        self.head.fill(self. default_color_head)

        self.rect = self.head.get_rect()

        self.particle_system_manager = utils.Temporary_gameobject_manager()
        self.animation_manager = utils.Temporary_gameobject_manager()
        self.bullet_manager = Bullet_manager(self.surface)

    
    def eventUpdate(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == self.keymap[0] and self.direction != [1, 0] and not self.movementUpdateLock:
                self.direction = [-1, 0]
                self.movementUpdateLock = True
            elif event.key == self.keymap[1] and self.direction != [-1, 0] and not self.movementUpdateLock:
                self.direction = [1, 0]
                self.movementUpdateLock = True
            elif event.key == self.keymap[2]  and self.direction != [0, 1] and not self.movementUpdateLock:
                self.direction = [0, -1]
                self.movementUpdateLock = True
            elif event.key == self.keymap[3] and self.direction != [0, -1] and not self.movementUpdateLock:
                self.direction = [0, 1]
                self.movementUpdateLock = True
            
            # if event.key == pygame.K_UP:
            #     self.battery += 1
            # if event.key == pygame.K_DOWN and self.battery != 0:
            #     self.battery -= 1

            if event.key == self.keymap[4] and self.battery > 1:
                self.dashCountdown = self.dashDuration

                self.battery -= 2

            if event.key == self.keymap[5] and self.battery > 0:
                self.bullet_manager.spawn(self.direction)
                
                self.battery -= 1


    def imageUpdate(self):
        # zde se pocita zbarveni hada (pouze) na zaklade self.battery
        self.length = math.ceil(self.battery / self.battery_to_segments) + 2

        # last_segment_color_coef = 1
        # if self.battery % self.battery_to_segments != 0: last_segment_color_coef = 1/(self.battery % self.battery_to_segments)
        
        death_color_override = None
        if self.deathAnimationCountdown > 0: death_color_override = (0, 0, 0)
        else: death_color_override = None

        last_segment_color = None
        if self.battery % self.battery_to_segments == 0: last_segment_color = (255, 255, 255)
        if self.battery % self.battery_to_segments == 1: last_segment_color = (0, 100, 100)
        if self.battery % self.battery_to_segments == 2: last_segment_color = (100, 255, 255)

        _skin_fill = None
        
        for snake_pos in self.snake[0:-1]:
            self.surface.blit(self.skin, snake_pos)
        
        self.surface.blit(self.head, self.snake[-1])
        if (self.death and death_color_override != None): _skin_fill = death_color_override 
        else: _skin_fill = last_segment_color 
        self.skin.fill(_skin_fill)
        self.surface.blit(self.skin, self.snake[0])

        if (self.death and death_color_override != None): _skin_fill = death_color_override 
        else: _skin_fill = self.default_color_skin 
        self.skin.fill(_skin_fill)

    def movementUpdate(self):
        self.movementUpdateLock = False
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

            if len(self.snake) > self.length and self.length > 0:
                self.snake.pop(0)
            if len(self.snake) < self.length:
                self.snake.insert(0, self.snake[0])
            
            self.speedCountdown = 0
        else: self.speedCountdown += 1

    def update(self, food_sprite_group):
        self.reference_pos = ((self.snake[-1][0] + (self.scale/2), self.snake[-1][1] + (self.scale/2)))

        if self.dead:
            if self.deathAnimationCountdown <= -self.deathAnimationSpeed:
                self.deathAnimationCountdown = self.deathAnimationSpeed
            else:
                self.deathAnimationCountdown -= 1
        else:
            self.particle_system_manager.update()
            for i in range(len(self.particle_system_manager.content)):
                self.particle_system_manager.content[i][0].position = self.reference_pos


            self.animation_manager.update()
            for i in range(len(self.animation_manager.content)):
                global_settings.GAME_SURFACE_OFSET = self.animation_manager.content[i][0].pos

            self.bullet_manager.position = self.reference_pos
            self.bullet_manager.update()

            if (self.wallCollision() or self.selfCollision()) or self.opponentBodyCollision() or self.opponentBulletCollision():
                self.death()

            #vzhledem k tomu, ze eventUpdate potrebuje typ eventu, musí se volat oddelene
            if not self.surpressMovementUpdate: self.movementUpdate()
            self.dashUpdate()
            self.foodUpdate(food_sprite_group)

        self.imageUpdate()

    def dashUpdate(self):
        if self.dashCountdown == self.dashDuration:
            self.animation_manager.add(effects.Animation_shake((0, 0), 40, 3), (self.dashDuration))
        
        if self.dashCountdown != 0:
            if (self.dashDuration * 3/4) < self.dashCountdown < self.dashDuration:
                self.speed = 0
                self.particle_system_manager.add(effects.Particle_system(self.surface, self.reference_pos, direction=self.direction, spawn_cooldown=0), 2)
            elif self.dashDuration * 2/8 < self.dashCountdown < self.dashDuration * 1/2:
                pass 

            elif 0 < self.dashCountdown < self.dashDuration * 2/8:
                self.speed = 1000

            self.dashCountdown -= 1
        else:
            self.speed = 5

    def foodUpdate(self, food_sprite_group):
        for i in food_sprite_group.sprites():
            if i.rect.collidepoint(self.reference_pos):
                i.kill()
                self.battery += self.battery_to_segments

                self.particle_system_manager.add(effects.Particle_system(self.surface, self.reference_pos, particle_life=15, spawn_cooldown=0.0, color="red"), 7)
            

    def selfCollision(self):
        return self.snake[-1] in self.snake[0:-1]
    
    def wallCollision(self):
        is_collision = self.snake[len(self.snake)-1][0] >= global_settings.SCREEN_SIZE[0] or self.snake[len(self.snake)-1][0] < 0 or self.snake[len(self.snake)-1][1] >= global_settings.SCREEN_SIZE[1] or self.snake[len(self.snake)-1][1] < 0

        return is_collision 

    def death(self):
        self.speed = 100000
        self.dead = True

    def opponentBodyCollision(self):
        if self.opponent_player != None:
            is_collision = False

            if not is_collision:
                is_collision = self.snake[-1] in self.opponent_player.snake[0:-1]

            return is_collision

    def opponentBulletCollision(self):
        coll_rect_list = []
        for i in self.snake:
            coll_rect_list.append(pygame.Rect(i[0], i[1], 20, 20))

        for i in self.opponent_player.bullet_manager.content.sprites():
            for selfrect in coll_rect_list:
                if pygame.Rect.colliderect(selfrect, i.rect):
                    return True

        return False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction):
        super().__init__()

        self.sprite_size = None
        if direction[1] == 0: self.sprite_size = (10, 5)
        elif direction[0] == 0: self.sprite_size = (5, 10)

        self.image = pygame.Surface(self.sprite_size)
        self.image.fill("aqua")

        self.rect = self.image.get_rect(midbottom = position)
        
        self.direction = direction
        self.speed = 15 # tady je speed implementovany dobre, 

    def update(self):
        self.rect.x += self.direction[0] * utils.fsm(self.speed)
        self.rect.y += self.direction[1] * utils.fsm(self.speed)

        if (not 0 <= self.rect.x <= global_settings.SCREEN_SIZE[0]) or (not 0 <= self.rect.y <= global_settings.SCREEN_SIZE[1]):
            self.kill()


class Bullet_manager:
    def __init__(self, surface, position = (0, 0)):
        self.surface = surface

        self.content = pygame.sprite.Group()
        self.potition = position

    def spawn(self, direction):
        new_bullet = Bullet(self.position, direction)

        self.content.add(new_bullet)

    def update(self):
        self.content.update()
        self.content.draw(self.surface)


class Food(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill("red")

        self.rect = self.image.get_rect(midbottom = position)
        
        self.position = position


    def update(self):
        pass 


class Food_manager:
    def __init__(self, surface, food_amount=5):
        self.surface = surface
        
        self.food_amount = food_amount

        self.content = pygame.sprite.Group()

    def spawn(self):
        spawn_position = list(utils.random_screen_position(borders=20))   # aby se jidlo spawnovalo na nasobcich 20 a tim padem vypadalo hezky
        for i in range(2): spawn_position[i] = round(spawn_position[i]/20) * 20
        spawn_position[0] += 10
        new_food = Food(spawn_position)

        self.content.add(new_food)

    def update(self):
        if len(self.content.sprites()) < self.food_amount:
            self.spawn()

        self.content.update()
        self.content.draw(self.surface)
