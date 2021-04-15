import gui
import files
import random

import math

import pygame
from pygame import gfxdraw
import pygame
from pygame.locals import *
from pygame import gfxdraw
from pygame import Surface
from pygame import key
from pygame import mouse
from pygame import font

pbuf = pygame.Surface((640, 480))

fps = 60
fpsClock = pygame.time.Clock()


desert = [50, 100]
corruption = [100, 200]

fileName = ""

player = [0, 0, 20]
wrld = [0, 0, 0, 0]
scrn = [0, 0, 0, 0, 0]
fallPath = [0, 0]
fallPathActive = False

screen = 0

currentSlot = 0

scale = 5

width = 0
height = 0

def updateVars():
  global wrld
  global scrn
  wrld = files.world()
  scrn = gui.screen()

def setScreen(scrn):
  global screen
  screen = scrn

def updateSettings():
  global scale
  scale = files.getSetting(1)

def filledRect(surface, x, y, w, h, col):
  gfxdraw.filled_polygon(surface, ((x, y), (x+w, y), (x+w, y+h), (x, y+h)), col)

def progress(percent, line):
  gfxdraw.line(pbuf, 0, 0 * line, 640, 0, (0, 0, 0))
  gfxdraw.line(pbuf, 0, 0 * line, math.floor(percent*640), 0, (0, 0, 255))
  screen.blit(pbuf, (0, 50 * line + 30))
  pygame.display.flip()

def title(title, line):
  filledRect(screen, 0, 50*line, 640, 20, (0, 0, 0))
  font = pygame.font.SysFont(None, 24)
  img = font.render(title, True, (255, 255, 255))
  screen.blit(img, (0, 50*line))
  pygame.display.flip()

def text(x, y, string, size, color):
  font = pygame.font.SysFont(None, size)
  img = font.render(string, True, color)
  screen.blit(img, (x, y))
  pygame.display.flip()

def worldsMenu():
  global fpsClock, fps
  list = files.listAllWorlds()
  list.append("nw")
  print(list)
  for i in range(len(list)):
    filledRect(screen, 5, 30*i+5, 630, 24, (128, 128, 128))
    text(10, 30*i+7, list[i], 24, (255, 255, 255))
  while True:
    mouse = pygame.mouse.get_pressed()
    if mouse[0]:
      pos = pygame.mouse.get_pos()
      for i in range(len(list)):
        if (pointInRect(pos, (5, 30*i+5, 630, 24))):
          print(list[i])
          if (list[i] == "nw"):
            generateWorld()
          else:
            playWorld(list[i])
          return
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
    fpsClock.tick(fps)

def pointInRect(point,rect):
    x1, y1, w, h = rect
    x2, y2 = x1+w, y1+h
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False

def playWorld(name):
  global fileName
  fileName = "Worlds/" +name + ".wrld"
  files.prepareWorld(fileName)


def randomString(length):
  lets = "abcdefghijklmnopqrstuvwxyz"
  string = ""
  for i in range(length):
    string = string + lets[random.randint(0, 25)]
  return string

def generateWorld():
  global width, height, desert, corruption, fileName
  filledRect(screen, 0, 0, 640, 480, (0, 0, 0))
  width = files.getSetting(5)
  height = files.getSetting(6)
  fileName = "Worlds/" + randomString(8) + ".wrld"
  files.setDim(width, height)
  gnd = 50
  desert = [50, 100]
  corruption = [100, 200]
  dGnd = 0
  pgnd = [gnd] * width
  title("Generating", 0)
  title("Terraforming", 1)
  for a in range(width):
    progress(a/width, 1)
    if (a > desert[0] and a < desert[1]):
      for b in range(0, gnd):
        blk = 0
        files.setBlock(a, b, blk)
      for b in range(gnd, height):
        blk = 3
        files.setBlock(a, b, blk)
    elif (a > corruption[0] and a < corruption[1]):
      for b in range(0, gnd):
        blk = 0
        files.setBlock(a, b, blk)
      files.setBlock(a, gnd, 5)
      for b in range(gnd+1, height):
        blk = 2
        files.setBlock(a, b, blk)
    else:
      for b in range(0, gnd):
        blk = 0
        #if (random.randint(0, 100) < 10):
          #blk = random.randint(4, 7)
        files.setBlock(a, b, blk)
      files.setBlock(a, gnd, 1)
      for b in range(gnd + 1, height):
        blk = 2
        files.setBlock(a, b, blk)
    dGnd = dGnd + random.randint(-1, 1)
    if (dGnd < -1):
      dGnd = -1
    if (dGnd > 1):
      dGnd = 1
    pgnd[a] = gnd
    gnd = gnd + dGnd
  spwnx = random.randint(files.getSetting(4) + 1, files.getSetting(4) + 51)
  spwny = 0
  while (files.getBlockType(files.getBlock(spwnx, spwny)) != 2):
    spwny = spwny + 1
  progress(.3, 0)
  title("Generating Landmarks", 1)
  
  for i in range(random.randint(15, 35)):
    chasmRadius = random.randint(3, 5)
    a = random.randint(corruption[0] + chasmRadius + 2, corruption[1] - chasmRadius - 2)
    curRadius = chasmRadius
    chasmDepth = random.randint(25, 50)
    for y in range(pgnd[a], chasmDepth):
      for x in range(a - curRadius, a + curRadius):
        files.setBlock(x, y, 0)
      files.setBlock(a - curRadius, y, 4)
      files.setBlock(a + curRadius, y, 4)
      curRadius = curRadius + random.randint(-1, 1)
      if (curRadius < chasmRadius - 2):
            curRadius = chasmRadius - 2
      if (curRadius > chasmRadius + 2):
            curRadius = chasmRadius + 2
  
  for i in range(random.randint(100, 200)):
    x = random.randint(5, width - 5)
    y = random.randint(5, height-5)
    w = random.randint(3, 5)
    h = random.randint(3, 5)
    for a in range(-w, w+1):
      for b in range(-h, h+1):
        files.setBlock(x+a, y+b, 6)
  progress(.6, 0)
  progress(1, 0)
  files.setSpawn(spwnx, spwny)
  files.saveWorld(fileName)
  files.prepareWorld(fileName)

# 1 4 7
# 2 5 8
# 3 6 9
def replace():
  title("Smoothing", 1)
  title("Smoothing World 1 / 2", 2)
  replaceRule([[-1, 2, -1], [0, (-1, 0), -1], [-1, 0, 2]], [[-1, -1, -1], [-1, (-1, 1), (-1, 0)], [-1, -1, -1]])
  progress(.5, 1)
  title("Smoothing World 2 / 2", 2)
  replaceRule([[-1, 0, 2], [0, (-1, 0), -1], [-1, 2, -1]], [[-1, -1, -1], [-1, (-1, 2), (-1, 0)], [-1, -1, -1]])
  progress(1, 1)

def replaceRule(rule, replace):
  global width, height
  print(rule)
  print(replace)
  for x in range(width):
    progress((x / width), 2)
    for y in range(height):
      attemptReplace(x, y, rule, replace)

def attemptReplace(x, y, rule, replace):
  global width, height
  tot = 0
  target = 0
  for a in range(-1, 2):
    for b in range(-1, 2):
      target = target + 1
      if (x + a >= 0 and x + a <= width-1 and y + b >= 0 and y + b <= height-1):
        if (type(rule[a+1][b+1]) is int):
          if (rule[a+1][b+1] == -1):
            tot = tot + 1
          elif (getBlockType(x+a, y+b) == rule[a+1][b+1]):
            tot = tot + 1
        else:
          if (rule[a+1][b+1][0] == -1 and rule[a+1][b+1][1] == getBlock(x + a, y + b)):
            tot = tot + 1
          elif (files.getBlock(x + a, y + b) == rule[a + 1][b + 1]):
            tot = tot + 1
      else:
        tot = tot + 1
      if (tot != target):
        return
  if (tot == 9):
    for a in range(-1, 1):
      for b in range(-1, 1):
        if (x + a >= 0 and x + a <= width-1 and y + b >= 0 and y + b <= height-1):
          if (replace[a + 1][b + 1] != -1):
            if (replace[a+1][b+1][0] == -1):
              files.setBlock(x+a, y+b, (files.getBlock(x+a, y+b), replace[a+1][b+1][1]))
            else:
              files.setBlock(x+a, y+b, replace[a+1][b+1])

def getBiome(x, y):
  global desert, corruption
  if (x >= desert[0] and x <= desert[1]):
    return "desert"
  elif (x >= corruption[0] and x <= corruption[1]):
    return "corruption"
  else:
    return "Forest"

def addToInventory(item):
  for a in range(25):
    if (files.getInventoryItem(a) == int(item[0])):
      files.setInventoryItem(a, item[0], files.getInventoryQuantity(a) + int(item[1]))
      return
  for a in range(25):
    if (files.getInventoryItem(a) == 0):
      files.setInventoryItem(a, item[0], int(item[1]))
      return

def findInInventory(item):
  return 0

def takeFromInventory(item, qt):
  return 0

def getNextOpenSlot():
  return 0

def fall():
  return 0

def checkFallDamage():
  return 0


def movePlayer(dx, dy):
  global player
  global scrn
  global wrld
  x = player[0]
  y = player[1]
  sx, sy = 0, 0
  prevx, prevy = x, y
  updateVars()
  [xmin, ymin, xmax, ymax, p] = scrn
  [minx, miny, maxx, maxy] = wrld
  if (dy < 0):
    if (y > ymin and not checkBlock(x, y, 0, dy) and checkBlock(x, y, 0, 1)):
      if (y < maxy - p and y > miny + p and ymin > miny):
        sy = dy
      y = y + dy
  if (dy > 0):
    if (y < ymax and not checkBlock(x, y, 0, dy)):
      if (y < maxy - p and y > miny + p and ymax < maxy):
        sy = dy
      y = y + dy
  if (dx < 0):
    if (getBlock(x+dx, y) == 1):
      if (y < maxy - p and y > miny + p and ymin > miny):
        sy = sy - 1
      y = y - 1
    if (x > xmin and not checkBlock(x, y, dx, 0)):
      if (x < maxx - p and x > minx + p and xmin > minx):
        sx = dx
      x = x + dx
      
  if (dx > 0):
    if (getBlock(x+dx, y) == 2):
      if (y < maxy - p and y > miny + p and ymin > miny):
        sy = sy - 1
      y = y - 1
    if (x < xmax and not checkBlock(x, y, dx, 0)):
      if (x < maxx - p and x > minx + p and xmax < maxx):
        sx = dx
      x = x + dx
      
  
  if (sx != 0 or sy != 0):
    gui.shift(sx, sy)
  updateVars()
  player[0] = x
  player[1] = y
  gui.drawBlockBehind(prevx - scrn[0], prevy - scrn[1], prevx, prevy)
  gui.drawPlayer(x - scrn[0], y - scrn[1])

def setPlayerPos(x, y):
  global player
  global scrn
  gui.drawBlockBehind(x - scrn[0], y - scrn[1], x, y)
  player[0] = x
  player[1] = y
  gui.drawPlayer(x - scrn[0], y - scrn[1])


def changeHealth(dh):
  global player
  player[2] = player[2] + dh
  gui.drawHealthBar()

def getHealth():
  global player
  return player[2]

def applyGravity():
  global player
  global fallPath
  global fallPathActive
  x = player[0]
  y = player[1]
  dy = 0
  onG = onGround(x, y)
  if (not onG):
    if (not fallPathActive):
      fallPath = [player[0], player[1]]
      fallPathActive = True
    if (fallPathActive):
      dy = 1
  else:
    if (fallPathActive):
      fallPathActive = False
      if (player[1] - fallPath[1] > 8):
        changeHealth(-(abs(player[1] - fallPath[1]) - 8))
      fallPath = [0, 0]
  return dy

def onGround(x, y):
  updateVars()
  return checkBlock(x, y, 0, 1)

def checkBlock(x, y, dx, dy):
  updateVars()
  b  = files.getBlockType(files.getBlock(x + dx, y + dy))
  if (b < 2):
    return False
  else:
    return True

def getBlock(x, y):
  return files.getBlock(x, y)

def getBlockType(x, y):
  return files.getBlockType(files.getBlock(x, y))

def changeSlot(ds):
  global currentSlot
  currentSlot = currentSlot + ds
  if (currentSlot == 10):
    currentSlot = 0
  if (currentSlot == -1):
    currentSlot = 9
  gui.drawToolBar(currentSlot)

def mouseClick(x, y):
  global scale
  x = math.floor(x / (16))
  y = math.floor(y / (16))
  useTool(x, y)

def mouseClickInventory(x, y):
  x = math.floor(x / 24)
  y = math.floor(y / 24)
  if (x < 6 and y < 5):
    gui.displaySlot(x, y)

def useTool(tx, ty):
  global currentSlot
  global scrn
  currentTool = files.getInventoryItem(currentSlot)
  if (currentTool == 4):
    addToInventory(files.getDrop(getBlock(tx + scrn[0], ty + scrn[1])))
    files.setBlock(tx + scrn[0], ty + scrn[1], 0)
    updateBlock(tx, ty)
  elif (currentTool == 1):
    files.setBlock(tx + scrn[0], ty + scrn[1], 2)
    updateBlock(tx, ty)
  elif (currentTool == 2):
    files.setBlock(tx + scrn[0], ty + scrn[1], 3)
    updateBlock(tx, ty)

def updateBlock(x, y):
  for a in range(-1, 2):
    for b in range(-1, 2):
      gui.drawBlock(x + a, y + b, x + a + scrn[0], y + b + scrn[1])

def setActiveSlot(n):
  global currentSlot
  currentSlot = n
  gui.drawToolBar(currentSlot)

def settleWater():
  for i in range(10):
    settleWaterOnce()

def getWaterNum(n):
  return (4 - (n - 4))

def getNumWater(n):
  return (4 + (4 - n))

def settleWaterOnce():
  global wrld
  global scrn
  updateVars()
  for a in range(wrld[2]):
    for b in range(wrld[3]):        
        if (b < wrld[3]):
          attemptMoveDown(a, b)
        if (a > wrld[0]):
          attemptMoveLeft(a, b)
        if (a < wrld[2] - 1):
          attemptMoveRight(a, b)

def getWater(a, b):
  blk = files.getBlock(a, b)
  t = files.getBlockType(blk)
  blk = getWaterNum(blk)
  return blk, t

def attemptMoveDown(a, b):
  global scrn
  blk, t = getWater(a, b)
  if (files.getBlockType(files.getBlock(a, b + 1)) == 0) and t == 1:
    l = getWaterNum(files.getBlock(a, b+1))
    if l == 8: l = 0
    if (l < 4):
      files.setBlock(a, b, (8, 0))
      files.setBlock(a, b + 1, (getNumWater(blk), 0))
      if (a > scrn[0] and a < scrn[2]):
          if (b > scrn[1] and b < scrn[3]):
            gui.drawBlock(a - scrn[0], b - scrn[1], a, b)
            gui.drawBlock(a - scrn[0], b - scrn[1] + 1, a, b + 1)
  if (files.getBlockType(files.getBlock(a, b + 1)) == 1) and t == 1:
    l = getWaterNum(files.getBlock(a, b+1))
    if l == 8: l = 0
    if (l < 4):
      files.setBlock(a, b, (getNumWater(blk - 1), 0))
      files.setBlock(a, b + 1, (getNumWater(l + 1), 0))
      if (a > scrn[0] and a < scrn[2]):
          if (b > scrn[1] and b < scrn[3]):
            gui.drawBlock(a - scrn[0], b - scrn[1], a, b)
            gui.drawBlock(a - scrn[0], b - scrn[1] + 1, a, b + 1)

def attemptMoveLeft(a, b):
  global scrn
  blk, t = getWater(a, b)
  if (files.getBlockType(files.getBlock(a-1, b)) != 2) and t == 1:
    l = getWaterNum(files.getBlock(a-1, b))
    if l == 8: l = 0
    if (l < 4):
      files.setBlock(a, b, (getNumWater(blk - 1), 0))
      files.setBlock(a-1, b, (getNumWater(l + 1), 0))
      if (a > scrn[0] and a < scrn[2]):
          if (b > scrn[1] and b < scrn[3]):
            gui.drawBlock(a - scrn[0], b - scrn[1], a, b)
            gui.drawBlock(a - scrn[0]-1, b - scrn[1], a-1, b)

def attemptMoveRight(a, b):
  global scrn
  blk, t = getWater(a, b)
  if (files.getBlockType(files.getBlock(a+1, b)) != 2) and t == 1:
    l = getWaterNum(files.getBlock(a+1, b))
    if l == 8: l = 0
    if (l < 4):
      files.setBlock(a, b, (getNumWater(blk - 1), 0))
      files.setBlock(a+1, b, (getNumWater(l + 1), 0))
      if (a > scrn[0] and a < scrn[2]):
          if (b > scrn[1] and b < scrn[3]):
            gui.drawBlock(a - scrn[0], b - scrn[1], a, b)
            gui.drawBlock(a - scrn[0]+1, b - scrn[1], a+1, b)


# things to do constantly
def tick():
  global player
  if (player[2] <= 0):
    return "dead"

def checkBiome():
  global desert, corruption, player
  if (player[0] >= desert[0] and player[0] <= desert[1]):
    return "desert"
  elif (player[0] >= corruption[0] and player[0] <= corruption[1]):
    return "corruption"
  else:
    return "forest"

def nextTick(code):
  if (code == "dead"):
    respawn()

def saveWorld():
  global fileName
  files.saveWorld(fileName)

#do this when I want to respawn
def respawn():
  global player
  player = [0, 0, 20]
  gui.respawn()