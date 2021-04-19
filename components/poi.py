import pygame
from pygame.math import Vector2 as Vec

class POI:
    ''' Store POI's of the map '''

    def __init__(self, name, color, size = None):
        self._size: Vec = Vec(5, 5) if size is None else Vec(size)
        self._color = color
        self._icon = self._make_icon()
        self._name = name
        self.pos = (0, 0)

    def _make_icon(self, ):
        icon = pygame.Surface(self._size)
        icon.fill(self._color)
        return icon

    def get_name(self):
        ''' get the name of the POI '''
        return self._name

    def get_size(self):
        ''' get the size of the POI '''
        return self._size

    def get_icon(self):
        ''' get POI icon '''
        return self._icon

    def copy(self):
        ''' copy point '''
        poi = self.__class__(self._name, self._color, self._size)
        poi.pos = self.pos
        return poi

    def __repr__(self):
        return f'{self._name}: ({self.pos}, {self._size})'
