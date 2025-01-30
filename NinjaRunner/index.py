import pygame
import random

pygame.init()

clock = pygame.time.Clock()
FPS = 60

# Create game window
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 128

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ninja Runner Parallax")

# Load images
background = pygame.image.load("background.bmp").convert_alpha()  # Home screen background
background2 = pygame.image.load("background2.bmp").convert_alpha()  # Far background
cloud = pygame.image.load("cloud.bmp").convert_alpha()             # Medium background
roof = pygame.image.load("roof.bmp").convert_alpha()               # Closest background
home_ninja_sprite_sheet = pygame.image.load("ninjast.bmp").convert_alpha()  # Ninja sprite sheet for the game
ninja_sprite_sheet = pygame.image.load("run.bmp").convert_alpha()  # Home ninja sprite sheet
obstacle_img = pygame.image.load("obstacle.bmp").convert_alpha()   # Obstacle image

# Get image dimensions
bg_width = background2.get_width()
ninja_width = ninja_sprite_sheet.get_width()
ninja_height = ninja_sprite_sheet.get_height() // 2  # Height per frame (sprite sheet has 2 rows)
obstacle_width = obstacle_img.get_width()
obstacle_height = obstacle_img.get_height()

# Resize obstacle to fit with ninja at the bottom (optional: scale to 75%)
obstacle_img = pygame.transform.scale(obstacle_img, (int(obstacle_width * 0.75), int(obstacle_height * 0.75)))

# Create animation frames for game ninja
frame_width = ninja_sprite_sheet.get_width()
frame_height = ninja_sprite_sheet.get_height() // 2  # Divide by 2 because there are 2 frames vertically
ninja_frames = []
for i in range(2):
    frame = ninja_sprite_sheet.subsurface(pygame.Rect(0, i * frame_height, frame_width, frame_height))
    ninja_frames.append(frame)

# Create animation frames for home ninja
home_frame_width = home_ninja_sprite_sheet.get_width()
home_frame_height = home_ninja_sprite_sheet.get_height() // 2  # 1 column, 2 rows
home_ninja_frames = []
for i in range(2):
    frame = home_ninja_sprite_sheet.subsurface(pygame.Rect(0, i * home_frame_height, home_frame_width, home_frame_height))
    home_ninja_frames.append(frame)

# Animation variables for game ninja
current_frame = 0
frame_time = 300  # Adjust the time between frames (in milliseconds)
last_frame_time = pygame.time.get_ticks()

# Animation variables for home ninja
home_current_frame = 0
home_frame_time = 300  # Adjust the time between frames (in milliseconds)
home_last_frame_time = pygame.time.get_ticks()

# Game variables
scroll = 0
ninja_x = 5  # 5 pixels from the left
ninja_y = SCREEN_HEIGHT - ninja_height  # Position ninja at the bottom

# Jump variables
is_jumping = False
jump_height = 5
gravity = 0.2
jump_velocity = jump_height

# Parallax speeds
bg_speed = 1
cloud_speed = 0.5
roof_speed = 2

# Background positions for infinite scroll
bg2_x = 0
cloud_x = 0
roof_x = 0

# Obstacle variables
obstacle_x = SCREEN_WIDTH  # Start position off-screen to the right
obstacle_y = 105  # Position obstacle at the bottom

# Set the speed of the obstacle
obstacle_speed = 2

# Game states
in_game = False  # To track if the game has started
game_over = False  # To track if the game is over

# Score variable
score = 0

# Function to draw the home screen
def draw_home_screen():
    global home_current_frame, home_last_frame_time

    screen.blit(background, (0, 0))  # Use background.bmp

    # Update the home ninja frame based on time
    if pygame.time.get_ticks() - home_last_frame_time > home_frame_time:
        home_current_frame = (home_current_frame + 1) % len(home_ninja_frames)
        home_last_frame_time = pygame.time.get_ticks()

    # Draw the animated home ninja
    ninja_center_x = (SCREEN_WIDTH - home_frame_width) // 2
    ninja_center_y = (SCREEN_HEIGHT - home_frame_height) // 2
    screen.blit(home_ninja_frames[home_current_frame], (ninja_center_x, ninja_center_y))

    # Draw instructions
    font = pygame.font.Font(None, 18)  # Smaller font size
    instruction_text = font.render("Press Enter to Start", True, (0, 0, 0))
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))  # Center the text
    screen.blit(instruction_text, instruction_rect)
    pygame.display.update()

# Function to draw the game over screen
def draw_game_over():
    screen.fill((0, 0, 0))  # Black background
    font = pygame.font.Font(None, 15)  # Smaller font size
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    restart_text = font.render("Press Enter to Restart", True, (255, 255, 255))
    home_text = font.render("Press A to Go Home", True, (255, 255, 255))

    # Center the text
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    home_rect = home_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(home_text, home_rect)
    pygame.display.update()

# Function to check collision between ninja and obstacle
def check_collision():
    global ninja_x, ninja_y, obstacle_x, obstacle_y, obstacle_width, obstacle_height, game_over
    if ninja_x + ninja_width > obstacle_x and ninja_x < obstacle_x + obstacle_width:
        if ninja_y + ninja_height > obstacle_y:
            game_over = True  # If there is a collision, end the game

# Function to draw the score
def draw_score():
    global score
    font = pygame.font.Font(None, 18)  # Smaller font size
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))

def draw_bg():
    global bg2_x, cloud_x, roof_x

    # Move the background layers based on the scroll
    bg2_x -= bg_speed
    cloud_x -= cloud_speed
    roof_x -= roof_speed

    # Draw the far background
    screen.blit(background2, (bg2_x, 0))
    screen.blit(background2, (bg2_x + bg_width, 0))

    # Draw the medium background (cloud)
    screen.blit(cloud, (cloud_x, 0))
    screen.blit(cloud, (cloud_x + bg_width, 0))

    # Draw the closest background (roof)
    screen.blit(roof, (roof_x, 0))
    screen.blit(roof, (roof_x + bg_width, 0))

    # Reset the positions to create the infinite loop effect
    if bg2_x <= -bg_width:
        bg2_x = 0
    if cloud_x <= -bg_width:
        cloud_x = 0
    if roof_x <= -bg_width:
        roof_x = 0

def draw_ninja():
    global current_frame, last_frame_time

    # Update the frame based on time
    if pygame.time.get_ticks() - last_frame_time > frame_time:
        current_frame = (current_frame + 1) % len(ninja_frames)  # Cycle through frames
        last_frame_time = pygame.time.get_ticks()

    # Draw the current frame
    screen.blit(ninja_frames[current_frame], (ninja_x, ninja_y))

def jump():
    global ninja_y, is_jumping, jump_velocity

    # Jumping mechanics
    if is_jumping:
        ninja_y -= jump_velocity  # Move the ninja up
        jump_velocity -= gravity  # Simulate gravity pulling the ninja down

        # End jump when it reaches the ground
        if ninja_y >= SCREEN_HEIGHT - ninja_height:
            ninja_y = SCREEN_HEIGHT - ninja_height
            is_jumping = False
            jump_velocity = jump_height  # Reset jump height

def draw_obstacle():
    global obstacle_x, obstacle_y
    screen.blit(obstacle_img, (obstacle_x, obstacle_y))  # Draw the obstacle using the image

def move_obstacle():
    global obstacle_x, obstacle_y, score

    # Move the obstacle towards the ninja (left to right)
    obstacle_x -= obstacle_speed

    # Check if the ninja has jumped over the obstacle
    if obstacle_x + obstacle_width < 0:
        score += 1  # Increase score when the obstacle is passed

    # Reset obstacle when it goes off the left side of the screen
    if obstacle_x < -obstacle_width:
        obstacle_x = SCREEN_WIDTH

# Game loop
run = True
while run:
    clock.tick(FPS)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Start game if not in-game and enter is pressed
    if not in_game and not game_over:
        draw_home_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            in_game = True  # Start the game

    # If game over, show game over screen
    elif game_over:
        draw_game_over()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            # Restart the game
            ninja_y = SCREEN_HEIGHT - ninja_height
            is_jumping = False
            jump_velocity = jump_height
            obstacle_x = SCREEN_WIDTH
            score = 0  # Reset score on restart
            game_over = False
            in_game = True
        if keys[pygame.K_a]:
            # Go back to the home screen
            in_game = False
            game_over = False

    # If game is running, play the game
    elif in_game:
        # Handle jump key press
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not is_jumping:
            is_jumping = True  # Start the jump

        # Draw world
        draw_bg()

        # Move obstacle and draw it
        move_obstacle()
        draw_obstacle()

        # Jump the ninja
        jump()

        # Draw the ninja
        draw_ninja()

        # Draw the score
        draw_score()

        # Check for collision
        check_collision()

    pygame.display.update()

pygame.quit()
