import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen setup
CELL_SIZE = 20
WIDTH = 600
HEIGHT = 400
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game by N.Akshith (Roll No: 249P1A0590)")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 150, 255)
GRAY = (100, 100, 100)

# Fonts and clock
font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 42, bold=True)
clock = pygame.time.Clock()

def draw_text_center(text, color, y_offset=0, size="big"):
    f = big_font if size == "big" else font
    label = f.render(text, True, color)
    rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2 + y_offset))
    screen.blit(label, rect)

def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def spawn_food(snake):
    """Ensure food spawns on valid grid not overlapping the snake."""
    while True:
        fx = random.randint(0, COLS - 1) * CELL_SIZE
        fy = random.randint(0, ROWS - 1) * CELL_SIZE
        if [fx, fy] not in snake:
            return [fx, fy]

def draw_snake(snake):
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], CELL_SIZE, CELL_SIZE))

def get_player_name():
    """Ask player to enter their name before game starts."""
    name = ""
    active = True
    while active:
        screen.fill(BLACK)
        draw_text_center("Enter Your Name", YELLOW, -40)
        draw_text_center("Press ENTER to Start", BLUE, 70)
        draw_text_center(name or "_", WHITE, 10, size="small")
        draw_text("Created by: N.Akshith (Roll No: 249P1A0590)", 10, HEIGHT - 30, GRAY)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isalnum() or event.unicode.isspace():
                    if len(name) < 15:
                        name += event.unicode

def run_game(level=1, player_name="Player"):
    snake = [[100, 100], [80, 100], [60, 100]]
    direction = "RIGHT"
    food = spawn_food(snake)
    score = 0
    speed = 10 + level * 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        head = list(snake[0])
        if direction == "UP":
            head[1] -= CELL_SIZE
        elif direction == "DOWN":
            head[1] += CELL_SIZE
        elif direction == "LEFT":
            head[0] -= CELL_SIZE
        elif direction == "RIGHT":
            head[0] += CELL_SIZE
        snake.insert(0, head)

        # Eating
        if head == food:
            score += 1
            food = spawn_food(snake)
        else:
            snake.pop()

        # Collisions
        if (head[0] < 0 or head[0] >= WIDTH or
            head[1] < 0 or head[1] >= HEIGHT or
            head in snake[1:]):
            return "game_over", level, score

        # Level complete
        if score >= 10:
            return "level_complete", level, score

        # Draw
        screen.fill(BLACK)
        draw_snake(snake)
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))
        draw_text(f"Player: {player_name}", 10, 10, YELLOW)
        draw_text(f"Score: {score}  Level: {level}", 10, 40, WHITE)
        draw_text("Created by: N.Akshith (Roll No: 249P1A0590)", 10, HEIGHT - 30, GRAY)
        pygame.display.flip()
        clock.tick(speed)

def show_message(title, subtitle, prompt, player_name):
    while True:
        screen.fill(BLACK)
        draw_text_center(title, YELLOW, -40)
        draw_text_center(subtitle, WHITE, 10)
        draw_text_center(prompt, BLUE, 60)
        draw_text("Press ESC to Quit", 10, HEIGHT - 30, WHITE)
        draw_text(f"Created by: N.Akshith (Roll No: 249P1A0590)", 10, HEIGHT - 60, GRAY)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def main():
    state = "name_input"
    level = 1
    score = 0
    player_name = "Player"

    while True:
        if state == "name_input":
            player_name = get_player_name()
            state = "welcome"

        elif state == "welcome":
            if show_message(f"Welcome {player_name}!", "Get ready to play!", "Press SPACE to Start", player_name):
                state = "playing"

        elif state == "playing":
            result, level, score = run_game(level, player_name)
            state = result

        elif state == "game_over":
            if show_message("Game Over!", f"Score: {score}", "Press SPACE to Restart", player_name):
                level = 1
                score = 0
                state = "welcome"

        elif state == "level_complete":
            if level < 10:
                if show_message(f"Level {level} Complete!", f"Score: {score}", "Press SPACE for Next Level", player_name):
                    level += 1
                    state = "playing"
            else:
                if show_message("🎉 All Levels Complete!", f"Final Score: {score}", "Press SPACE to Play Again", player_name):
                    level = 1
                    score = 0
                    state = "welcome"

if __name__ == "__main__":
    main()
