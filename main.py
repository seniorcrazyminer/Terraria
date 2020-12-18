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

keys = pygame.key.get_pressed()

blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)

inventoryOpen = False

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))
buffer = pygame.Surface((width, height))
buffer1 = pygame.Surface((222, 24))
buffer2 = pygame.Surface((222, 48))
buffer3 = pygame.Surface((width, height))


mainBuffer = pygame.Surface((width, height))


files.loadTextures("textures.txt", "itextures.txt")

gui.setGfxSurface(buffer)
gui.setToolSurface(buffer1)
gui.setHbSurface(buffer2)
gui.setInvSurface(buffer3)



files.openInventory("inventory.txt", "quantity.txt")
logic.generateWorld(500, 500, "world.txt")
files.prepareWorld("world.txt")


# Game loop.
while True:


    keys = pygame.key.get_pressed()  #checking pressed keys
    
    mouse = pygame.mouse.get_pressed()

    dx = 0
    dy = 0

    if mouse[0]:
      pos = pygame.mouse.get_pos()
      if inventoryOpen:
        logic.mouseClickInventory(pos[0], pos[1])
      else:
        logic.mouseClick(pos[0], pos[1])
    
    if keys[pygame.K_RIGHT]:
      dx = dx + 1
    
    if keys[pygame.K_LEFT]:
      dx = dx - 1
      #plyr.move(-1, 0)
    
    if keys[pygame.K_DOWN]:
      dy = dy + 1
      #plyr.move(0, 1)
    
    if keys[pygame.K_UP]:
      dy = dy - 1
      #plyr.move(0, -1)
    
    if keys[pygame.K_q]:
      files.saveWorld("world.txt")
        
    if keys[pygame.K_r]:
      logic.respawn()
        
    if keys[pygame.K_c]:
      gui.checkAllAir()
        
    #if keys[pygame.K_d]:
        
    if keys[pygame.K_e]:
      inventoryOpen = True
      gui.drawInventory()
    
    if keys[pygame.K_t]:
      inventoryOpen = False
        
    #if keys[pygame.K_q]:
        

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        

    # Update.
    dy = dy + logic.applyGravity()
    logic.movePlayer(dx, dy)
    # Draw.
    
    if (inventoryOpen):
      mainBuffer.blit(buffer3, (0, 0))
    else:
      mainBuffer.blit(buffer, (0, 0))
      mainBuffer.blit(buffer1, (0, 0))
      mainBuffer.blit(buffer2, (223, 0))


    screen.blit(mainBuffer, (0, 0))
    pygame.display.flip()
    fpsClock.tick(fps)

