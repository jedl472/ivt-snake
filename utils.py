import random

import global_settings

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

# frames speed modifier - vezme si jako parametr nejakou uzivatelem zadanou rychlost a zahrne aktualni fps
# aby rychlost hry nebyla zavisla na frameratu
def fsm(speed):
   coef = 60 / global_settings.REAL_GAME_FPS 

   return int(speed * coef)

def random_screen_position(borders = 0):
    return (random.randrange(borders, global_settings.SCREEN_SIZE[0]-borders), random.randrange(borders, global_settings.SCREEN_SIZE[1]-borders))
