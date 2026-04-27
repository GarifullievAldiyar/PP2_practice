import pygame
import random

pygame.init()

WIDTH, HEIGHT = 600, 600
CELL = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


running = True


def spawn_food():
    return (random.randint(0, 29), random.randint(0, 29))

def spawn_poison():
    return (random.randint(0, 29), random.randint(0, 29))

def spawn_obstacles(level, snake):
    obs = []
    if level >= 3:
        for _ in range(level + 2):
            while True:
                pos = (random.randint(0, 29), random.randint(0, 29))
                if pos not in snake:
                    obs.append(pos)
                    break
    return obs



def draw_game(snake, food, poison, obstacles):
    screen.fill((0, 0, 0))

    
    for s in snake:
        pygame.draw.rect(screen, (0, 255, 0),
                         (s[0]*CELL, s[1]*CELL, CELL, CELL))

    
    pygame.draw.rect(screen, (255, 255, 0),
                     (food[0]*CELL, food[1]*CELL, CELL, CELL))

    
    pygame.draw.rect(screen, (139, 0, 0),
                     (poison[0]*CELL, poison[1]*CELL, CELL, CELL))

    
    for o in obstacles:
        pygame.draw.rect(screen, (100, 100, 100),
                         (o[0]*CELL, o[1]*CELL, CELL, CELL))

    pygame.display.update()



def run_game():
    global running

    snake = [(5, 5)]
    direction = (1, 0)

    score = 0
    level = 1
    speed = 8

    food = spawn_food()
    poison = spawn_poison()
    obstacles = spawn_obstacles(level, snake)

    while running:
        clock.tick(speed)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN:
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT:
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT:
                    direction = (1, 0)

        
        head = snake[0]
        new_head = (head[0] + direction[0], head[1] + direction[1])
        snake.insert(0, new_head)

        
        if new_head[0] < 0 or new_head[1] < 0 or new_head[0] > 29 or new_head[1] > 29:
            return

        if new_head in snake[1:]:
            return

        if new_head in obstacles:
            return

        
        if new_head == food:
            score += 1
            food = spawn_food()
        else:
            snake.pop()

        
        if new_head == poison:
            snake = snake[:-2]
            poison = spawn_poison()
            if len(snake) <= 1:
                return

        
        if score > 0 and score % 5 == 0:
            level += 1
            speed += 1
            obstacles = spawn_obstacles(level, snake)

       
        draw_game(snake, food, poison, obstacles)