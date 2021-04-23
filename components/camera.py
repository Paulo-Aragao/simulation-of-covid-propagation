# pylint: skip-file
''' simulate a big canvas '''
import pygame
from abc import ABC, abstractmethod
Vec = pygame.math.Vector2


class Canvas:
    ''' Generic canvas '''
    def __init__(self, size, screen, focus):
        self._focus = focus
        self.surface = pygame.Surface(size)
        self.surface.fill((255, 255, 255))
        self._offset_center = Vec(screen.get_size()) // 2
        self._screen = screen

    def draw(self):
        ''' Draw canvas on screen centering focus '''
        offset = Vec(
            x = self._offset_center.x - self._focus.x,
            y = self._offset_center.y - self._focus.y,
        )
        self._screen.blit(self.surface, offset)

class Camera:
    def __init__(self, focus, screen_size):
        self.focus = focus
        self.offset = Vec(0, 0)
        self._offset_center = Vec(screen_size) // 2

    def set_method(self, method):
        self._method = method

    def scroll(self):
        self._method.scroll()

class CamScroll(ABC):
    def __init__(self, camera):
        self._camera = camera

    @abstractmethod
    def scroll(self):
        pass

class Follow(CamScroll):
    def __init__(self, camera):
        CamScroll.__init__(self, camera)

    def scroll(self):
        offset = Vec(
            x = self._camera._offset_center.x - self._camera.focus.x,
            y = self._camera._offset_center.y - self._camera.focus.y,
        )
        self._camera.offset = offset
'''
class Border(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)

    def scroll(self):
        self.camera.offset_float.x += (self.player.rect.x - self.camera.offset_float.x + self.camera.CONST.x)
        self.camera.offset_float.y += (self.player.rect.y - self.camera.offset_float.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float.x), int(self.camera.offset_float.y)
        self.camera.offset.x = max(self.player.left_border, self.camera.offset.x)
        self.camera.offset.x = min(self.camera.offset.x, self.player.right_border - self.camera.DISPLAY_W)

class Auto(CamScroll):
    def __init__(self,camera,player):
        CamScroll.__init__(self,camera,player)

    def scroll(self):
        self.camera.offset.x += 1

'''







