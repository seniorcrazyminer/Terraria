import files
import gui
import logic

import math as math

import sys

import pygame
from pygame.locals import *
from pygame import gfxdraw
from pygame import Surface
from pygame import key
from pygame import mouse

pygame.init()

keys = []

blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
buffer = pygame.Surface((width, height))
buffer1 = pygame.Surface((222, 24))
buffer2 = pygame.Surface((222, 48))



files.loadTextures("textures.txt", "itextures.txt")

gui.setGfxSurface(buffer)
gui.setToolSurface(buffer1)
gui.setHbSurface(buffer2)


files.openInventory("inventory.txt", "quantity.txt")
files.openWorld("world.txt")


gui.drawFullScreen()
gui.drawToolBar(0)


# Game loop.
while True:


    keys = pygame.key.get_pressed()  #checking pressed keys
    mouse = pygame.mouse.get_pressed()

    if mouse[0]:
      pos = pygame.mouse.get_pos()
      logic.mouseClick(pos[0], pos[1])
    
    if keys[pygame.K_RIGHT]:
      logic.movePlayer(1, 0)
    
    if keys[pygame.K_LEFT]:
      logic.movePlayer(-1, 0)
      #plyr.move(-1, 0)
    
    if keys[pygame.K_DOWN]:
      logic.movePlayer(0, 1)
      #plyr.move(0, 1)
    
    if keys[pygame.K_UP]:
      logic.movePlayer(0, -1)
      #plyr.move(0, -1)
    
    if keys[pygame.K_q]:
      files.saveWorld("world.txt")
        
    if keys[pygame.K_r]:
      logic.respawn()
        
    #if keys[pygame.K_a]:
        
    #if keys[pygame.K_d]:
        
    if keys[pygame.K_e]:
      logic.changeSlot(1)
        
    #if keys[pygame.K_q]:
        

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        

    # Update.
    logic.applyGravity()
    # Draw.
    screen.blit(buffer, (0, 0))
    screen.blit(buffer1, (0, 0))
    screen.blit(buffer2, (223, 0))


    pygame.display.flip()
    fpsClock.tick(fps)

