import pygame, sys, random
import win32api
import win32con
import win32gui
import math
import random

def hide_console():
    window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(window, win32con.SW_HIDE)

if __name__ == "__main__":
    hide_console()

pygame.init()

clock = pygame.time.Clock()

screen_info = pygame.display.info()

screen_width = screen_info.current_w
screen_height= screen_info.current_h
print(screen_width, screen_height)