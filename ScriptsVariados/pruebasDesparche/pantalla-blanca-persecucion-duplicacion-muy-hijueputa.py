# Este código crea una ventana de juego en la que una caja roja sigue al puntero del mouse y se duplica al colisionar con él.
# Utiliza pygame para manejar los gráficos y eventos, creando una animación interactiva.

import pygame
import sys
import random
import math


# Inicializa Pygame
pygame.init()

# Configuración de la pantalla
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mouse Chase and Duplicate")

# Definición de colores
white = (255, 255, 255)
red = (255, 0, 0)

# Clase para representar la animación
class Animation(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 5

    def update(self):
        # Mover la animación hacia el mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx)
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)

        # Colisión con el mouse
        if self.rect.colliderect(mouse_rect):
            self.rect.x, self.rect.y = random.randint(0, screen_width - 50), random.randint(0, screen_height - 50)
            animations.add(Animation())

# Rectángulo para representar el mouse
mouse_rect = pygame.Rect(0, 0, 1, 1)

animations = pygame.sprite.Group()
animations.add(Animation())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar la posición del mouse
    mouse_rect.topleft = pygame.mouse.get_pos()

    # Actualizar las animaciones
    animations.update()

    # Dibujar en la pantalla
    screen.fill(white)
    animations.draw(screen)
    pygame.display.flip()

    # Control de la velocidad
    # clock.tick(60)

pygame.quit()
sys.exit()
