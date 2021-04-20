"""
Biblioteca gráfica para jogos e simulações.
"""
from functools import partial
from typing import List
import csv
import pygame
from pygame.locals import QUIT
from pygame.math import Vector2 as Vec
# from pygame_widgets import Button
import pygame_gui
# from pygame_gui.windows.ui_file_dialog import UIFileDialog
# from pygame_gui.elements.ui_button import UIButton

from components.poi import POI
from components.widgets import FileExplorer, ButtonArray, Button
# from helpers.util import prompt_file

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- CLASS ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class EditorState:
    ''' Current state of editor '''

    def __init__(self):
        home_poi = POI("home", (0, 255, 0))
        center_poi = POI("center", (255, 225, 255))
        self._available_points = {
            home_poi.get_name(): home_poi,
            center_poi.get_name(): center_poi
        }
        self._points: List[POI] = []
        self._current_point: POI = None
        self.last_pressed_mouse = [False, False, False]

    def add_point(self, point):
        ''' add point '''
        self._points.append(point.copy())

    def remove_point(self, point):
        ''' remove point '''
        self._points.remove(point)

    def get_points(self) -> List[POI]:
        ''' get all points '''
        return self._points

    def get_poi(self):
        ''' get current not yet added POI '''
        return self._current_point

    def set_poi(self, poi_name):
        ''' set current not yet added POI '''
        mouse_pos = Vec(pygame.mouse.get_pos())
        if poi_name not in self._available_points:
            self._current_point = None
        else:
            self._current_point = self._available_points[poi_name]
            self.update_poi_pos(mouse_pos)

    def update_poi_pos(self, mouse_pos):
        ''' update current not yet added POI position'''
        if self._current_point is None:
            return
        self._current_point.pos = (
            mouse_pos.x-self._current_point.get_size().x/2,
            mouse_pos.y-self._current_point.get_size().y-2
        )

    def get_poi_names(self):
        ''' get available point names '''
        return list(self._available_points.keys())

    def save(self):
        ''' save state to files '''
        with open('output/points.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(('t', 'x', 'y'))
            writer.writerows(([point.get_name()] + list(point.pos)
                for point in self._points))

    def load(self, file_path):
        ''' load points from file '''
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                point = self._available_points[row[0]].copy()
                point.pos = Vec(*[float(n) for n in row[1:]])
                self._points.append(point)

class Editor:
    ''' Simulation map editor '''

    def __init__(self, surface: pygame.Surface):
        self._screen = surface
        self._state = EditorState()
        self._widgets = self._build_widgets()
        self._uimanager = pygame_gui.UIManager(surface.get_size())

    def _build_widgets(self):
        names = self._state.get_poi_names()
        on_clicks = [partial(
            self._state.set_poi, name)
            for name in names + [None]]
        button_array = ButtonArray((100, 10), (200, 20), self._screen,
           (len(names)+1, 1), border=0, texts=(names+['nenhum']),
           onClicks=on_clicks)
        button_save = Button((310, 10), (60, 20), screen, text='salvar',
            onClick=self._state.save)
        button_load = Button((380, 10), (60, 20), screen, text='carregar',
            onClick=self._ask_for_file)
        return [button_array, button_save, button_load]

    def _ask_for_file(self):
        self._state.set_poi(None)
        file_explorer = FileExplorer((0,0), (300, 300), self._screen,
            on_select=self._load_file, on_cancel=self._cancel_load)
        self._widgets.append(file_explorer)

    def _load_file(self, file_path):
        self._state.load(file_path)
        del self._widgets[-1]

    def _cancel_load(self):
        del self._widgets[-1]

    def _process_click(self, mouse_pos) -> bool:
        [_, _, right] = self._state.last_pressed_mouse
        points = self._state.get_points()
        poi = self._state.get_poi()

        if poi is None:
            if not right:
                return True
            for point in points:
                point_rect = pygame.Rect(point.pos, point.get_size())
                if point_rect.collidepoint(mouse_pos):
                    self._state.remove_point(point)
        else:
            new_point_rect = pygame.Rect(poi.pos, poi.get_size())
            for point in points:
                point_rect = pygame.Rect(point.pos, poi.get_size())
                collided_point = point_rect.colliderect(new_point_rect)
                if collided_point:
                    if right:
                        self._state.remove_point(point)
                    break
            else:
                if right:
                    return True
                new_point_rect = pygame.Rect(poi.pos, poi.get_size())
                widgets_rects = [
                    w.get_rect()
                    for w in self._widgets]
                collided_widget = sum([
                    1 for r in widgets_rects
                    if r.colliderect(new_point_rect)]) > 0
                if not collided_widget:
                    self._state.add_point(poi)
            return True
        return False


    def listen(self, events: List[pygame.event.Event], time_delta_):
        ''' Listen for events
        Args:
            events: queue of pygame events
        '''
        mouse_pos = Vec(pygame.mouse.get_pos())
        self._state.update_poi_pos(mouse_pos)

        for widget in self._widgets:
            widget.listen(events, time_delta_)

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self._process_click(mouse_pos):
                    break
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._state.last_pressed_mouse = pygame.mouse.get_pressed()
                break

    def draw(self):
        ''' Draw components in the screen '''
        poi = self._state.get_poi()
        for point in self._state.get_points():
            screen.blit(point.get_icon(), point.pos)
        if poi is not None:
            screen.blit(poi.get_icon(), poi.pos)
        for widget in self._widgets:
            widget.draw()

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- SETUP ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SCREEN_SIZE = (600, 600)
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Teste')
clock = pygame.time.Clock()
editor = Editor(screen)
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- MAIN LOOP ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
while True:
    time_delta = clock.tick(30)/1000.0
    evts = pygame.event.get()
    for evt in evts:
        if evt.type == QUIT:
            pygame.quit()
    screen.fill((0,0,0))
    # <----- DRAW AND LISTEN ------>
    editor.listen(evts, time_delta)
    editor.draw()
    # -----> DRAW AND LISTEN <-------
    pygame.display.update()
