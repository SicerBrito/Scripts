import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Set up the display
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mouse Chase and Duplicate")

# Define colors
white = (255, 255, 255)
red = (255, 0, 0)

# Create a class to represent the animation
class Circle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed = 5

    def update(self):
        # Move the circle towards the mouse
        mouse_x, mouse_y = pygame.mouse.get_pos()
        angle = math.atan2(mouse_y - self.rect.centery, mouse_x - self.rect.centerx)
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)

        # Check for collision with the mouse
        if self.rect.colliderect(mouse_rect):
            self.rect.x, self.rect.y = random.randint(0, screen_width - 50), random.randint(0, screen_height - 50)
            circles.add(Circle())

# Create a rectangle to represent the mouse
mouse_rect = pygame.Rect(0, 0, 1, 1)

# Create a group to hold the circles
circles = pygame.sprite.Group()
circles.add(Circle())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the mouse position
    mouse_rect.topleft = pygame.mouse.get_pos()

    # Update the circles
    circles.update()

    # Draw the circles
    screen.fill(white)
    circles.draw(screen)
    pygame.display.flip()

# Quit pygame
pygame.quit()
sys.exit()
