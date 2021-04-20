"""Module containing graphical widgets"""
import pygame
from pygame.math import Vector2 as Vec
import pygame_gui
from pygame_gui.windows.ui_file_dialog import UIFileDialog
import pygame_widgets

class Widget:
    """Generic component for graphical inteface"""

    def __init__(self, pos, size, parent_surface):
        self._style = {
            'size': Vec(size),
            'pos': Vec(pos)
        }
        self._state = {
            'active': True
        }
        self._parent_surface = parent_surface
        self._root_surface = pygame.Surface(size)

    def _update_surface(self):
        pass

    def listen(self, evts, time_delta):
        """listen events
        Args:
            evts (list): queue of pygame.event.Event
        """

    def draw(self):
        """Draw component on the screen."""
        self._parent_surface.blit(self._root_surface, self._style['pos'])

    def activate(self):
        """Activate  widget."""
        self._state['active'] = True

    def deactivate(self):
        """Deactivate  widget."""
        self._state['active'] = False

    def get_size(self) -> Vec:
        return self._style['size']

    def get_pos(self) -> Vec:
        return self._style['pos']

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(*self._style['pos'], *self._style['size'])


class StepperWidget(Widget):
    """GUI widget of a step bar element """

    def __init__(self, pos, size, parent_surface, steps = 10):

        super().__init__(pos, size, parent_surface)

        size = Vec(size)
        width = size.x - size.y*2
        full_step_width = width // steps
        full_step_width -= 0.5*full_step_width // steps
        margin = 0.25*full_step_width
        step_width = full_step_width - margin

        self._style.update({
            'step_width': step_width,
            'margin': margin,
            'active_step_color': (255, 255, 255),
            'inactive_step_color': (180, 180, 180),
            'steps': steps,
            'bg_color': (0, 0, 0)
        })

        self._surfaces = self._build_surfaces()
        self._rects = self._build_rects()

        self._state.update({
            'left_button_hover': False,
            'right_button_hover': False,
            'value': 5
        })

        self._draw_button('left')
        self._draw_button('right')

        self._update_surface()

    def _build_surfaces(self):
        style = self._style
        step_surface = pygame.Surface((style['step_width'], style['size'].y))
        active_step= step_surface.copy()
        inactive_step = step_surface.copy()

        active_step.fill(style['active_step_color'])
        inactive_step.fill(style['inactive_step_color'])

        right_button = pygame.Surface(style['size'].yy)
        left_button = pygame.Surface(style['size'].yy)

        return {
            'active_step': active_step, 'inactive_step': inactive_step,
            'right_button': right_button, 'left_button': left_button
        }

    def _build_rects(self):
        pos = self._style['pos']
        size = self._style['size'].yy
        steps = self._style['steps']
        right_button_pos = self._calc_step_pos(steps)

        left_button = pygame.Rect(pos, size)
        right_button = pygame.Rect(pos + right_button_pos, size)
        return {
            'left_button': left_button,
            'right_button': right_button
        }

    def _calc_step_pos(self, idx):
        step_width = self._style['step_width']
        margin = self._style['margin']
        return (idx*(step_width+margin)+self._style['size'].y+margin, 0)

    def _update_surface(self):
        self._root_surface.fill(self._style['bg_color'])

        self._root_surface.blit(self._surfaces['left_button'], (0, 0))

        value = self._state['value']

        for i in range(value):
            self._root_surface.blit(
                self._surfaces['active_step'], self._calc_step_pos(i))
        for i in range(value, self._style['steps']):
            self._root_surface.blit(
                self._surfaces['inactive_step'], self._calc_step_pos(i))

        self._root_surface.blit(
            self._surfaces['right_button'], self._calc_step_pos(i+1))

    def _draw_button(self, side):
        name = f'{side}_button'
        surface = self._surfaces[name]
        rect = self._rects[name]
        surface.fill(self._style['bg_color'])
        color = (self._style['active_step_color']
            if self._state[f'{name}_hover'] else self._style['inactive_step_color'])
        if side == 'left':
            pygame.draw.polygon(surface, color, [
                (0, (rect.h-1)//2), (rect.w-1, 0), (rect.w-1, rect.h-1)])
        elif side == 'right':
            pygame.draw.polygon(surface, color, [
                (0, 0), (0, rect.h-1), (rect.w-1, (rect.h-1) // 2)])

    def listen(self, evts, time_delta):
        """Process pygame events on the element
           Args:
               evts: list of pygame events.
        """
        pos = pygame.mouse.get_pos()

        state = self._state
        rects = self._rects
        if state['left_button_hover']:
            if not rects['left_button'].collidepoint(pos):
                state['left_button_hover'] = False
                self._draw_button('left')
        elif state['right_button_hover']:
            if not rects['right_button'].collidepoint(pos):
                state['right_button_hover']= False
                self._draw_button('right')
        else:
            if rects['left_button'].collidepoint(pos):
                state['left_button_hover'] = True
                self._draw_button('left')
            elif rects['right_button'].collidepoint(pos):
                state['right_button_hover'] = True
                self._draw_button('right')

        for evt in evts:
            if evt.type == pygame.MOUSEBUTTONUP:
                if state['left_button_hover']:
                    state['value'] -= state['value'] > 0
                elif state['right_button_hover']:
                    state['value'] += state['value'] < self._style['steps']
                break

        self._update_surface()


class ButtonArray(Widget):
    '''especialization of ButtonArray from pygame_widgets'''
    def __init__(self, pos, size, parent_surface, shape, **kargs):
        super().__init__(pos, size, parent_surface)
        self._widget = pygame_widgets.ButtonArray(
            parent_surface, *pos, *size, shape, **kargs)

    def listen(self, evts, _):
        self._widget.listen(evts)

    def draw(self):
        self._widget.draw()

class Button(Widget):
    '''especialization of ButtonArray from pygame_widgets'''
    def __init__(self, pos, size, parent_surface, **kargs):
        super().__init__(pos, size, parent_surface)
        self._widget = pygame_widgets.Button(
            parent_surface, *pos, *size, **kargs)

    def listen(self, evts, _):
        self._widget.listen(evts)

    def draw(self):
        self._widget.draw()


class FileExplorer(Widget):
    ''' file explorer widget '''

    def __init__(self, pos, size, parent_surface, on_select, on_cancel):
        super().__init__(pos, size, parent_surface)
        self._manager = pygame_gui.UIManager(parent_surface.get_size())
        self._widget = UIFileDialog(
            rect=pygame.Rect(pos, size), manager=self._manager)
        self._on_select = on_select
        self._on_cancel = on_cancel

    def listen(self, evts, time_delta):
        self._manager.update(time_delta)
        for event in evts:
            self._manager.process_events(event)
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == self._widget.ok_button:
                        self._on_select(self._widget.current_file_path)
                    elif event.ui_element in (
                        self._widget.close_window_button,
                        self._widget.cancel_button):
                        self._on_cancel()


    def draw(self):
        self._manager.draw_ui(self._parent_surface)
