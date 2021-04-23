"""
Teste de camera
"""
# from typing import List
import pygame
from pygame.locals import QUIT
from pygame.math import Vector2 as Vec
from components.camera import Canvas
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- SETUP ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pygame.init()
screen = pygame.display.set_mode((600, 600))
focus = Vec(400, 400)
canvas = Canvas((1000, 1000), screen, focus)
pygame.display.set_caption('Teste')
clock = pygame.time.Clock()
focus.update(0, 0)
point = pygame.Surface((10, 10))
point.fill((255, 0, 0))
canvas.surface.blit(point, (50, 50))
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- VARIABLES ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
    # <----- HOLD KEYS ------>
    keys = pygame.key.get_pressed()
    offset = {
        pygame.K_UP: (0,1), pygame.K_DOWN: (0,-1),
        pygame.K_LEFT: (1,0), pygame.K_RIGHT: (-1,0)
    }
    SPEED_FACTOR= (
        8 if keys[pygame.K_LCTRL] else 2 if keys[pygame.K_LSHIFT] else 4)
    for key in offset:
        if keys[key]:
            focus.update(focus+(Vec(offset[key])*SPEED_FACTOR))
    # -----> HOLD KEYS <------
    screen.fill((0,0,0))
    # <----- DRAW ------>
    canvas.draw()
    # screen.blit(canvas, (0, 0))
    # -----> DRAW <------
    pygame.display.update()
    clock.tick(30)
