# py -m pip install pygame 
# py -m pip install pywin32


import pygame, sys, random
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

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Aquí puedes agregar el código para dibujar y actualizar el juego.

        pygame.display.flip()  # Actualizar la pantalla
        clock.tick(60)  # Limitar la velocidad de cuadros a 60 FPS
