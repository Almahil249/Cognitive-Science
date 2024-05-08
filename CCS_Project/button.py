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
    if button_rect.collidepoint(mouse_pos):
        color = hover_color
    else:
        color = button_color
    pygame.draw.rect(screen, color, button_rect)

    # Draw text on button
    button_text = font.render('Auto Play', True, text_color)
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    return button_rect  # Return button rectangle for click detection

# Main game loop
# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#         # Check for mouse click
#         if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
#             # Check if the click was within the button's area
#             if draw_button(screen, (SCREEN_WIDTH - BUTTON_WIDTH) / 2, (SCREEN_HEIGHT - BUTTON_HEIGHT) / 2,
#                            BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, HOVER_COLOR, "Click Me", TEXT_COLOR).collidepoint(event.pos):
#                 print("Button clicked!")

#     # Fill the background
#     screen.fill((255, 255, 255))  # White background

    # Draw the button
    draw_button(screen, (SCREEN_WIDTH - BUTTON_WIDTH) / 2, (SCREEN_HEIGHT - BUTTON_HEIGHT) / 2,
                BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, HOVER_COLOR, "Click Me", TEXT_COLOR)

    # # Update the display
    # pygame.display.flip()
