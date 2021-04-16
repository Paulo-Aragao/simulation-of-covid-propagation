import pygame 

pygame.init()

window = pygame.display.set_mode((800,600))
window_open = True
while window_open:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            window_open = False

pygame.quit()

