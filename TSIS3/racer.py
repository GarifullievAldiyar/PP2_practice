import pygame
import random

WIDTH, HEIGHT = 400, 600
LANES = [100, 200, 300]

class Player:
    def __init__(self):
        self.lane = 1
        self.y = 500
        self.speed = 5
        self.base_speed = 5
        self.shield = False
        self.nitro_timer = 0
        self.alive = True

    def move(self, direction):
        self.lane = max(0, min(2, self.lane + direction))

    def update(self):
        if self.nitro_timer > 0:
            self.nitro_timer -= 1
        else:
            self.speed = self.base_speed

    def rect(self):
        return pygame.Rect(LANES[self.lane] - 20, self.y, 40, 60)


class Enemy:
    def __init__(self, lane, speed):
        self.lane = lane
        self.y = -60
        self.speed = speed

    def update(self):
        self.y += self.speed

    def rect(self):
        return pygame.Rect(LANES[self.lane] - 20, self.y, 40, 60)


class Obstacle:
    def __init__(self, lane, type):
        self.lane = lane
        self.y = -40
        self.type = type

    def update(self):
        self.y += 5

    def rect(self):
        return pygame.Rect(LANES[self.lane] - 20, self.y, 40, 40)


class PowerUp:
    def __init__(self, lane, type):
        self.lane = lane
        self.y = -40
        self.type = type

    def update(self):
        self.y += 5

    def rect(self):
        return pygame.Rect(LANES[self.lane] - 15, self.y, 30, 30)


def run_game(screen, settings):
    clock = pygame.time.Clock()
    player = Player()

    enemies = []
    obstacles = []
    powerups = []

    distance = 0
    score = 0

    spawn_timer = 0

    running = True
    while running:
        screen.fill((30, 30, 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", 0, 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-1)
                if event.key == pygame.K_RIGHT:
                    player.move(1)

        
        difficulty_scale = 1 + distance / 2000

        
        spawn_timer += 1
        if spawn_timer > 40 / difficulty_scale:
            spawn_timer = 0

            lane = random.randint(0, 2)

            if lane != player.lane:
                enemies.append(Enemy(lane, 5 + difficulty_scale))

            if random.random() < 0.3:
                obstacles.append(Obstacle(random.randint(0, 2), "barrier"))

            if random.random() < 0.2:
                powerups.append(PowerUp(random.randint(0, 2),
                                        random.choice(["nitro", "shield", "repair"])))

        
        player.update()

        for e in enemies:
            e.update()
        for o in obstacles:
            o.update()
        for p in powerups:
            p.update()

        
        for e in enemies:
            if player.rect().colliderect(e.rect()):
                if player.shield:
                    player.shield = False
                    enemies.remove(e)
                else:
                    player.alive = False

        for p in powerups:
            if player.rect().colliderect(p.rect()):
                if p.type == "nitro":
                    player.nitro_timer = 180
                    player.speed = 10
                elif p.type == "shield":
                    player.shield = True
                elif p.type == "repair":
                    player.alive = True
                powerups.remove(p)

        
        enemies = [e for e in enemies if e.y < HEIGHT]
        obstacles = [o for o in obstacles if o.y < HEIGHT]
        powerups = [p for p in powerups if p.y < HEIGHT]

        
        pygame.draw.rect(screen, (0, 255, 0), player.rect())

        for e in enemies:
            pygame.draw.rect(screen, (255, 0, 0), e.rect())

        for o in obstacles:
            pygame.draw.rect(screen, (200, 200, 0), o.rect())

        for p in powerups:
            pygame.draw.rect(screen, (0, 0, 255), p.rect())

        
        distance += player.speed
        score = int(distance)

        font = pygame.font.SysFont(None, 30)
        screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))

        pygame.display.flip()
        clock.tick(60)

        if not player.alive:
            return "game_over", score, distance