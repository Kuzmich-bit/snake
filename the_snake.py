"""Игра «Змейка» («Изгиб Питона»)."""

import sys
from random import randint

import pygame

pygame.init()

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
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Изгиб Питона')
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс всех игровых объектов."""

    def __init__(self, position=CENTER_POSITION, body_color=None):
        """Инициализирует позицию и цвет объекта."""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Метод отрисовки объекта. Переопределяется в дочерних классах."""
        pass


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self, snake_positions=None):
        """Задаёт цвет яблока и устанавливает его начальную позицию."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions=None):
        """Устанавливает случайное положение яблока на поле."""
        if snake_positions is None:
            snake_positions = []
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if position not in snake_positions:
                self.position = position
                break

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction is None:
            return
        opposite = (-self.direction[0], -self.direction[1])
        if self.next_direction != opposite:
            self.direction = self.next_direction
        self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        dir_x, dir_y = self.direction
        new_head = (
            (head_x + dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                snake.next_direction = UP
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                snake.next_direction = DOWN
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                snake.next_direction = LEFT
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                snake.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def main():
    """Основной игровой цикл."""
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

        clock.tick(SPEED)


if __name__ == '__main__':
    main()
