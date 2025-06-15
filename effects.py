import pygame
import random

import global_settings

def lerp(a, b, t):
    return a + (b - a) * t 

class Animation:
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
        # print("update: ", self.phase/self.duration, lerp(self.init_pos[0], self.target_pos[0], self.phase/self.duration), "pos: ", self.pos)
        if self.phase < self.duration:
            self.pos[0] = lerp(self.init_pos[0], self.target_pos[0], self.phase/self.duration)
            self.pos[1] = lerp(self.init_pos[1], self.target_pos[1], self.phase/self.duration)

            self.phase += 1

class Animation_shake(Animation):
    def __init__(self, mother_pos, offset_range, speed):
        super().__init__(mother_pos, mother_pos, speed)

        self.speed = speed
        self.mother_pos = list(mother_pos)
        self.offset_range = offset_range

        self.pos = list(mother_pos)

        self.isActive = True

    def restart(self):
        next_pos = (self.mother_pos[0] + random.randrange(-self.offset_range, self.offset_range), self.mother_pos[1] + random.randrange(-self.offset_range, self.offset_range))
        super().__init__(self.pos, next_pos, self.speed)

    def update(self):
        self.update_lerp()

        if self.phase >= self.duration and self.isActive:
            self.restart()

    def end(self):
        super().__init__(self.pos, self.mother_pos, self.duration)
        self.isActive = False



class Particle(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        
        self.image = pygame.Surface((3, 3))
        self.image.fill("aqua")
        self.speed = 0.3

        self.rect = self.image.get_rect(midbottom = position)

        self.direction = (random.randrange(-10, 10) * self.speed, random.randrange(-10, 10) * self.speed)
        
        self.life = 30 #decrements


    def update(self):
        if self.life <= 0:
            self.kill()
        else: 
            self.life -= 1
            self.rect.x += self.direction[0]
            self.rect.y += self.direction[1]



class Particle_system:
    def __init__(self, surface, position, spawn_cooldown = 0):
        #particle properties
        self.particle_speed = 0.3
        self.particle_life = 30
        
        #particle system
        self.spawn_cooldown = spawn_cooldown
        self.spawn_cooldown_countdown = 0 #kazdym updatem se incrementuje, -1 pokud je objekt neaktivni
        
        self.particles = pygame.sprite.Group()

        self.position = position
        self.surface = surface


    def update(self):
        if self.spawn_cooldown_countdown >= self.spawn_cooldown:
            new_particle = Particle(self.position)
            self.particles.add(new_particle)
            
            self.spawn_cooldown_countdown = 0
        elif self.spawn_cooldown_countdown != -1: 
            self.spawn_cooldown_countdown += 1

        self.particles.draw(self.surface)
        # pygame.draw.circle(self.surface, "red", self.position, 20)
        self.particles.update()
        

    def kill(self):
        kill_delay = self.particle_life - self.spawn_cooldown_countdown
        self.spawn_cooldown_countdown = -1
        return kill_delay
