import pygame
from racer import run_game
import ui
import persistence

pygame.init()
screen = pygame.display.set_mode((400,600))

settings = persistence.load_settings()

state = "menu"
player_name = "Player"

while True:

    if state == "menu":
        state = ui.menu(screen)

    elif state == "game":
        state, score, distance = run_game(screen, settings)

        if state == "game_over":
            persistence.add_score(player_name, score, distance)

    elif state == "game_over":
        state = ui.game_over(screen, score, distance)

    elif state == "leaderboard":
        data = persistence.load_leaderboard()
        state = ui.leaderboard(screen, data)

    elif state == "settings":
        
        settings["sound"] = not settings["sound"]
        persistence.save_settings(settings)
        state = "menu"

    elif state == "quit":
        break

pygame.quit()