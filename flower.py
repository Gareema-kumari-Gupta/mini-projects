import numpy as np 
import pygame , math

life = 0.0   #0 = seed, 1 =gone

def stem(life):
    h=ease(life / 0.4) * 470
    y = np.linspace(0,h,900)
    return 14 * np.sin(y/80+t),y

def bloom(life):
    for ring in range(4):
        open=smooth(life,0.42+ring*0.04)
        petals(ring*6+5,open*1.3)

def wilt(life):
    droop=smooth(life,0.75)
    colour=mix(PINK,GREY,droop)
    petals.fall(gravity=9.8*droop)

pygame.display.set_caption("life of a flower")
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    life += dt/29
    screen.fill((0,0,0))
    draw(stem(life),bloom(life),wilt(life))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()