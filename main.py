import pygame
import sys
import os
import random
from helper.aspect_scale import aspect_scale

# Initialize Pygame
pygame.init()

# Set up display
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
window_size = (WINDOW_WIDTH, WINDOW_HEIGHT)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Space Explorer")

# constants
HEALTH_DECREASE_RATE = 0.07
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Initial health value
health = 1.0

# Get the current script's directory
current_dir = os.path.dirname(os.path.realpath(__file__))

image_dir = current_dir + "/assets/images/"
sound_dir = current_dir + "/assets/sound/"

background_music = pygame.mixer.Sound(os.path.join(sound_dir, 'main.mp3'))
crash_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'crash.wav'))
ping_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'ping.wav'))

background_music.play(-1)
# Load background image
background = pygame.image.load(os.path.join(image_dir,  "galaxy.jpg"))
background = pygame.transform.scale(background, window_size)

# Load original player image facing right
player_left = pygame.image.load(os.path.join(image_dir, "player.png"))
player_left = aspect_scale(player_left, 230, 230)


print(player_left)
# Flip player image to face left
player_right = pygame.transform.flip(player_left, True, False)

# Load oxygen_tank image
oxygen_tank_image = pygame.image.load(os.path.join(image_dir, "oxygen_tank.png"))
oxygen_tank_image = aspect_scale(oxygen_tank_image, 60, 60)

# Initial position of player
player_rect = player_left.get_rect()
player_rect.center = window_size[0] // 2, window_size[1] // 2

# Create a smaller rect for collision detection
player_collision_rect = pygame.Rect(player_rect.x, player_rect.y, 155, 80)

# Set the speed of player
speed = 7

asteroid_speed= 10

# Initial direction
direction = "right"

# List to store treat positions
treat_positions = []

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)

points = 0

# Function to render text
def render_text(text, color, position):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

# Create sprite class for the player collision rectangle
class NyanCatCollisionRect(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect

# Create sprite for the player collision rectangle
player_collision_sprite = NyanCatCollisionRect(player_collision_rect)


# Function to spawn asteroid
def spawn_asteroid():
    side = random.choice(["top", "bottom", "left", "right"])
    if side == "top":
        x = random.randint(0, window_size[0] - asteroid_image.get_width())
        y = -asteroid_image.get_height()
        velocity = (random.uniform(-1, 1), random.uniform(0.7, 1))  # Random velocity downwards
    elif side == "bottom":
        x = random.randint(0, window_size[0] - asteroid_image.get_width())
        y = window_size[1]
        velocity = (random.uniform(-1, 1), random.uniform(-1, -0.7))  # Random velocity upwards
    elif side == "left":
        x = -asteroid_image.get_width()
        y = random.randint(0, window_size[1] - asteroid_image.get_height())
        velocity = (random.uniform(0.7, 1), random.uniform(-1, 1))  # Random velocity to the right
    elif side == "right":
        x = window_size[0]
        y = random.randint(0, window_size[1] - asteroid_image.get_height())
        velocity = (random.uniform(-1, -0.7), random.uniform(-1, 1))  # Random velocity to the left

    asteroid_rect = pygame.Rect(x, y, asteroid_image.get_width(), asteroid_image.get_height())
    asteroid_positions.append(asteroid_rect)
    asteroid_velocities.append(velocity)
    asteroid_timers.append(random.randint(200, 500))

# Load asteroid image
asteroid_image = pygame.image.load(os.path.join(image_dir, "asteroid.png"))
asteroid_image = aspect_scale(asteroid_image, 70, 70)

# List to store asteroid positions
asteroid_positions = []
asteroid_velocities =[]
asteroid_timers = []

# Create a sprite group for asteroids
asteroids_group = pygame.sprite.Group()

def start_screen():
    screen.blit(background, (0, 0))

    title_text = title_font.render("Space Explorer", True, WHITE)
    title_rect = title_text.get_rect(center=(window_size[0] // 2, window_size[1] // 4))
    screen.blit(title_text, title_rect)

    start_button = pygame.Rect(window_size[0] // 4, window_size[1] // 2, window_size[0] // 2, 50)
    pygame.draw.rect(screen, BLACK, start_button)
    start_text = font.render("Start Game", True, WHITE)
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)

    instructions_button = pygame.Rect(window_size[0] // 4, window_size[1] // 2 + 100, window_size[0] // 2, 50)
    pygame.draw.rect(screen, BLACK, instructions_button)
    instructions_text = font.render("Instructions", True, WHITE)
    instructions_text_rect = instructions_text.get_rect(center=instructions_button.center)
    screen.blit(instructions_text, instructions_text_rect)

    pygame.display.flip()

    return start_button, instructions_button

def game_over():
    screen.blit(background, (0,0))
    game_over_text = pygame.font.Font(None, 72).render("Game Over", True, RED)
    game_over_rect = game_over_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2))
    screen.blit(game_over_text, game_over_rect)

    # Display time survived
    minutes = total_elapsed_time // 60000
    seconds = (total_elapsed_time // 1000) % 60

    time_text = font.render(f"Time Survived: {minutes:02}:{seconds:02}", True, WHITE)
    time_rect = time_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 + 50))
    screen.blit(time_text, time_rect)

    pygame.display.flip()
    asteroid_positions.clear()
    asteroid_velocities.clear()
    asteroid_timers.clear()

    # Wait for a few seconds before going back to start screen
    pygame.time.delay(3000)

    return "start_screen"

# Function to display instructions
def display_instructions():
    screen.blit(background, (0, 0))

    title_text = title_font.render("Instructions", True, WHITE)
    title_rect = title_text.get_rect(center=(window_size[0] // 2, 50))
    screen.blit(title_text, title_rect)

    instruction_texts = [
        "1. Collect oxygen tanks to supplement your depleting oxygen",
        "2. Avoid asteroids",
        "3. Survive as long as possible",
    ]

    for i, instruction in enumerate(instruction_texts):
        text = font.render(instruction, True, WHITE)
        text_rect = text.get_rect(center=(window_size[0] // 2, 150 + i * 50))
        screen.blit(text, text_rect)

    back_button = pygame.Rect(window_size[0] // 4, window_size[1] - 100, window_size[0] // 2, 50)
    pygame.draw.rect(screen, (0, 255, 0), back_button)
    back_text = font.render("Back to Menu", True, WHITE)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)

    pygame.display.flip()

    return back_button

# Initial state
current_state = "start_screen"

# Main game loop
clock = pygame.time.Clock()
spawn_timer = 0
spawn_interval = 200
spawn_timer_asteroid = 0
spawn_interval_asteroid = 200
last_time=0
total_elapsed_time = 0

treat_timers = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == "start_screen":
                start_button, instructions_button = start_screen()
                if start_button.collidepoint(event.pos):
                    current_state = "playing"
                    start_time = pygame.time.get_ticks()
                elif instructions_button.collidepoint(event.pos):
                    current_state = "instructions"
            elif current_state == "instructions":
                back_button = display_instructions()
                if back_button.collidepoint(event.pos):
                    current_state = "start_screen"

    if current_state == "start_screen":
        start_screen()
    elif current_state == "instructions":
        display_instructions()
    elif current_state == "playing":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= speed
            direction = "left"
            # Ensure player stays within the left boundary
            player_rect.x = max(player_rect.x, 0)
        elif keys[pygame.K_RIGHT]:
            player_rect.x += speed
            direction = "right"
            # Ensure player stays within the right boundary
            player_rect.x = min(player_rect.x, window_size[0] - player_collision_rect.width)
        elif keys[pygame.K_UP]:
            player_rect.y -= speed
            # Ensure player stays within the top boundary
            player_rect.y = max(player_rect.y, 0)
        elif keys[pygame.K_DOWN]:
            player_rect.y += speed
            # Ensure player stays within the bottom boundary
            player_rect.y = min(player_rect.y, window_size[1] - player_rect.height)

        # Update the smaller collision rect's position
        player_collision_rect.topleft = (player_rect.x + 40, player_rect.y + 20)

        # Randomly spawn oxygen_tank
        spawn_timer += clock.get_rawtime()
        if spawn_timer >= spawn_interval:
            spawn_timer = 0
            treat_x = random.randint(0, window_size[0] - oxygen_tank_image.get_width())
            treat_y = random.randint(0, window_size[1] - oxygen_tank_image.get_height())
            treat_rect = pygame.Rect(treat_x, treat_y, oxygen_tank_image.get_width(), oxygen_tank_image.get_height())

            # Check if player is not at the treat location and there are no other oxygen_tank there
            if (
                not player_rect.colliderect(treat_rect)
                and not any(treat_rect.colliderect(existing_treat) for existing_treat in treat_positions)
            ):
                treat_positions.append(treat_rect)
                treat_timers.append(random.randint(700, 1000))

        # Draw background and player
        screen.blit(background, (0, 0))

        # Draw oxygen_tank and update timers
        for i in range(len(treat_positions)):
            screen.blit(oxygen_tank_image, treat_positions[i])
            treat_timers[i] -= clock.get_rawtime()
            if player_collision_rect.colliderect(treat_positions[i]):
                # Increment points and remove oxygen_tank
                ping_sound.play()
                health += 0.1
                treat_positions.pop(i)
                treat_timers.pop(i)
                break
            if treat_timers[i] <= 0:
                # Remove oxygen_tank and its timer when the time is up
                treat_positions.pop(i)
                treat_timers.pop(i)
                break

        current_time = pygame.time.get_ticks() - start_time
        elapsed_time = current_time - last_time
        last_time = current_time
        total_elapsed_time += elapsed_time

        # Spawn asteroid
        spawn_timer_asteroid += clock.get_rawtime()
        if spawn_timer_asteroid >= spawn_interval_asteroid and current_time > 2000:
            spawn_timer_asteroid = 0
            spawn_asteroid()

        # Move asteroids and update timers
        for i in range(len(asteroid_positions)):
            asteroid_positions[i].x += asteroid_speed * asteroid_velocities[i][0]
            asteroid_positions[i].y += asteroid_speed * asteroid_velocities[i][1]
            screen.blit(asteroid_image, asteroid_positions[i])
            asteroid_timers[i] -= clock.get_rawtime()
            if asteroid_timers[i] <= 0 and (asteroid_positions[i].x > WINDOW_WIDTH or asteroid_positions[i].x <0) or (asteroid_positions[i].y < 0 or asteroid_positions[i].y > WINDOW_HEIGHT) :
                # Remove asteroid, its timer, and velocity when the time is up
                asteroid_positions.pop(i)
                asteroid_velocities.pop(i)
                asteroid_timers.pop(i)
                break

        # Update sprite group with asteroid positions
        asteroids_group.empty()
        for asteroid_rect in asteroid_positions:
            asteroid_sprite = pygame.sprite.Sprite()
            asteroid_sprite.rect = asteroid_rect
            asteroids_group.add(asteroid_sprite)


        # Draw player
        if direction == "right":
            player = player_right
        else:
            player = player_left

        screen.blit(player, player_rect)

        health -= HEALTH_DECREASE_RATE * (elapsed_time / 1000.0)

        # Cap the health value
        if health > 1:
            health = 1

        # Check for collision with asteroids
        if pygame.sprite.spritecollide(player_collision_sprite, asteroids_group, False):
            crash_sound.play()
            current_state = game_over()

        if health <= 0:
            current_state = game_over()

        # Draw health bar background
        pygame.draw.rect(screen, WHITE, (10, 10, 200, 30))

        # Draw health bar fill
        pygame.draw.rect(screen, RED, (10, 10, 200 * health, 30))

        # Draw health percentage
        text = font.render(f"{int(health * 100)}%", True, WHITE)

        screen.blit(text, (220, 15))

        # Update display
        pygame.display.flip()

        # Set the frame rate
        clock.tick(60)
