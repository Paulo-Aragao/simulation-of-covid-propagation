import pygame
import math
import numpy as np
 
def move_coords(angle, radius, coords):
    theta = math.radians(angle)
    return coords[0] + radius * math.cos(theta), coords[1] + radius * math.sin(theta)

def move_coords_biased(coords, angle, radius):
    angle_biased = get_angle_biased(angle, 0.00001)
    x = radius * np.cos( angle + angle_biased )
    y = radius * np.sin( angle + angle_biased )
    
    new_coord = Point(coords.x + x, coords.y + y)
    return new_coord

def get_angle_biased(x, k):
    random_angle = np.random.uniform(-np.pi, np.pi)
    angle = (1/(2*np.pi*np.i0(k)))*(np.e**(k*(x-random_angle)))
    return angle

def get_angle_between_points(p1, p2):
        return math.atan2(p2.y - p1.y,p2.x - p1.x)

class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
def main():
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
     
    coords = Point(400,200)
    angle = 1
    rect = pygame.Rect(coords.x, coords.y, 20, 20)
    coords_center = Point(600, 400)
    rect_center = pygame.Rect(coords_center.x, coords_center.y, 20, 20)
    speed = 1
    radius = 1
    next_tick = 500
     
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
         
        ticks = pygame.time.get_ticks() 
        if ticks > next_tick:
            next_tick += speed
            angle = get_angle_between_points(coords, coords_center)
            # coords = move_coords(angle, 2, coords)
            
            coords = move_coords_biased(coords, angle, radius)
            rect.topleft = coords.x,coords.y
             
        screen.fill((0,0,30))
        screen.fill((0,150,0), rect)
        screen.fill((0,0,150), rect_center)

        pygame.display.flip()
        clock.tick(30)
     
    pygame.quit()
 
if __name__ == '__main__':
    main()
