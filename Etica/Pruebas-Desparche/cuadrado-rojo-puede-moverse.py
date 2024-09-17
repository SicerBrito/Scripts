# Este código es un ejemplo básico de un juego en Pygame donde controlas un cuadrado rojo que puede moverse por la pantalla utilizando las teclas de dirección (arriba, abajo, izquierda y derecha).

import pygame
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
screen_width = 800
screen_height = 600

# Crear la ventana del juego
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mi Juego")

# Variables del juego
player_x = screen_width // 2
player_y = screen_height // 2
player_speed = 5

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Lógica del juego
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # Dibujar en la pantalla
    screen.fill((0, 0, 0))  # Rellenar la pantalla con color negro
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, 50, 50))  # Dibujar un rectángulo rojo

    pygame.display.flip()  # Actualizar la pantalla

# Finalizar Pygame
pygame.quit()
