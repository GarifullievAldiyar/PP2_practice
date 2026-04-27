import pygame

def draw_text(screen, text, y):
    font = pygame.font.SysFont(None, 40)
    render = font.render(text, True, (255,255,255))
    rect = render.get_rect(center=(200, y))
    screen.blit(render, rect)

def menu(screen):
    while True:
        screen.fill((0,0,0))
        draw_text(screen, "RACER", 150)
        draw_text(screen, "ENTER - PLAY", 250)
        draw_text(screen, "L - LEADERBOARD", 300)
        draw_text(screen, "S - SETTINGS", 350)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "game"
                if event.key == pygame.K_l:
                    return "leaderboard"
                if event.key == pygame.K_s:
                    return "settings"

def game_over(screen, score, distance):
    while True:
        screen.fill((0,0,0))
        draw_text(screen, f"Score: {score}", 250)
        draw_text(screen, "R - Retry", 320)
        draw_text(screen, "M - Menu", 360)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "game"
                if event.key == pygame.K_m:
                    return "menu"

def leaderboard(screen, data):
    while True:
        screen.fill((0,0,0))

        y = 100
        for i, entry in enumerate(data):
            draw_text(screen, f"{i+1}. {entry['name']} - {entry['score']}", y)
            y += 40

        draw_text(screen, "ESC - BACK", 500)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"