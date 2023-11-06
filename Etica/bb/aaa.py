import pygame
import sys
import win32api
import win32con
import win32gui

def hide_console():
    window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(window, win32con.SW_HIDE)

if __name__ == "__main__":
    hide_console()

    pygame.init()

    clock = pygame.time.Clock()

    # Obtener información de la pantalla actual
    screen_info = pygame.display.Info()

    # Definir el ancho y alto de la pantalla
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    # Crear la ventana del juego
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Definir los colores
    black = (0, 0, 0)
    white = (255, 255, 255)

    # Inicializar las coordenadas de la bola
    ball_x = screen_width // 2
    ball_y = screen_height // 2
    ball_speed_x = 5
    ball_speed_y = 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Mover la bola
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Detección de colisiones con los bordes de la ventana
        if ball_x >= screen_width or ball_x <= 0:
            ball_speed_x *= -1
        if ball_y >= screen_height or ball_y <= 0:
            ball_speed_y *= -1

        # Limpiar la pantalla
        screen.fill(black)

        # Dibujar la bola
        pygame.draw.circle(screen, white, (ball_x, ball_y), 10)

        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(60)  # Limitar la velocidad de cuadros a 60 FPS
