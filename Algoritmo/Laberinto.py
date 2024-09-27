import pygame
import random
import time

# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
CELL_SIZE = 40  # Tamaño de las celdas en el laberinto
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)  # Color verde para la meta

# Fuente: Usar fuente del sistema
font_large = pygame.font.SysFont('Arial', 50)  # Fuente grande para el título
font_medium = pygame.font.SysFont('Arial', 36)  # Fuente mediana para el resto

# Velocidad del jugador
PLAYER_SPEED = 5
HEADER_HEIGHT = 50  # Altura del área del encabezado

# FPS (Frames por segundo)
FPS = 60
clock = pygame.time.Clock()


# Clase para el Jugador
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)

    def move(self, dx, dy):
        if 0 <= self.rect.x + dx <= SCREEN_WIDTH - 20:
            self.rect.x += dx
        if 0 <= self.rect.y + dy <= SCREEN_HEIGHT - HEADER_HEIGHT - 20:  # Ajusta para la altura del encabezado
            self.rect.y += dy

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, self.rect)


# Clase para el Laberinto con algoritmo de backtracking recursivo
class Maze:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.cell_width = SCREEN_WIDTH // self.grid_size
        self.cell_height = (SCREEN_HEIGHT - HEADER_HEIGHT) // self.grid_size
        self.visited = [[False for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.grid = [[1 for _ in range(self.grid_size)] for _ in range(self.grid_size)]  # 1 = pared, 0 = camino
        self.generate_maze(0, 0)  # Genera el laberinto desde la esquina superior izquierda

    def generate_maze(self, x, y):
        self.visited[y][x] = True
        self.grid[y][x] = 0  # Marcar la celda como parte del camino

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)  # Mezcla las direcciones para generar caminos aleatorios

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size and not self.visited[ny][nx]:
                # Crear el camino entre las celdas
                if dx == 1:  # Mover derecha
                    self.grid[y][x + 1] = 0
                elif dx == -1:  # Mover izquierda
                    self.grid[y][x - 1] = 0
                elif dy == 1:  # Mover abajo
                    self.grid[y + 1][x] = 0
                elif dy == -1:  # Mover arriba
                    self.grid[y - 1][x] = 0

                self.generate_maze(nx, ny)

    def draw(self, screen):
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[y][x] == 1:  # Dibuja las paredes
                    pygame.draw.rect(screen, BLACK, (
                    x * self.cell_width, y * self.cell_height + HEADER_HEIGHT, self.cell_width, self.cell_height))


# Clase Juego principal
class Game:
    def __init__(self, player_name):
        self.player = Player(20, HEADER_HEIGHT + 20)  # Ajusta la posición inicial del jugador
        self.score = 0
        self.level = 1
        self.game_over = False
        self.player_name = player_name
        self.finish_line = pygame.Rect(SCREEN_WIDTH - 40, SCREEN_HEIGHT - 80, 20, 80)  # Línea de meta
        self.maze = Maze(15)  # Generar laberinto para el nivel actual

    def reset(self):
        self.level = 1
        self.score = 0
        self.player = Player(20, HEADER_HEIGHT + 20)  # Ajusta la posición inicial del jugador
        self.maze = Maze(15)
        self.finish_line = pygame.Rect(SCREEN_WIDTH - 40, SCREEN_HEIGHT - 80, 20, 80)

    def check_collision(self):
        # Verifica si el jugador choca con alguna pared
        for y in range(self.maze.grid_size):
            for x in range(self.maze.grid_size):
                if self.maze.grid[y][x] == 1:
                    wall_rect = pygame.Rect(x * self.maze.cell_width, y * self.maze.cell_height + HEADER_HEIGHT,
                                            self.maze.cell_width, self.maze.cell_height)
                    if self.player.rect.colliderect(wall_rect):
                        self.show_game_over()
                        self.reset()
                        return

    def check_finish(self):
        # Verifica si el jugador ha alcanzado la línea de meta
        if self.player.rect.colliderect(self.finish_line):
            self.level += 1
            self.maze = Maze(15)
            self.player = Player(20, HEADER_HEIGHT + 20)
            self.finish_line = pygame.Rect(random.randint(400, SCREEN_WIDTH - 40),
                                           random.randint(200, SCREEN_HEIGHT - 80), 20, 80)
            self.score += 100

    def update(self, keys):
        # Movimiento con teclas de flechas o WASD
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move(-PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move(PLAYER_SPEED, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.move(0, -PLAYER_SPEED)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.move(0, PLAYER_SPEED)

        self.check_collision()
        self.check_finish()

    def draw(self):
        screen.fill(WHITE)  # Fondo blanco
        pygame.draw.rect(screen, GREEN, self.finish_line)  # Dibuja la línea de meta en verde
        self.maze.draw(screen)
        self.player.draw(screen)
        self.draw_score()

    def draw_score(self):
        score_text = font_medium.render(f"{self.player_name} - Nivel: {self.level} - Puntos: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    def show_game_over(self):
        # Muestra un mensaje de "Has perdido" y pausa por 2 segundos
        screen.fill(WHITE)
        game_over_text = font_large.render("¡Has perdido!", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()
        time.sleep(2)  # Pausa por 2 segundos antes de reiniciar el juego


# Función para capturar el nombre del jugador en una ventana aparte
def get_player_name():
    name = ""
    input_active = True

    while input_active:
        screen.fill(WHITE)  # Fondo blanco
        prompt = font_medium.render("Nombre del jugador:", True, BLACK)  # Texto de solicitud
        screen.blit(prompt, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

        name_text = font_medium.render(name, True, BLACK)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) > 0:  # Acepta cualquier longitud de nombre
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isalpha():
                    name += event.unicode.upper()

    return name


# Pantalla de instrucciones
def show_instructions():
    while True:
        screen.fill(WHITE)
        instructions_title = font_large.render("Instrucciones", True, BLACK)
        screen.blit(instructions_title, (SCREEN_WIDTH // 2 - 150, 50))

        instructions_text = [
            "Usa las teclas de flechas o WASD para moverte.",
            "Llega a la meta verde sin chocar con las paredes.",
            "Pulsa ENTER para ir a la pantalla de nombre."
        ]

        for i, text in enumerate(instructions_text):
            instruction_line = font_medium.render(text, True, BLACK)
            screen.blit(instruction_line, (50, 150 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Sale a la pantalla de nombre


# Menú principal
def main_menu():
    while True:
        screen.fill(WHITE)
        title = font_large.render("PinkMaze", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - 100, 50))

        start_option = font_medium.render("Presiona (1) para iniciar el juego", True, BLACK)
        screen.blit(start_option, (SCREEN_WIDTH // 2 - 200, 200))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    show_instructions()  # Muestra las instrucciones
                    player_name = get_player_name()  # Luego pide el nombre del jugador
                    game = Game(player_name)
                    run_game(game)


# Función principal del juego
def run_game(game):
    running = True

    while running:
        keys = pygame.key.get_pressed()
        game.update(keys)
        game.draw()
        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

    pygame.quit()


if __name__ == "__main__":
    main_menu()
