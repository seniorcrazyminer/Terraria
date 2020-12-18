import gui
import files
import random

import math

player = [0, 0, 0, 0, 0, 20]
wrld = [0, 0, 0, 0]
scrn = [0, 0, 0, 0, 0]

currentSlot = 0

scale = 5

def updateVars():
  global wrld
  global scrn
  wrld = files.world()
  scrn = gui.screen()

def generateWorld(w, h, fileName):
  gnd = 50
  desert = [50, 100]
  for a in range(w):
    if (a > desert[0] and a < desert[1]):
      for b in range(0, gnd):
        blk = 0
        files.setBlock(a, b, blk)
      for b in range(gnd, h):
        blk = 3
        files.setBlock(a, b, blk)
    else:
      for b in range(0, gnd):
        blk = 0
        #if (random.randint(0, 100) < 10):
          #blk = random.randint(4, 7)
        files.setBlock(a, b, blk)
      files.setBlock(a, gnd, 1)
      for b in range(gnd + 1, h):
        blk = 2
        files.setBlock(a, b, blk)
    gnd = gnd + random.randint(-1, 1)
  files.saveWorld(fileName)

def addToInventory(item, qt):
  return 0

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
  updateVars()
  [xmin, ymin, xmax, ymax, p] = scrn
  [minx, miny, maxx, maxy] = wrld
  gui.drawBlockBehind(x - player[2], y - player[3], x, y)
  if (dx < 0):
    if (x > xmin and not checkBlock(x, y, dx, 0)):
      if (x < maxx - p and x > minx + p and xmin > minx):
        sx = dx
      x = x + dx
  if (dx > 0):
    if (x < xmax and not checkBlock(x, y, dx, 0)):
      if (x < maxx - p and x > minx + p and xmax < maxx):
        sx = dx
      x = x + dx
  if (dy < 0):
    if (y > ymin and not checkBlock(x, y, 0, dy)):
      if (y < maxy - p and y > miny + p and ymin > miny):
        sy = dy
      y = y + dy
  if (dy > 0):
    if (y < ymax and not checkBlock(x, y, 0, dy)):
      if (y < maxy - p and y > miny + p and ymax < maxy):
        sy = dy
      y = y + dy
  if (sx != 0 or sy != 0):
    gui.shift(sx, sy)
    player[2] = player[2] + sx
    player[3] = player[3] + sy
  updateVars()
  player[0] = x
  player[1] = y
  gui.drawPlayer(x - player[2], y - player[3])


def changeHealth(dh):
  global player
  player[5] = player[5] + dh
  gui.drawHealthBar()

def getHealth():
  global player
  return player[5]

def applyGravity():
  global player
  x = player[0]
  y = player[1]
  onG = onGround(x, y)
  if (not onG):
    movePlayer(0, 1)
    player[4] = player[4] + 1
  else:
    if (player[4] > 8):
      changeHealth(-(player[4] - 8))
    player[4] = 0

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
  x = math.floor(x / (scale*4))
  y = math.floor(y / (scale*4))
  gui.fillRect(4*scale*x, 4*scale*y, 4*scale, 4*scale, (255, 0, 0))
  useTool(x, y)


def useTool(tx, ty):
  global currentSlot
  global scrn
  currentTool = files.getInventoryItem(currentSlot)
  if (currentTool == 1):
    gui.fillRect(4*scale*tx, 4*scale*ty, 4*scale, 4*scale, (0, 255, 0))
    files.setBlock(tx + scrn[0], ty + scrn[1], 0)
    gui.drawBlock(tx, ty, tx + scrn[0], ty + scrn[1])


def setActiveSlot(n):
  return 0

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
      files.setBlock(a, b, 8)
      files.setBlock(a, b + 1, getNumWater(blk))
      if (a > scrn[0] and a < scrn[2]):
          if (b > scrn[1] and b < scrn[3]):
            gui.drawBlock(a - scrn[0], b - scrn[1], a, b)
            gui.drawBlock(a - scrn[0], b - scrn[1] + 1, a, b + 1)
  if (files.getBlockType(files.getBlock(a, b + 1)) == 1) and t == 1:
    l = getWaterNum(files.getBlock(a, b+1))
    if l == 8: l = 0
    if (l < 4):
      files.setBlock(a, b, getNumWater(blk - 1))
      files.setBlock(a, b + 1, getNumWater(l + 1))
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
      files.setBlock(a, b, getNumWater(blk - 1))
      files.setBlock(a-1, b, getNumWater(l + 1))
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
      files.setBlock(a, b, getNumWater(blk - 1))
      files.setBlock(a+1, b, getNumWater(l + 1))
      if (a > scrn[0] and a < scrn[2]):
          if (b > scrn[1] and b < scrn[3]):
            gui.drawBlock(a - scrn[0], b - scrn[1], a, b)
            gui.drawBlock(a - scrn[0]+1, b - scrn[1], a+1, b)



#do this when I want to respawn
def respawn():
  global player
  player = [0, 0, 0, 0]
  gui.respawn()
  