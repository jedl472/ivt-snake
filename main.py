from math import floor
import pygame
import random

import effects
import ui
import global_settings
import game
import utils

pygame.init()

screen = pygame.display.set_mode(global_settings.SCREEN_SIZE)
clock = pygame.time.Clock()

game_surface = pygame.Surface(global_settings.SCREEN_SIZE)
game_surface.set_colorkey((0, 0, 0))


menu_state = 0
def menu_button_start():
    global menu_state
    menu_state = 1
    main_menu.active = False


main_menu = ui.Main_menu(startButtonPressed=menu_button_start, active=True)


food_manager = game.Food_manager(game_surface)

player1 = game.Player(game_surface)
player2 = game.Player(game_surface, start_position=400)
player2.keymap = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT, pygame.K_SLASH]

player2.opponent_player = player1
player1.opponent_player = player2

players = [player1, player2]

while True:
    global_settings.REAL_GAME_FPS = clock.get_fps()
    for event in pygame.event.get():
        for i in players: i.eventUpdate(event)
        main_menu.eventUpdate(event)

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            raise SystemExit
   
    screen.fill("black") # cerna

    print(menu_state)

    match menu_state:
        case 0:
            screen.blit(main_menu.surface, (0, 0))
            main_menu.update()

        case 1:
            print("test")
            screen.blit(game_surface, global_settings.GAME_SURFACE_OFSET)
            screen.blit(main_menu.surface, (0, 0))
            game_surface.fill("black") # cerna

            for i in players: i.update(food_manager.content)
            main_menu.update()

            food_manager.update()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(global_settings.SET_GAME_FPS)  


