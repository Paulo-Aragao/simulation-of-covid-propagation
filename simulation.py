from typing import List
from random import choices
import numpy as np
import math
import csv
from scipy.stats import bernoulli
import random
class Agent:
    '''Unit of the simulation'''
    def __init__(self, pos, home):
        self.center = None
        self.home = home
        self.pos = pos
        self.speed = 5
        self.situation = "infected"

class Simulation:
    '''Standalone simulation'''
    def __init__(self, filepath,infection_probability,proximity,recovery_probability,gravitation_tick):
        home_list, center_list = self._load_file()
        self._agents: List[Agent]  = self._create_agents(home_list)
        self._centers = self._create_centers(center_list)
        self._homes = home_list
        agent = self._agents[0]
        #hyperparametres
        self._infection_probability = infection_probability
        self._proximity = proximity
        self._recovery_probability = recovery_probability
        self._gravitation_tick = gravitation_tick
    def _load_file(self):
        file_path = 'output/points.csv'
        home_list = []
        center_list = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if row[0] == 'home':
                    home_list.append((float(row[1]), float(row[2])))
                elif row[0] == 'center':
                    center_list.append((float(row[1]), float(row[2])))
        return home_list, center_list

    def _create_agents(self, home_list):
        return [Agent(home, home) for home in home_list]

    def _create_centers(self, center_list):
        return [center for center in center_list]

    def _euclidian_distance(self, a, b):
        return np.linalg.norm(np.array(a) - np.array(b))

    def _choose_center(self, agent):
        distances = [self._euclidian_distance(agent.pos, center) for center in self._centers]
        weights =  [min(distances)/distance * 100 for distance in distances]
        choosen = choices(distances, weights, k=1)
        idx = distances.index(choosen)
        return self._centers[idx]

    def get_agents(self):
        return self._agents
    
    def get_centers(self):
        return self._centers

    def get_homes(self):
        return self._homes

    def next_step(self):
        for agent in self._agents:
            agent.center = self._choose_center(agent)
            #recovery covid
            if agent.situation == "infected":
                if bernoulli.rvs(p=self._recovery_probability, size=1)[0] == 1:
                    agent.situation = "safe"

    def check_proximity_contamination(self,target_agent):
        for agent in self._agents:
            if agent.situation == "safe" and agent is not target_agent:
                if self._euclidian_distance(target_agent.pos,agent.pos) < self._proximity:
                    if bernoulli.rvs(p=self._infection_probability, size=1)[0] == 1:
                        agent.situation = "infected"
    def movement_agents(self):
        for agent in self._agents:
            #check proximity
            if agent.situation == "infected":
                self.check_proximity_contamination(agent)
            angle = self.get_angle_between_points(agent.pos, agent.center)
            agent.pos = self.move_coords_biased(agent.pos,angle,agent.speed)
    def move_coords_biased(self,coords, angle, radius):
        angle_biased = self.get_angle_biased(angle, 6)
        x = radius * np.cos( angle + angle_biased )
        y = radius * np.sin( angle + angle_biased )

        new_coord = (coords[0] + x, coords[1] + y)
        return new_coord

    def get_angle_biased(self,a, k):
        random_angle = np.random.uniform(-np.pi, np.pi)
        angle = (1/(2*np.pi*np.i0(k)))*(np.e**(k*(a-random_angle)))
        return angle

    def get_angle_between_points(self,p1, p2):
        return math.atan2(p2[1] - p1[1],p2[0] - p1[0])