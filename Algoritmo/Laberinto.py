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


# Clase para el Laberinto
class Maze:
    def __init__(self, level):
        self.walls = []
        self.grid_size = 15  # Tamaño de la cuadrícula para generar paredes
        self.create_maze(level)

    def create_maze(self, level):
        # Genera un laberinto más estructurado en una cuadrícula
        cell_width = SCREEN_WIDTH // self.grid_size
        cell_height = (SCREEN_HEIGHT - HEADER_HEIGHT) // self.grid_size

        for row in range(self.grid_size):
            for col in range(self.grid_size):
                if random.choice([True, False]):
                    # Crear paredes horizontales o verticales
                    if random.choice([True, False]):
                        wall_x = col * cell_width
                        wall_y = row * cell_height + HEADER_HEIGHT
                        wall_width = cell_width
                        wall_height = 10
                    else:
                        wall_x = col * cell_width
                        wall_y = row * cell_height + HEADER_HEIGHT
                        wall_width = 10
                        wall_height = cell_height

                    wall_rect = pygame.Rect(wall_x, wall_y, wall_width, wall_height)

                    # Evitar que las paredes interfieran con la meta
                    if not self.is_wall_blocking_goal(wall_rect):
                        self.walls.append(wall_rect)

    def is_wall_blocking_goal(self, wall_rect):
        # Verifica si la pared está bloqueando el área de la meta
        goal_area = pygame.Rect(SCREEN_WIDTH - 60, SCREEN_HEIGHT - 80, 60, 80)
        return wall_rect.colliderect(goal_area)

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, BLACK, wall)


# Clase Juego principal
class Game:
    def __init__(self, player_name):
        self.player = Player(20, HEADER_HEIGHT + 20)  # Ajusta la posición inicial del jugador
        self.score = 0
        self.level = 1
        self.game_over = False
        self.player_name = player_name
        self.finish_line = pygame.Rect(SCREEN_WIDTH - 40, SCREEN_HEIGHT - 80, 20, 80)  # Línea de meta
        self.maze = Maze(self.level)  # Generar laberinto para el nivel actual

    def reset(self):
        # Reinicia el juego al chocar con una pared o ganar un nivel
        self.level = 1
        self.score = 0
        self.player = Player(20, HEADER_HEIGHT + 20)  # Ajusta la posición inicial del jugador
        self.maze = Maze(self.level)
        self.finish_line = pygame.Rect(SCREEN_WIDTH - 40, SCREEN_HEIGHT - 80, 20, 80)

    def check_collision(self):
        # Verifica si el jugador choca con alguna pared
        for wall in self.maze.walls:
            if self.player.rect.colliderect(wall):
                self.show_game_over()  # Muestra mensaje de "Has perdido"
                self.reset()  # Reinicia el juego
                break

    def check_finish(self):
        # Verifica si el jugador ha alcanzado la línea de meta
        if self.player.rect.colliderect(self.finish_line):
            self.level += 1
            self.maze = Maze(self.level)  # Generar un nuevo laberinto con más dificultad
            self.player = Player(20, HEADER_HEIGHT + 20)  # Coloca al jugador en la posición inicial
            self.finish_line = pygame.Rect(random.randint(400, SCREEN_WIDTH - 40),
                                           random.randint(200, SCREEN_HEIGHT - 80), 20, 80)
            self.score += 100  # Aumenta el puntaje al completar el nivel

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
        # Dibuja el área del encabezado
        pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, HEADER_HEIGHT))
        self.maze.draw(screen)
        self.player.draw(screen)
        pygame.draw.rect(screen, GREEN, self.finish_line)  # Dibuja la línea de meta de color verde
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


# Función para capturar el nombre del jugador
def get_player_name():
    name = ""
    input_active = True

    while input_active:
        screen.fill(WHITE)  # Fondo blanco para capturar el nombre
        prompt = font_medium.render("Nombre del jugador:", True, BLACK)  # Cambiado el texto
        screen.blit(prompt, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

        name_text = font_medium.render(name, True, BLACK)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False  # Sale del bucle al presionar ENTER
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode.isalpha() or event.unicode.isspace():  # Permitir letras y espacios
                    name += event.unicode.upper()

    return name


# Menú principal
def main_menu():
    while True:
        screen.fill(WHITE)  # Fondo blanco para el menú principal
        title = font_large.render("PinkMaze", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - 100, 50))  # Centrar el título

        options = [
            "Presiona (1) para iniciar una nueva partida",
            "Presiona (2) para ver las instrucciones",
        ]

        for i, option in enumerate(options):
            text = font_medium.render(option, True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 150 + i * 50))  # Alinear al centro
            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player_name = get_player_name()
                    game = Game(player_name)
                    run_game(game)
                if event.key == pygame.K_2:
                    show_instructions()


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
                    running = False  # Sale del juego

    pygame.quit()


def show_instructions():
    while True:
        screen.fill(WHITE)
        instructions_text = font_medium.render("Usa las flechas o WASD para moverte.", True, BLACK)
        text_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(instructions_text, text_rect)

        back_text = font_medium.render("Presiona ESC para regresar", True, BLACK)
        back_rect = back_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(back_text, back_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return  # Regresa al menú principal


if __name__ == "__main__":
    main_menu()
