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

menu_state = 1
main_menu = ui.Main_menu()

food_manager = game.Food_manager(game_surface)

players = [game.Player(game_surface)]

while True:
    global_settings.REAL_GAME_FPS = clock.get_fps()
    for event in pygame.event.get():
        for i in players: i.eventUpdate(event)
        main_menu.eventUpdate(event)

        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            raise SystemExit

    screen.fill("black") # cerna
    screen.blit(game_surface, global_settings.GAME_SURFACE_OFSET)
    screen.blit(main_menu.surface, (0, 0))
    game_surface.fill("black") # cerna

    for i in players: i.update(food_manager.content)
    main_menu.update()

    food_manager.update()
    pygame.display.flip()  # Refresh on-screen display
    clock.tick(global_settings.SET_GAME_FPS)  

# print(utils.random_screen_position())
# pygame.init()
#
# screen = pygame.display.set_mode(global_settings.SCREEN_SIZE)
# clock = pygame.time.Clock()
#
# game_surface = pygame.Surface(global_settings.SCREEN_SIZE)
# game_surface.set_colorkey((0, 0, 0)) # vsechno cerne se nebude blitovat (v podstate alfa kanal, ale rychlejsi a jednoudsi)
#
# debug_font = pygame.font.Font("src/fonts/arial.ttf", 20)
#
#
# screen_animation = effects.Animation_shake((0, 0), 100, 5)
# screen_animation.kill()
# screen_animation_isActive = False
#
# main_menu = ui.Main_menu()
#
# food_manager = game.Food_manager(game_surface)
#
# player = game.Player(game_surface)
# # player = pygame.sprite.GroupSingle()
# # player.add(Player())
#
# test_particle_system = effects.Particle_system(game_surface, (100, 100), direction=([0, 1]))
#
# while True:
#     global_settings.REAL_GAME_FPS = clock.get_fps()
#
#     # Process player inputs.
#     for event in pygame.event.get():
#         player.eventUpdate(event)
#         main_menu.eventUpdate(event)
#
#         if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
#             pygame.quit()
#             raise SystemExit
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_SPACE:
#                 if screen_animation_isActive == True:
#                     screen_animation_isActive = False
#                     screen_animation.kill()
#                 else:
#                     screen_animation_isActive = True
#                     screen_animation.isActive = True
#             if event.key == pygame.K_p:
#                 player.particle_system_manager.add(effects.Particle_system(game_surface, player.reference_pos), 5)
#
#
#             if event.key == pygame.K_x:
#                 main_menu.active = not main_menu.active
#
#
#         # if event.type == pygame.MOUSEBUTTONDOWN:
#         #     player.particle_system_manager.add(Particle_system(game_surface, event.pos), 5)
#
#
#
#     screen.fill("black") # cerna
#     screen.blit(game_surface, global_settings.GAME_SURFACE_OFSET)
#     screen.blit(main_menu.surface, (0, 0))
#     game_surface.fill("black") # cerna
#
#     global_settings.GAME_SURFACE_OFSET = screen_animation.pos
#     screen_animation.update()
#
#     player.update(food_manager.content)
#     main_menu.update()
#
#     food_manager.update()
#
#     #FPS - TODO: pridat do debug surface
#     score_surface = debug_font.render(f"FPS: {global_settings.REAL_GAME_FPS}", True, "White")
#     screen.blit(score_surface, (20 , 20))
#     score_surface = debug_font.render(f"Player battery: {player.battery}", True, "White")
#     screen.blit(score_surface, (20 , 45))
#     score_surface = debug_font.render(f"Player length: {player.length}", True, "White")
#     screen.blit(score_surface, (20 , 70))
#
#
#     test_particle_system.update()
#
#     pygame.display.flip()  # Refresh on-screen display
#     clock.tick(global_settings.SET_GAME_FPS)  
