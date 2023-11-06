import win32gui
import win32con
import pygame
import time

# Inicializa Pygame
pygame.init()

# Tamaño de la ventana
window_width, window_height = 100, 100

# Crear una ventana de Pygame
screen = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)

# Colores
black = (0, 0, 0)
red = (255, 0, 0)

# Función para mover la ventana de Pygame
def move_window(x, y):
    hwnd = pygame.display.get_wm_info()['window']
    win32gui.MoveWindow(hwnd, x, y, window_width, window_height, True)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener la posición del ratón
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Mover la ventana de Pygame a la posición del ratón
    move_window(mouse_x, mouse_y)

    # Dibujar una animación simple
    screen.fill(black)
    pygame.draw.circle(screen, red, (window_width // 2, window_height // 2), 25)
    pygame.display.update()

    time.sleep(0.01)

pygame.quit()
