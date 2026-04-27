import pygame
from game import run_game
from db import *
from config import load_settings, save_settings

pygame.init()

screen = pygame.display.set_mode((600, 600))
font = pygame.font.Font(None, 36)

state = "MENU"
username = ""
player_id = None

settings = load_settings()


def draw_menu():
    screen.fill((0,0,0))
    text = font.render("Enter username: " + username, True, (255,255,255))
    screen.blit(text, (100, 200))
    pygame.display.update()


def draw_game_over(score, level):
    screen.fill((0,0,0))
    best = get_best(player_id)

    t1 = font.render(f"Score: {score}", True, (255,255,255))
    t2 = font.render(f"Level: {level}", True, (255,255,255))
    t3 = font.render(f"Best: {best}", True, (255,255,0))

    screen.blit(t1, (200, 200))
    screen.blit(t2, (200, 240))
    screen.blit(t3, (200, 280))

    pygame.display.update()


def leaderboard():
    screen.fill((0,0,0))
    data = get_top10()

    y = 100
    for i, row in enumerate(data):
        text = font.render(f"{i+1}. {row[0]} {row[1]}", True, (255,255,255))
        screen.blit(text, (100, y))
        y += 40

    pygame.display.update()


running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == "MENU":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    player_id = get_or_create_player(username)
                    state = "GAME"
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

    if state == "MENU":
        draw_menu()

    elif state == "GAME":
        run_game()
        save_game(player_id, 10, 3) 
        state = "GAME_OVER"

    elif state == "GAME_OVER":
        draw_game_over(10, 3)

    elif state == "LEADERBOARD":
        leaderboard()