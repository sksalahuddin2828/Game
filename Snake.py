import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Colors (modern vibrant palette)
BLACK = (18, 18, 18)
WHITE = (255, 255, 255)
GREEN = (0, 255, 100)
RED = (255, 60, 60)
DARK_GREEN = (0, 155, 80)
BLUE = (0, 180, 255)

# Game settings
CELL_SIZE = 20
assert SCREEN_WIDTH % CELL_SIZE == 0, "Screen width must be a multiple of cell size."
assert SCREEN_HEIGHT % CELL_SIZE == 0, "Screen height must be a multiple of cell size."
CELL_WIDTH = SCREEN_WIDTH // CELL_SIZE
CELL_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Fonts
FONT_SMALL = pygame.font.SysFont('Segoe UI', 18)
FONT_LARGE = pygame.font.SysFont('Segoe UI', 48, bold=True)

# Directions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

class Snake:
    def __init__(self):
        # Start centered and 3 blocks long moving right
        self.positions = [(CELL_WIDTH // 2, CELL_HEIGHT // 2),
                          (CELL_WIDTH // 2 -1, CELL_HEIGHT // 2),
                          (CELL_WIDTH // 2 -2, CELL_HEIGHT // 2)]
        self.direction = RIGHT
        self.grow = False

    def head_position(self):
        return self.positions[0]

    def move(self):
        x, y = self.head_position()
        if self.direction == UP:
            y -= 1
        elif self.direction == DOWN:
            y += 1
        elif self.direction == LEFT:
            x -= 1
        elif self.direction == RIGHT:
            x += 1

        new_head = (x, y)

        # Check if growing - if yes, don't remove tail
        if self.grow:
            self.positions = [new_head] + self.positions
            self.grow = False
        else:
            self.positions = [new_head] + self.positions[:-1]

    def change_direction(self, new_direction):
        opposites = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        # Prevent reversing direction directly
        if new_direction != opposites.get(self.direction):
            self.direction = new_direction

    def collide_self(self):
        return self.head_position() in self.positions[1:]

    def collide_wall(self):
        x, y = self.head_position()
        return x < 0 or x >= CELL_WIDTH or y < 0 or y >= CELL_HEIGHT

    def grow_snake(self):
        self.grow = True

    def draw(self, surface):
        for pos in self.positions:
            rect = pygame.Rect(pos[0]*CELL_SIZE, pos[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, GREEN, rect)
            pygame.draw.rect(surface, DARK_GREEN, rect, 3) # border

class Food:
    def __init__(self, snake_positions):
        self.position = (0, 0)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        while True:
            x = random.randint(0, CELL_WIDTH -1)
            y = random.randint(0, CELL_HEIGHT -1)
            if (x, y) not in snake_positions:
                self.position = (x, y)
                break

    def draw(self, surface):
        rect = pygame.Rect(self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, WHITE, rect, 2) # border highlight

def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, DARK_GREEN, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, DARK_GREEN, (0, y), (SCREEN_WIDTH, y))

def draw_score(surface, score):
    score_text = FONT_SMALL.render(f"Score: {score}", True, BLUE)
    surface.blit(score_text, (10, 10))

def game_over_screen(surface, score):
    surface.fill(BLACK)
    game_over_text = FONT_LARGE.render("Game Over", True, RED)
    score_text = FONT_SMALL.render(f"Final Score: {score}", True, WHITE)
    restart_text = FONT_SMALL.render("Press R to Restart or Q to Quit", True, WHITE)

    surface.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//3))
    surface.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//3 + 60))
    surface.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//3 + 100))
    pygame.display.flip()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Modern Snake Game')
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food(snake.positions)
    score = 0

    running = True
    game_over = False

    while running:
        clock.tick(10)  # 10 frames per second (speed of snake)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)
                elif event.key == pygame.K_r and game_over:
                    # Restart game
                    snake = Snake()
                    food = Food(snake.positions)
                    score = 0
                    game_over = False
                elif event.key == pygame.K_q and game_over:
                    running = False
                    return

        if not game_over:
            snake.move()

            # Check collisions
            if snake.collide_wall() or snake.collide_self():
                game_over = True

            # Check if snake eats food
            if snake.head_position() == food.position:
                snake.grow_snake()
                score += 1
                food.randomize_position(snake.positions)

            # Draw everything
            screen.fill(BLACK)
            draw_grid(screen)
            snake.draw(screen)
            food.draw(screen)
            draw_score(screen, score)
            pygame.display.flip()
        else:
            game_over_screen(screen, score)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Error:", e)
    finally:
        pygame.quit()
        sys.exit()
