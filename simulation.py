from typing import List
from random import choices
import numpy as np
import math
import csv
from scipy.stats import bernoulli
import random
import time
class Agent:
    '''Unit of the simulation'''
    def __init__(self, pos, home):
        self.center = None
        self.home = home
        self.pos = pos
        self.speed = 5
        situation = None
        if bernoulli.rvs(p=0.8, size=1)[0] == 1:
            situation = "susceptible"
        else:
            situation = "infected"
        self.situation = situation
        self.lockdown = False

class Simulation:
    '''Standalone simulation'''
    def __init__(self, filepath,infection_probability,proximity,recovery_probability,gravitation_tick,lockdown_strength):
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
        self._gravitation_step = 0
        self._lockdown_strength = lockdown_strength
        #file writer
        self._rows = []
        #timer meditor
        self._start_time = time.time()
        self._end_time = time.time()
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
        return [Agent(home, home) for home in home_list] + [Agent(home, home) for home in home_list] + [Agent(home, home) for home in home_list]

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

    def next_step_gravitation(self):
        self._gravitation_step += 1
        if self._gravitation_step < 4:
            for agent in self._agents:
                agent.center = self._choose_center(agent)
        elif self._gravitation_step < 9:
            for agent in self._agents:
                agent.center = agent.home
        else:
            self.next_day()

    def check_proximity_contamination(self,target_agent):
        for agent in self._agents:
            if agent.situation == "susceptible" and agent is not target_agent:
                if self._euclidian_distance(target_agent.pos,agent.pos) < self._proximity:
                    if bernoulli.rvs(p=self._infection_probability, size=1)[0] == 1:
                        agent.situation = "infected"
    def movement_agents(self):
        for agent in self._agents:
            #check proximity
            if agent.situation == "infected":
                self.check_proximity_contamination(agent)
            if not agent.lockdown:
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

    def next_day(self):
        self._gravitation_step = 0
        self._end_time = time.time()
        print(" vivos "+str(len(self._agents))+ " tempo "+ str((self._end_time - self._start_time)))
        self._start_time = time.time()
        for agent in self._agents:
            agent.center = self._choose_center(agent)
            situation = None
            if bernoulli.rvs(p=self._lockdown_strength, size=1)[0] == 1:
                agent.lockdown = True
            else:
                agent.lockdown = False
            #recovery covid
            if agent.situation == "infected":
                if bernoulli.rvs(p=self._recovery_probability, size=1)[0] == 1:
                    agent.situation = "susceptible"
                elif bernoulli.rvs(p=0.03, size=1)[0] == 1:
                    self._agents.remove(agent)
        susceptiple = sum([ 1 if agent.situation == "susceptible" else 0 for agent in self._agents])
        infected = sum([ 1 if agent.situation == "infected" else 0 for agent in self._agents])
        lock_rate = sum([ 1 if agent.lockdown else 0 for agent in self._agents])
        self._rows.append([len(self._agents),susceptiple,infected,lock_rate/len(self._agents)])
        print(infected)
    def _write_file(self):
        with open('output/simulation_ld_0.0_ir_0.5.csv', 'w') as f:
            # using csv.writer method from CSV package
            write = csv.writer(f)
            write.writerow(['POPULATION','SUSCEPTIPLES','INFECTEDS','LOCKDOWN_RATE'])
            write.writerows(self._rows)

    def run(self,days):
        days = days*300
        self._start_time = time.time()
        cooldown = 0
        time_ = 0
        current_day = 0
        while(current_day < days):
            time_ = time_ + 1
            if time_ > cooldown:
                cooldown = cooldown + self._gravitation_tick
                self.next_step_gravitation()
            self.movement_agents()
            current_day += 1
        self._write_file()
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  ~-~-~-~-~-~-~-~- SETUP ~-~-~-~-~-~-~-~-
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
if __name__ == '__main__':
    #hyperparamters of SARS-CoV-2
    infection_probability = 0.04
    proximity = 2
    gravitation_tick = 30
    recovery_probability = 0.1
    lockdown_strength = 0.8
    sim = Simulation('output/points.csv',infection_probability,proximity,recovery_probability,gravitation_tick,lockdown_strength)

    sim.next_step_gravitation()
    sim.run(30)