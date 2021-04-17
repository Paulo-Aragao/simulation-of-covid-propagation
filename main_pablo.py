"""
Biblioteca gráfica para jogos e simulações.
"""
# from typing import List
import pygame
from pygame.locals import QUIT
from components.widgets import StepperWidget
# from lib.widgets import Widget
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- SETUP ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
pygame.init()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Teste')
clock = pygame.time.Clock()
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- GUI ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- Game UI ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class UIElement:
    """ Generic class holding static UI elements. """
    def __init__(self, pos, size, parent_surface):
        self._pos = pos
        self._size = size
        self._parent_surface = parent_surface
        self._surface = pygame.Surface(self._size)

    def _update_surface(self):
        pass

    def get_pos(self):
        """ Get current position """
        return self._pos

    def set_pos(self, pos):
        """ Set current position """
        self._pos = pos

    def draw(self):
        """ Draw element on the screen. """
        self._parent_surface.blit(self._surface, self._pos)

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
        widget.process_events(events)
        widget.draw()
    # >----- DRAW ------<
    pygame.display.update()
    clock.tick(30)
