"""
Simulation of covid-19 transmission
"""
from functools import partial
from typing import List
import csv
import pygame
from pygame.locals import QUIT
from pygame.math import Vector2 as Vec
import pygame_gui

from components.poi import POI
# from components.widgets import FileExplorer, ButtonArray, Button
from components.camera import Camera, Follow
from simulation import Simulation

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- CLASS ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class SimulationPygame:
    ''' Simulation '''

    def __init__(self, surface: pygame.Surface,infection_probability,proximity,recovery_probability,gravitation_tick):
        self._screen = surface
        self._widgets = self._build_widgets()
        self._uimanager = pygame_gui.UIManager(surface.get_size())
        self._focus = Vec(surface.get_size()) // 2
        self._camera = Camera(self._focus, surface.get_size())
        self._camera.set_method(Follow(self._camera))
        home_poi = POI("home", (0, 0, 255))
        center_poi = POI("center", (255, 225, 255))
        agent_poi = POI("agent", (0, 0, 255))
        self._available_points = {
            home_poi.get_name(): home_poi,
            center_poi.get_name(): center_poi
        }
        self._simulation = Simulation('output/points.csv',infection_probability,proximity,recovery_probability,gravitation_tick)

    def _build_widgets(self):
        return []

    def _process_keys(self):
        keys = pygame.key.get_pressed()
        offset = {
            pygame.K_w: (0,-1), pygame.K_s: (0,1),
            pygame.K_a: (-1,0), pygame.K_d: (1,0)
        }
        speed_factor = (
            8 if keys[pygame.K_LCTRL] else 2 if keys[pygame.K_LSHIFT] else 4)
        for key in offset:
            if keys[key]:
                self._focus.update(self._focus+(Vec(offset[key])*speed_factor))

    def listen(self, events: List[pygame.event.Event], time_delta_):
        ''' Listen for events
        Args:
            events: queue of pygame events
        '''
        mouse_pos = Vec(pygame.mouse.get_pos())

        for widget in self._widgets:
            widget.listen(events, time_delta_)

        self._process_keys()

    def draw(self):
        ''' Draw components in the screen '''
        self._camera.scroll()
        for center in self._simulation.get_centers():
             screen.blit(self._available_points['center'].get_icon(), center + self._camera.offset)
        for home in self._simulation.get_homes():
            screen.blit(self._available_points['home'].get_icon(), home + self._camera.offset)
        for agent in self._simulation.get_agents():
            agent_surface = pygame.Surface((5, 5))
            if agent.situation == "safe":
                agent_surface.fill((0, 255, 0))
            else:
                agent_surface.fill((255, 0, 0))
            screen.blit(agent_surface, agent.pos + self._camera.offset)
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
#hyperparamters of SARS-CoV-2
infection_probability = 0.04
proximity = 0.8
recovery_probability = 0.1
gravitation_tick = 30
sim = SimulationPygame(screen,infection_probability,proximity,recovery_probability,gravitation_tick)

tick_day = 30
cooldown = 30
time = 0
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- MAIN LOOP ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
sim._simulation.next_step()
while True:
    time_delta = clock.tick(30)/1000.0
    evts = pygame.event.get()
    for evt in evts:
        if evt.type == QUIT:
            pygame.quit()
    screen.fill((0,0,0))
    # <----- DRAW AND LISTEN ------>
    #test moviment
    time = time + 1
    if time > cooldown:
        cooldown = cooldown + tick_day
        sim._simulation.next_step()
    sim._simulation.movement_agents()
    #
    sim.listen(evts, time_delta)
    sim.draw()
    # -----> DRAW AND LISTEN <-------
    pygame.display.update()
