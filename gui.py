import files
import logic
import pygame
import random
from pygame import *
from pygame import gfxdraw
from pygame import font
from pygame import image

bgSurface = 0
gfxSurface = 0
toolSurface = 0
hbSurface = 0
invSurface = 0
scrn = [0, 0, 32, 24, 10]

scale = 5

bgcol = (120, 255, 241)
forestbg = pygame.image.load("Images/Forest_background_1.png")
desertbg = pygame.image.load("Images/Desert_background_1.png")
corruptbg = pygame.image.load("Images/Corruption_background_1.png")



lastBlockDrawn = 0


playerSprite = [[[255, 255, 255], [255, 255, 255], [255, 255, 255],
                 [255, 255, 255]],
                [[255, 255, 255], [255, 255, 255], [255, 255, 255],
                 [255, 255, 255]],
                [[255, 255, 255], [255, 255, 255], [255, 255, 255],
                 [255, 255, 255]],
                [[255, 255, 255], [255, 255, 255], [255, 255, 255],
                 [255, 255, 255]]]

noTexture = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
             [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
             [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
             [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]


def screen():
    global scrn
    return scrn


def setBgcol(col):
    global bgcol
    if (bgcol != col):
        bgcol = col
        drawFullScreen()


def updateSettings():
    global scale
    scale = files.getSetting(1)


def setScreen(xmin, ymin, xmax, ymax, padding):
    global scrn
    scrn = [xmin, ymin, xmax, ymax, padding]


def setGfxSurface(surf, bgsurf):
    global gfxSurface, bgSurface
    gfxSurface = surf
    bgSurface = bgsurf


def setToolSurface(surf):
    global toolSurface
    toolSurface = surf


def setInvSurface(surf):
    global invSurface
    invSurface = surf


def setHbSurface(surf):
    global hbSurface
    hbSurface = surf
    hbSurface.set_colorkey((255, 255, 255))


def drawPlayer(x, y):
    drawSprite(x, y, playerSprite)


def drawBlockBehind(x, y, wx, wy):
    drawBlock(x, y, wx, wy)

def getCoord(let, num):
  lets = "ABCDE"
  return num - 1, lets.find(let)

def getVariation(wx, wy, blk):
  top = files.getBlock(wx, wy - 1)
  bottom = files.getBlock(wx, wy + 1)
  left = files.getBlock(wx - 1, wy)
  right = files.getBlock(wx + 1, wy)
  topleft = files.getBlock(wx - 1, wy-1)
  topright = files.getBlock(wx + 1, wy-1)
  bottomleft = files.getBlock(wx - 1, wy+1)
  bottomright = files.getBlock(wx + 1, wy+1)

  if (blk != 2):
    if (left == blk and right == blk):
      if (bottom == 2):
        return getCoord("A", 14)
    if (left == blk and right == blk):
      if (top == 2):
        return getCoord("B", 14)
    if (top == blk and bottom == blk):
      if (right == 2):
        return getCoord("C", 14)
    if (top == blk and bottom == blk):
      if (left == 2):
        return getCoord("D", 14)

  # base zone blending
  if (top == blk and bottom == blk and left == blk and right == blk and bottomright == blk and topright == blk and topleft != blk and bottomleft != blk):
    return getCoord("A", 11)
  if (top == blk and bottom == blk and left == blk and right == blk and bottomleft == blk and topleft == blk and topright != blk and bottomright != blk):
    return getCoord("A", 12)
  if (top == blk and bottom == blk and left == blk and right == blk and topright == blk and topleft == blk and bottomleft == blk and bottomright == blk):
    return getCoord("B", 2)
  if (top == blk and bottom == blk and left == blk and right == blk and bottomright == blk and bottomleft == blk and topleft != blk and topright != blk):
    return getCoord("B", 7)
  if (top != blk and bottom != blk and left != blk and right != blk and bottomright != blk and topright != blk and topleft != blk and bottomleft != blk):
    return getCoord("D", 10)
  if (top == blk and bottom == blk and left == blk and right == blk and topright == blk and topleft == blk and bottomleft != blk and bottomright != blk):
    return getCoord("C", 7)

  if (top == blk and bottom == blk and right == blk):
    return getCoord("A", 1)
  if (left == blk and bottom == blk and right == blk):
    return getCoord("A", 2)
  if (top == blk and bottom == blk and left == blk):
    return getCoord("A", 5)
  if (left == blk and top == blk and right == blk):
    return getCoord("C", 2)
  
  if (top == blk and bottom == blk):
    return getCoord("A", 6)
  if (bottom == blk and right == blk):
    return getCoord("D", 1)
  if (bottom == blk and left == blk):
    return getCoord("D", 2)
  if (top == blk and right == blk):
    return getCoord("E", 1)
  if (top == blk and left == blk):
    return getCoord("E", 2)
  if (left == blk and right == blk):
    return getCoord("E", 7)

  if (bottom == blk):
    return getCoord("A", 7)
  if (right == blk):
    return getCoord("A", 10)
  if (left == blk):
    return getCoord("A", 13)
  if (top == blk):
    return getCoord("D", 7)
  
  
  return getCoord("D", 10)

def drawBlock(x, y, wx, wy):
    global gfxSurface
    global scale
    global bgcol, lastBlockDrawn, texts, block
    blk = files.getBlock(wx, wy)
    
    if (blk != 0):
      if (blk != lastBlockDrawn):
        block = pygame.image.load("Prime/Content/Images/Tiles_" + str(files.getTexture(blk)) + ".png")
      tx, ty = getVariation(wx, wy, blk)
      db = block.subsurface(((18 * tx), (18 * ty), 16, 16))
      filledRect(gfxSurface, 16 * x, 16 * y, 16, 16, (255, 255, 255, 0))
      gfxSurface.blit(db, (16 * x, 16 * y))
    else:
        filledRect(gfxSurface, 16 * x, 16 * y, 16, 16, (255, 255, 255, 0))


def drawSprite(x, y, sprite):
    global gfxSurface
    global scale
    global bgcol
    filledRect(gfxSurface, 16 * x, 16 * y, 16, 16, (255, 255, 255))


def drawTool(x, y, num):
    global toolSurface
    text = files.getItemTexture(num)
    for a in range(5):
        for b in range(5):
            col = text[a][b].strip(')(').split(', ')
            for i in range(3):
                col[i] = int(col[i])
            if (col[0] != -1):
                filledRect(toolSurface, x + 4 * b, y + 4 * a, 4, 4, col)


def drawInvTool(dx, dy, x, y):
    global invSurface
    text = files.getItemTexture(files.getInventoryItem(5 * x + y))
    for a in range(5):
        for b in range(5):
            col = text[a][b].strip(')(').split(', ')
            for i in range(3):
                col[i] = int(col[i])
            if (col[0] != -1):
                filledRect(invSurface, dx + 4 * b, dy + 4 * a, 4, 4, col)


def filledRect(surface, x, y, w, h, col):
    gfxdraw.filled_polygon(surface,
                           ((x, y), (x + w, y), (x + w, y + h), (x, y + h)),
                           col)


def fillRect(x, y, w, h, col):
    global gfxSurface
    gfxdraw.filled_polygon(gfxSurface,
                           ((x, y), (x + w, y), (x + w, y + h), (x, y + h)),
                           col)


def shift(dx, dy):
    global scrn
    global scale
    wrld = files.world()
    if (scrn[0] + dx > wrld[0] and scrn[2] + dx < wrld[2]):
        scrn[0] = scrn[0] + dx
        scrn[2] = scrn[2] + dx
    if (scrn[1] + dy > wrld[1] and scrn[3] + dy < wrld[3]):
        scrn[1] = scrn[1] + dy
        scrn[3] = scrn[3] + dy
    gfxSurface.scroll(-16 * dx, -16 * dy)

    if (dx == -1):
        renderXLine(0, scrn[0])
    if (dx == 1):
        renderXLine(scrn[2] - scrn[0] - 1, scrn[2])
    if (dy == -1):
        renderYLine(0, scrn[1])
    if (dy == 1):
        renderYLine(scrn[3] - scrn[1] - 1, scrn[3])


def renderXLine(x, wx):
    global scrn
    for b in range(0, scrn[3] - scrn[1]):
        drawBlock(x, b, wx, scrn[1] + b)


def renderXLineChecked(x, wx):
    global scrn
    for b in range(0, scrn[3] - scrn[1]):
        if (files.getBlock(wx, scrn[1] + b) == 0):
            drawBlock(x, b, wx, scrn[1] + b)


def renderYLine(y, wy):
    global scrn
    for a in range(0, scrn[2] - scrn[0]):
        drawBlock(a, y, scrn[0] + a, wy)


def clearXLine(x):
    global scrn
    for b in range(0, scrn[3] - scrn[1]):
        drawSprite(x, b, noTexture)


def clearYLine(y):
    global scrn
    for a in range(0, scrn[2] - scrn[0]):
        drawSprite(a, y, noTexture)


def drawFullScreen():
    for a in range(0, scrn[2] - scrn[0]):
        renderXLine(a, scrn[0] + a)


def updateBackground():
    global bgSurface, forestbg, desertbg, corruptbg, db
    bio = logic.checkBiome()
    if (bio == "forest"):
        bgSurface.blit(forestbg, (0, 0))
    elif (bio == "desert"):
        bgSurface.blit(desertbg, (0, 0))
    elif (bio == "corruption"):
        bgSurface.blit(corruptbg, (0, 0))


def checkAllAir():
    for a in range(0, scrn[2] - scrn[0]):
        renderXLineChecked(a, scrn[0] + a)


def drawInventory():
    global invSurface
    invSurface.fill((255, 255, 255))
    for a in range(6):
        for b in range(5):
            gfxdraw.rectangle(invSurface, (22 * a, 22 * b, 24, 24), (0, 0, 0))
            drawInvTool(22 * a + 1, 22 * b + 1, a, b)


def displaySlot(x, y):
    idx = 5 * x + y
    font = pygame.font.SysFont(None, 48)
    img = font.render(
        str(files.getInventoryItem(idx)) + ", " +
        str(files.getInventoryQuantity(idx)), True, (255, 0, 0))
    filledRect(invSurface, 200, 0, 640, 280, (255, 255, 255))
    invSurface.blit(img, (200, 0))


def drawToolBar(slot):
    global toolSurface
    toolSurface.fill((255, 255, 255))
    for a in range(10):
        col = (0, 0, 0)
        gfxdraw.rectangle(toolSurface, (22 * a, 0, 24, 24), col)
        drawTool(22 * a + 1, 1, files.getInventoryItem(a))
    gfxdraw.rectangle(toolSurface, (22 * slot, 0, 24, 24), (255, 0, 0))


def drawHealthBar():
    global hbSurface
    health = logic.getHealth()
    hbSurface.fill((255, 255, 255))
    for a in range(10):
        for b in range(2):
            if ((10 * b) + a <= health):
                filledRect(hbSurface, 22 * a + 1, 22 * b + 1, 20, 20,
                           (255, 0, 0))


#do this when I want to respawn
def respawn():
    files.rePrepareWorld()
