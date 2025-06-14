import pygame
import random

def lerp(a, b, t):
    return a + (b - a) * t 

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

