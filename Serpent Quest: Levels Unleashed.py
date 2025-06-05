import pygame
import random
import sys

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
YELLOW = (255, 215, 0)
GRAY = (80, 80, 80)

# Game settings
CELL_SIZE = 20
assert SCREEN_WIDTH % CELL_SIZE == 0, "Screen width must be a multiple of cell size."
assert SCREEN_HEIGHT % CELL_SIZE == 0, "Screen height must be a multiple of cell size."
CELL_WIDTH = SCREEN_WIDTH // CELL_SIZE
CELL_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

# Fonts
FONT_SMALL = pygame.font.SysFont('Segoe UI', 18)
FONT_MEDIUM = pygame.font.SysFont('Segoe UI', 28, bold=True)
FONT_LARGE = pygame.font.SysFont('Segoe UI', 48, bold=True)

# Directions
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# Difficulty settings
DIFFICULTY_SETTINGS = {
    'easy': {'speed': 8, 'obstacle_count': 3, 'score_per_level': 5},
    'medium': {'speed': 12, 'obstacle_count': 6, 'score_per_level': 7},
    'hard': {'speed': 18, 'obstacle_count': 10, 'score_per_level': 10},
}

LEVELS_TOTAL = 100

class Snake:
    def __init__(self):
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

        if self.grow:
            self.positions = [new_head] + self.positions
            self.grow = False
        else:
            self.positions = [new_head] + self.positions[:-1]

    def change_direction(self, new_direction):
        opposites = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
        if new_direction != opposites.get(self.direction, ''):
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
            pygame.draw.rect(surface, DARK_GREEN, rect, 3)

class Food:
    def __init__(self, snake_positions, obstacle_positions):
        self.position = (0, 0)
        self.randomize_position(snake_positions, obstacle_positions)

    def randomize_position(self, snake_positions, obstacle_positions):
        while True:
            x = random.randint(0, CELL_WIDTH -1)
            y = random.randint(0, CELL_HEIGHT -1)
            if (x, y) not in snake_positions and (x, y) not in obstacle_positions:
                self.position = (x, y)
                break

    def draw(self, surface):
        rect = pygame.Rect(self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, YELLOW, rect, 3)

class Obstacle:
    def __init__(self, positions):
        self.position = self.place_position(positions)

    def place_position(self, taken_positions):
        while True:
            x = random.randint(0, CELL_WIDTH -1)
            y = random.randint(0, CELL_HEIGHT -1)
            if (x, y) not in taken_positions:
                return (x, y)

    def draw(self, surface):
        rect = pygame.Rect(self.position[0]*CELL_SIZE, self.position[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, GRAY, rect)
        pygame.draw.rect(surface, BLACK, rect, 2)

def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, DARK_GREEN, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, DARK_GREEN, (0, y), (SCREEN_WIDTH, y))

def draw_score(surface, score):
    score_text = FONT_SMALL.render(f"Score: {score}", True, BLUE)
    surface.blit(score_text, (10, 10))

def draw_level(surface, level):
    level_text = FONT_SMALL.render(f"Level: {level}", True, BLUE)
    surface.blit(level_text, (SCREEN_WIDTH - level_text.get_width() - 10, 10))

def draw_difficulty(surface, difficulty):
    diff_text = FONT_SMALL.render(f"Difficulty: {difficulty.capitalize()}", True, BLUE)
    surface.blit(diff_text, (SCREEN_WIDTH//2 - diff_text.get_width()//2, 10))

def game_over_screen(surface, score, level):
    surface.fill(BLACK)
    game_over_text = FONT_LARGE.render("Game Over", True, RED)
    score_text = FONT_MEDIUM.render(f"Final Score: {score}", True, WHITE)
    level_text = FONT_SMALL.render(f"You reached Level: {level}", True, WHITE)
    restart_text = FONT_SMALL.render("Press R to Restart or Q to Quit", True, WHITE)

    surface.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//3))
    surface.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//3 + 60))
    surface.blit(level_text, (SCREEN_WIDTH//2 - level_text.get_width()//2, SCREEN_HEIGHT//3 + 100))
    surface.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//3 + 140))
    pygame.display.flip()

def generate_obstacles(count, snake_positions, food_position):
    obstacles = []
    taken_positions = set(snake_positions)
    taken_positions.add(food_position)
    while len(obstacles) < count:
        obs = Obstacle(taken_positions)
        obstacles.append(obs)
        taken_positions.add(obs.position)
    return obstacles

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Modern Creative Snake")
    clock = pygame.time.Clock()

    # Initial difficulty choice
    difficulty = choose_difficulty(screen, clock)
    settings = DIFFICULTY_SETTINGS[difficulty]

    snake = Snake()
    food = Food(snake.positions, set())
    obstacles = generate_obstacles(settings['obstacle_count'], snake.positions, food.position)
    score = 0
    level = 1

    running = True
    game_over = False

    while running:
        clock.tick(settings['speed'])

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

                if game_over:
                    if event.key == pygame.K_r:
                        # Restart game but keep difficulty
                        snake = Snake()
                        food = Food(snake.positions, set())
                        obstacles = generate_obstacles(settings['obstacle_count'], snake.positions, food.position)
                        score = 0
                        level = 1
                        game_over = False
                    elif event.key == pygame.K_q:
                        running = False
                        return

        if not game_over:
            snake.move()

            # Check collisions
            if snake.collide_wall() or snake.collide_self() or any(snake.head_position() == obs.position for obs in obstacles):
                game_over = True

            # Eating food
            if snake.head_position() == food.position:
                snake.grow_snake()
                score += 1
                # Level up logic
                if score % settings['score_per_level'] == 0:
                    level += 1
                    # Increase speed for levels greater than 1 up to max speed
                    if level <= LEVELS_TOTAL:
                        # Gradually increase speed every few levels, capped by hard difficulty max speed
                        increment_speed = 0.2
                        new_speed = min(settings['speed'] + increment_speed * (level - 1), DIFFICULTY_SETTINGS['hard']['speed'])
                        settings['speed'] = new_speed

                        # Increase number of obstacles every 10 levels, capped by hard difficulty max obstacles
                        if level % 10 == 0:
                            new_obstacle_count = min(settings['obstacle_count'] + (level // 10), DIFFICULTY_SETTINGS['hard']['obstacle_count'])
                            settings['obstacle_count'] = new_obstacle_count

                    # Generate new obstacles for new level
                    obstacles = generate_obstacles(settings['obstacle_count'], snake.positions, food.position)

                # Reposition food
                food.randomize_position(snake.positions, set(obs.position for obs in obstacles))

            # Draw everything
            screen.fill(BLACK)
            draw_grid(screen)
            for obs in obstacles:
                obs.draw(screen)
            snake.draw(screen)
            food.draw(screen)
            draw_score(screen, score)
            draw_level(screen, level)
            draw_difficulty(screen, difficulty)
            pygame.display.flip()

        else:
            game_over_screen(screen, score, level)

def choose_difficulty(screen, clock):
    # Simple menu to select difficulty
    selected = 0
    options = ['easy', 'medium', 'hard']
    while True:
        screen.fill(BLACK)

        title = FONT_LARGE.render("Select Difficulty", True, BLUE)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

        for i, option in enumerate(options):
            color = YELLOW if i == selected else WHITE
            text = FONT_MEDIUM.render(option.capitalize(), True, color)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 150 + i*50))

        instruction = FONT_SMALL.render("Use Up/Down keys to select, Enter to confirm", True, WHITE)
        screen.blit(instruction, (SCREEN_WIDTH//2 - instruction.get_width()//2, SCREEN_HEIGHT - 70))

        pygame.display.flip()
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected -1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected +1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    return options[selected]

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("Error:", e)
    finally:
        pygame.quit()
        sys.exit()

