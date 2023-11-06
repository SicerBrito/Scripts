import pygame
import random
import math
import pygetwindow as gw

pygame.init()

# Configuración de la pantalla
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Obtener todas las ventanas abiertas
windows = gw.getWindowsWithTitle('')
target_windows = [window for window in windows if window.isMinimized == False]

# Clase para representar la animación
class Animation:
    def __init__(self, window):
        self.window = window
        self.speed = 5
        self.rect = pygame.Rect(0, 0, 50, 50)
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Fondo transparente
        pygame.draw.circle(self.image, (255, 0, 0), (25, 25), 25)  # Círculo rojo

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx)
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Lista de animaciones para cada ventana
animations = [Animation(window) for window in target_windows]

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar las animaciones
    for animation in animations:
        animation.update()

    # Dibujar las animaciones sobre las ventanas
    for animation in animations:
        if animation.window.isActive:
            window_rect = animation.window.left, animation.window.top, animation.window.width, animation.window.height
            pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0, 0), window_rect)  # Limpiar ventana
            animation.draw(pygame.display.get_surface())

    pygame.display.flip()

pygame.quit()
