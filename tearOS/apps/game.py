import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Awesome Game")

# Colors
black = (0, 0, 0)
white = (255, 255, 255)

# Player variables
player_x = 50
player_y = 50
player_size = 20
player_speed = 5

# Enemy variables
enemy_size = 20
enemy_x = random.randint(0, screen_width - enemy_size)
enemy_y = random.randint(0, screen_height - enemy_size)
enemy_speed = 3

# Score
score = 0
font = pygame.font.Font(None, 36)  # Choose a font

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Keep player within screen bounds
    if player_x < 0:
        player_x = 0
    elif player_x > screen_width - player_size:
        player_x = screen_width - player_size
    if player_y < 0:
        player_y = 0
    elif player_y > screen_height - player_size:
        player_y = screen_height - player_size

    # Enemy movement (random for now)
    enemy_x += random.randint(-enemy_speed, enemy_speed)
    enemy_y += random.randint(-enemy_speed, enemy_speed)

    # Collision detection
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)
    if player_rect.colliderect(enemy_rect):
        score += 1
        enemy_x = random.randint(0, screen_width - enemy_size)
        enemy_y = random.randint(0, screen_height - enemy_size)

    # Clear the screen
    screen.fill(black)

    # Draw the player
    pygame.draw.rect(screen, white, (player_x, player_y, player_size, player_size))

    # Draw the enemy
    pygame.draw.rect(screen, white, (enemy_x, enemy_y, enemy_size, enemy_size))

    # Display the score
    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, (10, 10))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
