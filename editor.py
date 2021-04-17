"""
Biblioteca gráfica para jogos e simulações.
"""
from functools import partial
from typing import List
import pygame
from pygame.locals import QUIT
from pygame_widgets import ButtonArray

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
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- DEFAULTS ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- VARIABLES ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Editor:
    ''' Simulation map editor '''

    def __init__(self, surface: pygame.Surface):
        self._icon_size = (5, 5)
        home_icon = self._make_icon((0, 255, 0))
        center_icon = self._make_icon((255, 255, 255))
        self._icons = [home_icon, center_icon, None]
        self._icon = center_icon
        self._icon_pos = None
        self._screen = surface
        self._widgets = self._build_widgets()
        self._points = []

    def _build_widgets(self):
        on_clicks = [partial(self.__class__.change_icon, self, i) for i in range(4)]
        button_array = ButtonArray(screen, 200, 10, 200, 20, (3, 1),
            border=0, texts=('casa', 'centro', 'nenhum'),
            onClicks = on_clicks
        )
        return [button_array]

    def _make_icon(self, color):
        icon = pygame.Surface(self._icon_size)
        icon.fill(color)
        return icon

    def change_icon(self, i):
        ''' Change the object is being placed
        Args:
            i (int): index of the object
        '''
        self._icon = self._icons[i]

    def listen(self, events: List[pygame.event.Event]):
        ''' Listen for events
        Args:
            events: queue of pygame events
        '''
        mouse_pos = pygame.mouse.get_pos()

        self._icon_pos = (
            mouse_pos[0]-self._icon_size[0]/2,
            mouse_pos[1]-self._icon_size[1]-2)

        for widget in self._widgets:
            widget.listen(events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and self._icon is not None:
                for point in self._points:
                    point_rect = pygame.Rect(*point[1], *self._icon_size)
                    new_point_rect = pygame.Rect(*self._icon_pos, *self._icon_size)
                    widgets_rects = [
                        pygame.Rect(w.getX(), w.getY(), w.getWidth(), w.getHeight())
                        for w in self._widgets]
                    collided_widget = sum([
                        1 for r in widgets_rects
                        if r.colliderect(new_point_rect)]) > 0
                    if point_rect.colliderect(new_point_rect) or collided_widget:
                        break
                else:
                    self._points.append((self._icon, self._icon_pos))
                break

    def draw(self):
        ''' Draw components in the screen '''
        for widget in self._widgets:
            widget.draw()
        for point in self._points:
            screen.blit(point[0], point[1])
        if self._icon is not None:
            screen.blit(self._icon, self._icon_pos)

editor = Editor(screen)

while True:
    evts = pygame.event.get()
    for evt in evts:
        if evt.type == QUIT:
            pygame.quit()
    screen.fill((0,0,0))
    editor.listen(evts)
    editor.draw()
    pygame.display.update()
    clock.tick(30)
