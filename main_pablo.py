"""
Biblioteca gráfica para jogos e simulações.
"""
# from typing import List
import pygame
from pygame.locals import QUIT
from components.widgets import StepperWidget
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- SETUP ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Teste')
clock = pygame.time.Clock()

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- DEFAULTS ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
STATE_NOT_STARTED = 0
STATE_STARTED = 1
STATE_PAUSED = 2
STATE_STOPPED = 3
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- VARIABLES ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# state = STATE_NOT_STARTED
speed_factor_widget = StepperWidget ((150, 560), (300, 20), screen)

widgets = [speed_factor_widget]

while True:
    events = pygame.event.get()
    for event in events:
        if event.type == QUIT:
            pygame.quit()
    screen.fill((0,0,0))
    # <----- DRAW ------>
    for widget in widgets:
        widget.listen(events)
        widget.draw()
    # >----- DRAW ------<
    pygame.display.update()
    clock.tick(30)
