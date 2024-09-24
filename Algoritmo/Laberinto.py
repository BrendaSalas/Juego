﻿import pygame
import random
import time

# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK_BACKGROUND = (255, 203, 220)  # Color de fondo #ffcbdc
TEXT_COLOR = (213, 0, 69)  # Color del texto

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
        pygame.draw.rect(screen, GREEN, self.rect)


# Clase para el Laberinto
class Maze:
    def __init__(self):
        self.walls = []
        self.create_maze()

    def create_maze(self):
        # Genera un laberinto sencillo
        for _ in range(30):  # número de paredes (menor cantidad para un laberinto más sencillo)
            x = random.randint(0, SCREEN_WIDTH // 20 - 1) * 20
            y = random.randint(HEADER_HEIGHT // 20, (SCREEN_HEIGHT - HEADER_HEIGHT) // 20 - 1) * 20 + HEADER_HEIGHT
            self.walls.append(pygame.Rect(x, y, 20, 20))

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, BLACK, wall)


# Clase Juego principal
class Game:
    def __init__(self, player_name):
        self.player = Player(20, HEADER_HEIGHT + 20)  # Ajusta la posición inicial del jugador
        self.maze = Maze()
        self.score = 0
        self.level = 1
        self.game_over = False
        self.player_name = player_name
        self.scores_per_level = []  # Lista para almacenar los puntajes por nivel
        self.finish_line = pygame.Rect(SCREEN_WIDTH - 40, SCREEN_HEIGHT - 80, 20, 80)  # Línea de meta

    def reset(self):
        # Almacena el puntaje actual en la lista antes de resetear
        self.scores_per_level.append(self.score)
        self.player = Player(20, HEADER_HEIGHT + 20)  # Ajusta la posición inicial del jugador
        self.maze = Maze()
        self.score = 0
        self.level += 1

    def check_collision(self):
        # Verifica si el jugador choca con alguna pared
        for wall in self.maze.walls:
            if self.player.rect.colliderect(wall):
                self.game_over = True
                break

    def check_finish(self):
        # Verifica si el jugador ha alcanzado la línea de meta
        if self.player.rect.colliderect(self.finish_line):
            self.reset()  # Reinicia el juego al llegar a la meta

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.player.move(-PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT]:
            self.player.move(PLAYER_SPEED, 0)
        if keys[pygame.K_UP]:
            self.player.move(0, -PLAYER_SPEED)
        if keys[pygame.K_DOWN]:
            self.player.move(0, PLAYER_SPEED)

        self.check_collision()
        self.check_finish()

    def draw(self):
        screen.fill(PINK_BACKGROUND)  # Cambia el fondo del juego al color rosa
        # Dibuja el área del encabezado
        pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, HEADER_HEIGHT))
        self.maze.draw(screen)
        self.player.draw(screen)
        pygame.draw.rect(screen, RED, self.finish_line)  # Dibuja la línea de meta
        self.draw_score()

    def draw_score(self):
        score_text = font_medium.render(f"{self.player_name} - Nivel: {self.level} - Puntos: {self.score}", True,
                                        TEXT_COLOR)
        screen.blit(score_text, (10, 10))

    def show_score_table(self):
        screen.fill(PINK_BACKGROUND)  # Cambia el fondo de la tabla de puntajes al color rosa
        title = font_medium.render("Tabla de Puntajes", True, TEXT_COLOR)
        screen.blit(title, (SCREEN_WIDTH // 2 - 100, 20))

        # Mostrar los puntajes obtenidos en cada nivel
        for i, score in enumerate(self.scores_per_level):
            level_text = font_medium.render(f"Nivel {i + 1}: {score} puntos", True, TEXT_COLOR)
            screen.blit(level_text, (SCREEN_WIDTH // 2 - 100, 80 + i * 40))

        pygame.display.flip()
        time.sleep(5)


def show_instructions():
    screen.fill(PINK_BACKGROUND)  # Cambia el fondo de las instrucciones al color rosa
    instructions = [
        "Instrucciones:",
        "1. Usa las teclas de flecha para moverte.",
        "2. Evita las paredes.",
        "3. Gana puntos por completar el laberinto.",
        "4. Llega a la línea de meta para avanzar.",
        "5. ¡Buena suerte!",
        "Presiona 'Esc' para regresar al menú principal."
    ]
    for i, line in enumerate(instructions):
        text = font_medium.render(line, True, TEXT_COLOR)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 50 + i * 40))  # Alinear al centro
        screen.blit(text, text_rect)
    pygame.display.flip()
    time.sleep(5)


# Función para capturar el nombre del jugador
def get_player_name():
    name = ""
    input_active = True

    while input_active:
        screen.fill(PINK_BACKGROUND)  # Cambia el fondo del nombre al color rosa
        prompt = font_medium.render("Nombre del jugador:", True, TEXT_COLOR)  # Cambiado el texto
        screen.blit(prompt, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50))

        name_text = font_medium.render(name, True, TEXT_COLOR)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(name) == 5:
                    input_active = False  # Sale del bucle si el nombre tiene 5 letras
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 5 and event.unicode.isalpha():
                    name += event.unicode.upper()

    return name


# Menú principal
def main_menu(game_scores):
    while True:
        screen.fill(PINK_BACKGROUND)  # Cambia el fondo del menú al color rosa
        title = font_large.render("PinkMaze", True, TEXT_COLOR)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 80))  # Centrar el título
        screen.blit(title, title_rect)

        options = ["Comenzar nueva partida (1)", "Instrucciones (2)", "Ver puntajes (3)"]  # Nuevas opciones
        for i, option in enumerate(options):
            text = font_medium.render(option, True, TEXT_COLOR)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 50))  # Centrar las opciones
            screen.blit(text, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return game_scores  # Sale del menú y empieza el juego
                elif event.key == pygame.K_2:
                    show_instructions()
                elif event.key == pygame.K_3:
                    show_score_table(game_scores)


# Iniciar el juego
def main():
    running = True
    in_menu = True
    player_name = ""
    game_scores = []

    while running:
        keys = pygame.key.get_pressed()  # Captura las teclas presionadas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if in_menu:
                    if event.key == pygame.K_1:
                        player_name = get_player_name()  # Pide el nombre
                        in_menu = False  # Iniciar juego
                    elif event.key == pygame.K_2:
                        show_instructions()
                    elif event.key == pygame.K_3:  # Nueva opción para ver puntajes
                        game = Game(player_name)
                        game.scores_per_level = game_scores  # Cargar puntajes previos
                        game.show_score_table()
                else:
                    if event.key == pygame.K_ESCAPE:  # Si se presiona 'Esc', regresa al menú principal
                        in_menu = True

        if in_menu:
            game_scores = main_menu(game_scores)
        else:
            game = Game(player_name)
            while not game.game_over:
                game.update(keys)  # Actualiza el juego con las teclas presionadas
                game.draw()
                pygame.display.flip()
                clock.tick(FPS)  # Controlar el FPS

            # Mostrar tabla de puntajes al final y almacenar los puntajes
            game.show_score_table()
            game_scores = game.scores_per_level  # Almacenar puntajes al final
            in_menu = True  # Regresar al menú

    pygame.quit()


if __name__ == "__main__":
    main()
