import pygame
import random
import time

# Inicializar pygame
pygame.init()

# Dimensiones de la pantalla
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 200  # Menor altura para un juego 1D
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)  # Color para el jugador
BLACK = (0, 0, 0)  # Color para las paredes

# Velocidad del jugador
PLAYER_SPEED = 5


# Clase para el Jugador
class Player:
    def __init__(self, position):
        self.position = position  # Posición en el eje X

    def move(self, dx):
        if 0 <= self.position + dx <= (SCREEN_WIDTH // 10 - 1):  # Para ajustar a la longitud del laberinto
            self.position += dx

    def draw(self, screen):
        # Representar el jugador como '.'
        text_surface = font.render('.', True, GREEN)
        screen.blit(text_surface, (self.position * 10 + 10, SCREEN_HEIGHT // 2 - 30))  # Posicionar el jugador


# Clase para el Laberinto
class Maze:
    def __init__(self):
        self.walls = self.create_walls()

    def create_walls(self):
        # Generar algunas paredes en posiciones aleatorias
        wall_positions = random.sample(range(1, SCREEN_WIDTH // 10 - 1), 5)  # Evitar el inicio y fin
        return sorted(wall_positions)

    def draw(self, screen):
        for pos in self.walls:
            # Representar las paredes como números
            text_surface = font.render('1', True, BLACK)
            screen.blit(text_surface, (pos * 10 + 10, SCREEN_HEIGHT // 2 - 30))  # Posicionar las paredes


# Clase Juego principal
class Game:
    def __init__(self):
        self.player = Player(0)  # El jugador empieza en la posición 0
        self.maze = Maze()
        self.game_over = False

    def check_collision(self):
        # Verifica si el jugador colisiona con una pared
        if self.player.position in self.maze.walls:
            self.game_over = True

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move(-1)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move(1)

        self.check_collision()

    def draw(self):
        screen.fill(WHITE)  # Fondo blanco
        self.maze.draw(screen)
        self.player.draw(screen)


# Fuente
font = pygame.font.Font(None, 60)  # Fuente predeterminada


def main():
    running = True
    game = Game()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update()
        game.draw()
        pygame.display.flip()
        pygame.time.Clock().tick(60)

        if game.game_over:
            print("Game Over! Reiniciando el juego...")
            time.sleep(1)
            game = Game()  # Reinicia el juego

    pygame.quit()


if __name__ == "__main__":
    main()
