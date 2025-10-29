import pygame
import random
import math
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Station Defender: Meteor Run")

# Load assets
station_img = pygame.image.load("assets/station.png").convert_alpha()
meteor_img = pygame.image.load("assets/meteor.png").convert_alpha()
bg_color = (10, 10, 30)

# Scale station
station_img = pygame.transform.scale(station_img, (180, 180))
station_rect = station_img.get_rect(center=(WIDTH // 2, HEIGHT - 100))

# Game variables
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 24)
score = 0
speed_factor = 1
game_over = False

# Meteor list
meteors = []

def spawn_meteor():
    x = random.randint(50, WIDTH - 50)
    size = random.randint(40, 100)
    y = -size
    speed = random.uniform(2, 5)
    meteors.append({"x": x, "y": y, "size": size, "speed": speed})

def draw_meteors():
    for m in meteors:
        meteor_scaled = pygame.transform.scale(meteor_img, (m["size"], m["size"]))
        screen.blit(meteor_scaled, (m["x"], m["y"]))

def move_meteors():
    global game_over
    for m in meteors:
        m["y"] += m["speed"] * speed_factor
        if m["y"] > HEIGHT:
            meteors.remove(m)
        else:
            # Collision check
            meteor_rect = pygame.Rect(m["x"], m["y"], m["size"], m["size"])
            if station_rect.colliderect(meteor_rect):
                game_over = True

def draw_text(text, pos, color=(255, 255, 255)):
    surface = font.render(text, True, color)
    screen.blit(surface, pos)

# Main loop
spawn_timer = 0
running = True
while running:
    dt = clock.tick(60) / 1000  # Delta time
    screen.fill(bg_color)

    # Input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and station_rect.left > 0:
        station_rect.x -= 400 * dt
    if keys[pygame.K_RIGHT] and station_rect.right < WIDTH:
        station_rect.x += 400 * dt

    # Spawn meteors
    spawn_timer += dt
    if spawn_timer > 0.7:
        spawn_meteor()
        spawn_timer = 0

    # Update meteors
    move_meteors()

    # Draw elements
    draw_meteors()
    screen.blit(station_img, station_rect)
    draw_text(f"Score: {int(score)}", (20, 20))

    # Score increase
    score += dt * 10
    speed_factor = 1 + score / 200

    # Game Over screen
    if game_over:
        draw_text("GAME OVER - Press R to Restart", (200, HEIGHT // 2), (255, 100, 100))
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            meteors.clear()
            score = 0
            game_over = False
            station_rect.centerx = WIDTH // 2
        continue

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
