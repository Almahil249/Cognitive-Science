import pygame
import sys
from pygame.locals import *

def draw_button(screen, x, y, width, height, button_color, hover_color, text_color):
    font = pygame.font.Font(None, 36)
    # Create button rectangle
    button_rect = pygame.Rect(x, y, width, height)

    # Get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # Determine if mouse is hovering over button
    if button_rect.collidepoint(mouse_pos):
        color = hover_color
    else:
        color = button_color

    # Draw button rectangle
    pygame.draw.rect(screen, color, button_rect)

    # Draw text on button
    button_text = font.render('Auto Play', True, text_color)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    return button_rect  # Return button rectangle for click detection

