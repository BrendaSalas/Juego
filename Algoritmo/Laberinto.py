import pygame
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
GREEN = (0, 255, 0)  # Color para el jugador
BLACK = (0, 0, 0)  # Color para las paredes

# Velocidad del jugador
PLAYER_SPEED = 5


# Clase para el Jugador
class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)  # Representar al jugador como un rectángulo

    def move(self, dx, dy):
        if 0 <= self.rect.x + dx <= SCREEN_WIDTH - 20:
            self.rect.x += dx
        if 0 <= self.rect.y + dy <= SCREEN_HEIGHT - 20:
            self.rect.y += dy

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.rect)  # Dibujar al jugador


# Clase para el Laberinto
class Maze:
    def __init__(self):
        self.walls = self.create_walls()

    def create_walls(self):
        walls = []
        for _ in range(10):  # Generar 10 paredes
            x = random.randint(0, SCREEN_WIDTH // 20 - 1) * 20
            y = random.randint(0, SCREEN_HEIGHT // 20 - 1) * 20
            walls.append(pygame.Rect(x, y, 20, 20))
        return walls

    def draw(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, BLACK, wall)  # Dibujar las paredes


# Clase Juego principal
class Game:
    def __init__(self):
        self.player = Player(20, 20)  # El jugador empieza en (20, 20)
        self.maze = Maze()
        self.game_over = False

    def check_collision(self):
        # Verificar si el jugador colisiona con alguna pared
        for wall in self.maze.walls:
            if self.player.rect.colliderect(wall):
                self.game_over = True
                break

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move(-PLAYER_SPEED, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move(PLAYER_SPEED, 0)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.move(0, -PLAYER_SPEED)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player.move(0, PLAYER_SPEED)

        self.check_collision()

    def draw(self):
        screen.fill(WHITE)  # Fondo blanco
        self.maze.draw(screen)
        self.player.draw(screen)


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


