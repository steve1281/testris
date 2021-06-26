import numpy as np
import pygame
from rgb import *

# note: we add 5 to the board.
board = np.zeros((25, 45), dtype=[ ('r', 'i4'), ('g', 'i4'), ('b', 'i4') ])
m = np.zeros((5, 5), dtype=[ ('r', 'i4'), ('g', 'i4'), ('b', 'i4') ])


def l_shape(m):
    m.fill(DARK_BLUE)
    m[ 2 ][ 1 ] = RED
    m[ 2 ][ 2 ] = RED
    m[ 2 ][ 3 ] = RED
    m[ 3 ][ 3 ] = RED


# init pygame
pygame.init()

WIDTH = 700
HEIGHT = 500

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("-- Testing --")

PLOT_X = 400
PLOT_Y = 400

OFFSET_Y = (HEIGHT - PLOT_Y) // 2
OFFSET_X = (WIDTH - PLOT_X) // 2

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

l_shape(m)
m_x = 5
m_y = 1

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            carryOn = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                carryOn = False
            if event.key == pygame.K_LEFT:
                # numpy.rot90(m, k=1, axes=(0, 1))[source]¶
                # m = np.rot90(m)
                m_y = m_y - 1
            if event.key == pygame.K_UP:
                m = np.rot90(m)
                m = np.rot90(m)
                m = np.rot90(m)
            if event.key == pygame.K_DOWN:
                m_x = m_x + 1
            if event.key == pygame.K_RIGHT:
                m_y = m_y + 1

    screen.fill(DARK_SLATE_GRAY)
    board.fill(DARK_BLUE)

    # The you can draw different shapes and lines or add text to your background stage.
    ICON_X = 400 / 40
    ICON_Y = 400 / 20

    board[ m_x:m_x + m.shape[ 0 ], m_y:m_y + m.shape[ 1 ] ] = m

    pygame.draw.rect(screen, ROYAL_BLUE, [ OFFSET_X, OFFSET_Y, PLOT_X, PLOT_Y ], 0)
    # note that we render 5 less, to allow for sprite overflow.
    for y, row in enumerate(board[ :-5 ]):
        for x, col in enumerate(row[ :-5 ]):
            pygame.draw.rect(screen, col,
                             [OFFSET_X + x * ICON_X, OFFSET_Y + y * ICON_Y, ICON_X-1, ICON_Y-1], 0)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
