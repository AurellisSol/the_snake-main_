from random import randint, choice

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 0)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Координаты центра экрана:
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, body_color=None, border_color=None):
        """Инициализирует объект с начальной позицией и цветом."""
        self.position = CENTER
        self.body_color = body_color
        self.border_color = border_color

    def draw(self):
        """Отрисовывает объект на экране.

        Должен быть переопределен в дочерних классах.
        """
        raise NotImplementedError(
            'Метод draw должен быть переопределен в дочернем классе.'
        )


class Apple(GameObject):
    """Класс для яблока, которое собирает змейка."""

    def __init__(
            self,
            body_color=APPLE_COLOR,
            border_color=BORDER_COLOR,
            occupied_positions=(CENTER)
    ):
        """Инициализирует яблоко с начальной позицией и цветом."""
        super().__init__(body_color=body_color, border_color=border_color)
        self.randomize_position(occupied_positions)

    def draw(self):
        """Отрисовывает яблоко на экране."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, self.border_color, rect, 1)

    def randomize_position(self, occupied_positions):
        """Устанавливает случайную позицию для яблока на игровом поле."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in occupied_positions:
                break


class Snake(GameObject):
    """Класс для змейки, управляемой игроком."""

    def __init__(self, body_color=SNAKE_COLOR, border_color=BORDER_COLOR):
        """Инициализирует змейку с начальной позицией,
        цветом и направлением.
        """
        super().__init__(body_color=body_color, border_color=border_color)
        self.reset()
        self.direction = RIGHT

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = (randint(-1, 1), randint(-1, 1))
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в текущем направлении."""
        x, y = self.direction
        head_x, head_y = self.get_head_position()
        new = (
            (head_x + (x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (y * GRID_SIZE)) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new)

        # Если длина змейки превышает ожидаемую, удаляем последний сегмент.
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self):
        """Отрисовывает змейку на экране."""
        for position in self.positions:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, self.border_color, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш для управления змейкой."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры, запускающая игровой цикл."""
    pg.init()
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка на столкновение с собой.
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(occupied_positions=snake.positions)

        # Проверка на сбор яблока.
        elif snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(occupied_positions=snake.positions)

        # Отрисовка.
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
