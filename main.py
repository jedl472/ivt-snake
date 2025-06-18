from math import floor
import pygame
import random
import time

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
    score_overlay.active = True


main_menu = ui.Main_menu(startButtonPressed=menu_button_start, active=True)
score_overlay = ui.Score_overlay(active=False)

food_manager = game.Food_manager(game_surface, food_amount=10)

player_scores = [0, 0]

player1 = None
player2 = None

def init_players():
    global player1
    global player2
    player1 = game.Player(game_surface)
    player2 = game.Player(game_surface, start_position=400)
    player2.keymap = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SLASH, pygame.K_RSHIFT]

    player2.opponent_player = player1
    player1.opponent_player = player2

init_players()

while True:
    global_settings.REAL_GAME_FPS = clock.get_fps()
    for event in pygame.event.get():
        player1.eventUpdate(event)
        player2.eventUpdate(event)
        main_menu.eventUpdate(event)

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and menu_state == 2:
            player1 = None
            player2 = None

            init_players()
            score_overlay.active = False

            game_surface.fill("black")
            pygame.display.flip()

            menu_state = 1


        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            global_settings.FLAG_DEBUG = not global_settings.FLAG_DEBUG

            
   
    screen.fill("black")

    match menu_state:
        case 0:
            game_surface.fill("black")
            screen.blit(main_menu.surface, (0, 0))
            main_menu.update()

        case 1:
            if global_settings.FLAG_DEBUG: player2.speed = 10000
            screen.blit(game_surface, global_settings.GAME_SURFACE_OFSET)
            screen.blit(main_menu.surface, (0, 0))
            game_surface.fill("black") # cerna
            
            players = [player1, player2]
            for i in enumerate(players): 
                i[1].update(food_manager.content)

                if i[1].dead:
                    menu_state = 2
                    player_scores[not i[0]] += 1
            main_menu.update()

            food_manager.update()


        case 2:
            score_overlay.active = True
            score_overlay.surface.fill("black")
            screen.blit(game_surface, global_settings.GAME_SURFACE_OFSET)
            score_overlay.update(player_scores)
            screen.blit(score_overlay.surface, (0, 0))

            for i in players: 
                i.surpressMovementUpdate = True
                i.update(food_manager.content)

            pygame.display.flip()


    pygame.display.flip()  # Refresh on-screen display
    clock.tick(global_settings.SET_GAME_FPS)  


