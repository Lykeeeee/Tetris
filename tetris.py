import pygame
import random

# renk
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SEAGREEN = (84, 255, 159)
CYAN = (0, 255, 255)
CHOCOLATE = (210, 105, 30)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# oyun alanı 
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_SIZE = 30

# sekil
SHAPES = [
    ([[1, 1, 1, 1]], ORANGE),  # I-Şekli
    ([[1, 1, 1, 0]], SEAGREEN),  # I-Şekli-kısa
    ([[1, 1], [1, 1]], CYAN),  # Kare Şekli
    ([[1, 1], [1, 0]], CHOCOLATE),  # Üçgen Şekli
    ([[1, 1, 0], [0, 1, 1]], GREEN),  # S-Şekli
    ([[0, 1, 1], [1, 1, 0]], RED),  # Z-Şekli
    ([[1, 1, 1], [0, 0, 1]], BLUE),  # L-Şekli
    ([[1, 1, 1], [1, 0, 0]], YELLOW),  # J-Şekli
    ([[1, 1, 1], [0, 1, 0]], MAGENTA),  # Kısa-T-Şekli
]


class TetrisGame:
    def __init__(self):
        pygame.init()

        # Ekran
        self.screen = pygame.display.set_mode((GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE))
        pygame.display.set_caption("Tetris")

        self.clock = pygame.time.Clock()
        self.grid = [[BLACK] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

        self.current_shape, self.current_shape_color = self.get_random_shape()
        self.current_shape_x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_shape_y = 0

        self.fall_time = 0
        self.fall_speed = 0.2

        self.move_time = 0
        self.move_speed = 0.07

        self.fast_fall = False
        self.fast_fall_speed = 0.05

        self.score = 0

    def get_random_shape(self):
        return random.choice(SHAPES)

    def rotate_shape(self):
        rotated_shape = list(zip(*reversed(self.current_shape)))
        return rotated_shape

    def is_valid_move(self, shape, x, y):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j] == 1:
                    if (
                        x + j < 0
                        or x + j >= GRID_WIDTH
                        or y + i >= GRID_HEIGHT
                        or self.grid[y + i][x + j] != BLACK
                    ):
                        return False
        return True

    def move_shape(self, dx, dy):
        new_x = self.current_shape_x + dx
        new_y = self.current_shape_y + dy

        if self.is_valid_move(self.current_shape, new_x, new_y):
            self.current_shape_x = new_x
            self.current_shape_y = new_y

    def rotate_current_shape(self):
        rotated_shape = self.rotate_shape()
        if self.is_valid_move(rotated_shape, self.current_shape_x, self.current_shape_y):
            self.current_shape = rotated_shape

    def lock_shape(self):
        for i in range(len(self.current_shape)):
            for j in range(len(self.current_shape[i])):
                if self.current_shape[i][j] == 1:
                    self.grid[self.current_shape_y + i][self.current_shape_x + j] = self.current_shape_color

        self.current_shape, self.current_shape_color = self.get_random_shape()
        self.current_shape_x = GRID_WIDTH // 2 - len(self.current_shape[0]) // 2
        self.current_shape_y = 0

        self.check_full_rows()

    def check_full_rows(self):
        full_rows = []
        for row in range(len(self.grid)):
            if all(cell != BLACK for cell in self.grid[row]):
                full_rows.append(row)

        if full_rows:
            self.clear_rows(full_rows)
            self.score += len(full_rows) * 100
            if self.score % 500 == 0:
                self.fall_speed -= 0.05
                self.move_speed -= 0.01
                if self.fall_speed < 0.1:
                    self.fall_speed = 0.1
                if self.move_speed < 0.01:
                    self.move_speed = 0.01

    def clear_rows(self, rows):
        for row in rows:
            del self.grid[row]
            self.grid.insert(0, [BLACK] * GRID_WIDTH)

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(self.score), True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def draw_settings_button(self):
        button_font = pygame.font.Font(None, 24)
        button_text = button_font.render("Ayarlar", True, WHITE)
        pygame.draw.rect(self.screen, BLUE, pygame.Rect(GRID_WIDTH * GRID_SIZE - 100, 10, 90, 30))
        self.screen.blit(button_text, (GRID_WIDTH * GRID_SIZE - 95, 15))

    def show_settings_menu(self):
        settings_running = True
        selected_option = 0

        while settings_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    settings_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        settings_running = False
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % 2
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % 2
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:
                            self.change_fall_speed()
                        elif selected_option == 1:
                            self.change_move_speed()

            self.screen.fill(BLACK)
            self.draw_settings_menu_options(selected_option)
            pygame.display.flip()
            self.clock.tick(60)

    def draw_settings_menu_options(self, selected_option):
        menu_font = pygame.font.Font(None, 36)
        option_font = pygame.font.Font(None, 24)

        title_text = menu_font.render("Ayarlar", True, WHITE)
        self.screen.blit(title_text, (10, 10))

        option1_text = option_font.render("1. Düşme Hızı: " + str(self.fall_speed), True, WHITE)
        option2_text = option_font.render("2. Hareket Hızı: " + str(self.move_speed), True, WHITE)

        if selected_option == 0:
            pygame.draw.rect(self.screen, BLUE, pygame.Rect(10, 50, option1_text.get_width() + 10, option1_text.get_height()))
        elif selected_option == 1:
            pygame.draw.rect(self.screen, BLUE, pygame.Rect(10, 80, option2_text.get_width() + 10, option2_text.get_height()))

        self.screen.blit(option1_text, (15, 55))
        self.screen.blit(option2_text, (15, 85))

    def change_fall_speed(self):
        new_fall_speed = float(input("Yeni düşme hızını girin (0.1 - 1 arasında): "))
        if 0.1 <= new_fall_speed <= 1:
            self.fall_speed = new_fall_speed

    def change_move_speed(self):
        new_move_speed = float(input("Yeni hareket hızını girin (0.01 - 0.1 arasında): "))
        if 0.01 <= new_move_speed <= 0.1:
            self.move_speed = new_move_speed

    def run(self):
        running = True

        move_left = False
        move_right = False
        move_down = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        move_left = True
                    elif event.key == pygame.K_RIGHT:
                        move_right = True
                    elif event.key == pygame.K_DOWN:
                        move_down = True
                    elif event.key == pygame.K_UP:
                        self.rotate_current_shape()
                    elif event.key == pygame.K_ESCAPE:
                        self.show_settings_menu()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        move_left = False
                    elif event.key == pygame.K_RIGHT:
                        move_right = False
                    elif event.key == pygame.K_DOWN:
                        move_down = False

            self.move_time += self.clock.get_rawtime() / 1000

            if move_left and self.move_time >= self.move_speed:
                self.move_shape(-1, 0)
                self.move_time = 0
            elif move_right and self.move_time >= self.move_speed:
                self.move_shape(1, 0)
                self.move_time = 0
            elif move_down and self.move_time >= self.move_speed:
                self.move_shape(0, 1)
                self.move_time = 0

            self.fall_time += self.clock.get_rawtime() / 1000
            if self.fall_time >= self.fall_speed:
                if self.is_valid_move(self.current_shape, self.current_shape_x, self.current_shape_y + 1):
                    self.current_shape_y += 1
                else:
                    self.lock_shape()
                self.fall_time = 0

            self.screen.fill(BLACK)

            for i in range(GRID_HEIGHT):
                for j in range(GRID_WIDTH):
                    pygame.draw.rect(
                        self.screen,
                        self.grid[i][j],
                        pygame.Rect(j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE),
                    )

            for i in range(len(self.current_shape)):
                for j in range(len(self.current_shape[i])):
                    if self.current_shape[i][j] == 1:
                        pygame.draw.rect(
                            self.screen,
                            self.current_shape_color,
                            pygame.Rect(
                                (self.current_shape_x + j) * GRID_SIZE,
                                (self.current_shape_y + i) * GRID_SIZE,
                                GRID_SIZE,
                                GRID_SIZE,
                            ),
                        )

            self.draw_score()
            self.draw_settings_button()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


game = TetrisGame()
game.run()