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
buffer1 = pygame.Surface((width, height))


files.loadTextures("textures.txt", "itextures.txt")
files.openWorld("world.txt")

gui.setGfxSurface(buffer)
gui.setGfxSurface1(buffer1)

dim = files.world()
w, h = dim[2], dim[3]
logic.generateWorld(w, h, "world.txt")

files.openInventory("inventory.txt", "quantity.txt")

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
      logic.movePlayer(0, -2)
      #plyr.move(0, -1)
    
    #if keys[pygame.K_w]:
        
    #if keys[pygame.K_s]:
        
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
    screen.blit(buffer1, (0, 0), (0, 0, 222, 24))


    pygame.display.flip()
    fpsClock.tick(fps)
