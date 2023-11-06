import pygame
import sys
import random
import math
import pygetwindow as gw
import pyautogui

# Inicializa Pygame
pygame.init()

# Configuración de la pantalla
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Obtén todas las ventanas abiertas
windows = gw.getAllWindows()

# Dibuja en cada ventana
for window in windows:
    # Activa la ventana
    window.activate()

    # Crea una nueva superficie para dibujar
    surface = pygame.Surface((window.width, window.height), pygame.SRCALPHA)

    # Dibuja en la superficie
    pygame.draw.circle(surface, (255, 0, 0), (window.width // 2, window.height // 2), 50)

    # Convierte la superficie a una imagen
    image = pygame.image.tostring(surface, 'RGBA')

    # Crea una imagen Pygame desde los datos
    window_image = pygame.image.fromstring(image, (window.width, window.height), 'RGBA')

    # Dibuja la imagen en la ventana
    window_image_rect = window_image.get_rect()
    window_image_rect.topleft = (window.left, window.top)
    window_image_rect.center = (window.width // 2, window.height // 2)
    window_image_rect.move_ip(window.left, window.top)
    window_image.set_alpha(128)
    window_image.set_colorkey((0, 0, 0, 0))
    window.windowSurface.blit(window_image, window_image_rect)

# Actualiza todas las ventanas
pygame.display.update()

# Ejecuta el bucle principal de Pygame
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
sys.exit()