import os
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import pygame
import random

# Inicializar Pygame


# Dimensiones de la ventana
width, height = 600, 400
window = pygame.display.set_mode((width, height))

# Colores
black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)

# Clase para la serpiente
class Snake:
    def __init__(self):
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = 'RIGHT'

    def move(self):
        head = self.body[0][:]
        if self.direction == 'RIGHT':
            head[0] += 10
        elif self.direction == 'LEFT':
            head[0] -= 10
        elif self.direction == 'UP':
            head[1] -= 10
        elif self.direction == 'DOWN':
            head[1] += 10
        self.body.insert(0, head)
        self.body.pop()

    def change_direction(self, direction):
        self.direction = direction

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(window, green, pygame.Rect(segment[0], segment[1], 10, 10))

# Bucle principal del juego
snake = Snake()
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction('UP')
            elif event.key == pygame.K_DOWN:
                snake.change_direction('DOWN')
            elif event.key == pygame.K_LEFT:
                snake.change_direction('LEFT')
            elif event.key == pygame.K_RIGHT:
                snake.change_direction('RIGHT')

    window.fill(black)
    snake.move()
    snake.draw()
    pygame.display.flip()
    clock.tick(15)
    
def ejecutar():
    pygame.init()

if __name__ == "__main__":
    ejecutar()
