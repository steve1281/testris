import numpy as np
import pygame
from pygame.locals import Rect

from rgb import DARK_BLUE, RED, DARK_SLATE_GRAY, ROYAL_BLUE, ORANGE, CYAN, YELLOW, MAGENTA, GREEN, SALMON, BLACK
from tetro import Tetro

# board = np.zeros((25, 45), dtype=[ ('r', 'i4'), ('g', 'i4'), ('b', 'i4') ])
board = np.zeros((25, 45), dtype='i4')  # , dtype=[ ('r', 'i4'), ('g', 'i4'), ('b', 'i4') ])


def _to_rgb(h):
    red = (h >> 16) & 0xff
    green = (h >> 8) & 0xff
    blue = h & 0xff
    return (red, green, blue)


def _to_number(r, g, b):
    h = r
    h = (h << 8) + g
    h = (h << 8) + b
    return h


board[ 10 ][ 10 ] = _to_number(*RED)

# create tetrominoes used in tetris
shapes = [
    Tetro([ (1, 0), (1, 1), (1, 2), (0, 2) ], (3, 3), _to_number(*ROYAL_BLUE)),  # J
    Tetro([ (1, 0), (1, 1), (1, 2), (2, 2) ], (3, 3), _to_number(*ORANGE)),  # L
    Tetro([ (0, 2), (1, 2), (2, 2), (3, 2), (4, 2) ], (5,5),  _to_number(*CYAN)),  # I
    Tetro([ (0, 0), (0, 1), (1, 0), (1, 1) ], (2, 2), _to_number(*YELLOW)),  # O
    Tetro([ (0, 0), (0, 1), (0, 2), (1, 1) ], (3, 3), _to_number(*MAGENTA)),  # T
    Tetro([ (1, 0), (2, 0), (0, 1), (1, 1) ], (3, 2), _to_number(*RED)),  # Z
    Tetro([ (0, 0), (1, 0), (1, 1), (2, 1) ], (3, 2), _to_number(*GREEN))  # S
]


def _shape(tetro: Tetro):
    """ return matrix representing """
    temp = np.zeros((tetro.shape[ 0 ], tetro.shape[ 1 ])) # , dtype=[ ('r', 'i4'), ('g', 'i4'), ('b', 'i4') ])
    temp.fill(BOARD_BACKGROUND_COLOR)
    for i in tetro.tetro:
        temp[ i[ 0 ] ][ i[ 1 ] ] = tetro.color
    return temp



# init pygame
pygame.init()

WIDTH = 900
HEIGHT = 500

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("-- Testing --")

PLOT_X = 800
PLOT_Y = 400
BOARD_BACKGROUND_COLOR = _to_number(*BLACK)  # SALMON  # DARK_BLUE

OFFSET_Y = (HEIGHT - PLOT_Y) // 2
OFFSET_X = (WIDTH - PLOT_X) // 2

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

shape_cnt = 0
m_x = 0
m_y = 40 // 2
m = _shape(shapes[ 0 ])

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
                m_y = m_y - 1
            if event.key == pygame.K_UP:
                m = np.rot90(m)
                m = np.rot90(m)
                m = np.rot90(m)
            if event.key == pygame.K_DOWN:
                m_x = m_x + 1
                board.fill(BOARD_BACKGROUND_COLOR)
                board[ 10, 10 ] = _to_number(*RED)
                # notes: want to place in m_x:m_x + m.shape[0], m_y:m_y+m.shape[1]
                # so question is, is there anything there already?
                # this can be checked with nonzero
                check_board = board[m_x:m_x + m.shape[0],m_y:m_y + m.shape[1]]
                print(m)
                print(check_board)
                ccm = np.nonzero(np.logical_and(m, check_board))
                print(ccm)
                if ccm[0].any():  # check x axis for collision possibilities
                    m_x = m_x - 1  # for now, assume collision


            if event.key == pygame.K_RIGHT:
                m_y = m_y + 1
            if event.key == pygame.K_SPACE:
                shape_cnt = shape_cnt + 1
                if shape_cnt == 7:
                    shape_cnt = 0
                m = _shape(shapes[ shape_cnt ])

    screen.fill(DARK_SLATE_GRAY)
    board.fill(BOARD_BACKGROUND_COLOR)

    # The you can draw different shapes and lines or add text to your background stage.
    ICON_X = 800 / 40
    ICON_Y = 400 / 20

    board[ m_x:m_x + m.shape[ 0 ], m_y:m_y + m.shape[ 1 ] ] = m
    board[ 10, 10 ] = _to_number(*RED)

    pygame.draw.rect(screen, ROYAL_BLUE, [ OFFSET_X, OFFSET_Y, PLOT_X, PLOT_Y ], 0)
    # note that we render 5 less, to allow for sprite overflow.
    for y, row in enumerate(board[ :-5 ]):
        for x, col in enumerate(row[ :-5 ]):
            pygame.draw.rect(screen, _to_rgb(col),
                             Rect(OFFSET_X + x * ICON_X, OFFSET_Y + y * ICON_Y, ICON_X, ICON_Y), 0)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
