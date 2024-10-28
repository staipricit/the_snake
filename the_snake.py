"""
Основной модуль игры со змеёй, включает настройки экрана,
сетки и направления.
"""

from random import choice, randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
    0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Игровой объект с позицией и цветом."""

    def __init__(self, position=(0, 0), body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Рисует объект на поверхности."""


class Apple(GameObject):
    """Объект яблока для игры."""

    def __init__(self):
        position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )
        super().__init__(position, APPLE_COLOR)

    def randomize_position(self):
        """Случайно меняет позицию яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self, surface):
        """Рисует яблоко на экране с границей."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Объект змеи в игре."""

    def __init__(self):
        super().__init__((GRID_SIZE * 5, GRID_SIZE * 5), SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def move(self):
        """Перемещает змею в текущем направлении и обновляет её длину."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None
        self.last = self.positions[-1]
        x, y = self.direction
        self.positions.insert(
            0,
            (
                (self.positions[0][0] + (x * GRID_SIZE)) % SCREEN_WIDTH,
                (self.positions[0][1] + (y * GRID_SIZE)) % SCREEN_HEIGHT,
            ),
        )
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает змею к начальным параметрам."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None

    def draw(self, surface):
        """Рисует змею на экране с границами и головой."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(
                (position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Возвращает текущую позицию головы змеи."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змеи, если есть новое."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления направлением объекта."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            keydown = [
                (pygame.K_UP, DOWN, UP),
                (pygame.K_DOWN, UP, DOWN),
                (pygame.K_LEFT, RIGHT, LEFT),
                (pygame.K_RIGHT, LEFT, RIGHT),
            ]
            for key, direction, next_direction in keydown:
                if event.key == key and game_object.direction != direction:
                    game_object.next_direction = next_direction
                    break


def main():
    """Основной игровой цикл."""
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
