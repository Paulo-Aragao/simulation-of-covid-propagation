from typing import List
# import numpy as np
import csv
class Agent:
    '''Unit of the simulation'''
    def __init__(self, pos, home):
        self.center = None
        self.home = home
        self.pos = pos

class Simulation:
    '''Standalone simulation'''
    def __init__(self, filepath):
        home_list, center_list = self._load_file()
        self._agents: List[Agent]  = self._create_agents(home_list)
        self._centers = self._create_centers(center_list)
        self._homes = home_list

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

    def get_agents(self):
        return [agent.pos for agent in self._agents]

    def get_centers(self):
        return self._centers

    def get_homes(self):
        return self._homes

    def next_step(self):
        pass
