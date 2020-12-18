import files
import logic

from pygame import gfxdraw

gfxSurface = 0
toolSurface = 0
hbSurface = 0
invSurface = 0
scrn = [0, 0, 32, 24, 10]

scale = 5

playerSprite = [[[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]], [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]], [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]], [[255, 255, 255], [255, 255, 255], [255, 255, 255], [255, 255, 255]]]

noTexture = [[[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]], [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]]

def screen():
  global scrn
  return scrn

def setScreen(xmin, ymin, xmax, ymax, padding):
  global scrn
  scrn = [xmin, ymin, xmax, ymax, padding]

def setGfxSurface(surf):
  global gfxSurface
  gfxSurface = surf

def setToolSurface(surf):
  global toolSurface
  toolSurface = surf

def setInvSurface(surf):
  global invSurface
  invSurface = surf

def setHbSurface(surf):
  global hbSurface
  hbSurface = surf
  hbSurface.set_colorkey((255,255,255))

def drawPlayer(x, y):
  drawSprite(x, y, playerSprite)

def drawBlockBehind(x, y, wx, wy):
  drawBlock(x, y, wx, wy)

def drawBlock(x, y, wx, wy):
  global gfxSurface
  global scale
  blk = files.getBlock(wx, wy)
  text = files.getTexture(blk) 
  for a in range(4):
    for b in range(4):
      col = text[a][b].strip(')(').split(', ')
      for i in range(3):
        col[i] = int(col[i])
      dx = (4*scale*x) + scale*b
      dy = (4*scale*y) + scale*a
      #gfxdraw.rectangle(gfxSurface, (dx, dy, scale, scale), col)
      filledRect(gfxSurface, dx, dy, scale, scale, col)

def drawSprite(x, y, sprite):
  global gfxSurface
  global scale
  for a in range(4):
    for b in range(4):
      col = sprite[a][b]
      for i in range(3):
        col[i] = int(col[i])
      dx = (4*scale*x) + scale*b
      dy = (4*scale*y) + scale*a
      #gfxdraw.rectangle(gfxSurface, (dx, dy, scale, scale), col)
      filledRect(gfxSurface, dx, dy, scale, scale, col)

def drawTool(x, y, num):
  global toolSurface
  text = files.getItemTexture(num)
  for a in range(5):
    for b in range(5):
      col = text[a][b].strip(')(').split(', ')
      for i in range(3):
        col[i] = int(col[i])
      filledRect(toolSurface, x + 4*b, y + 4*a, 4, 4, col)
 

def filledRect(surface, x, y, w, h, col):
  gfxdraw.filled_polygon(surface, ((x, y), (x+w, y), (x+w, y+h), (x, y+h)), col)

def fillRect(x, y, w, h, col):
  global gfxSurface
  gfxdraw.filled_polygon(gfxSurface, ((x, y), (x+w, y), (x+w, y+h), (x, y+h)), col)


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
  gfxSurface.scroll(-4*scale*dx, -4*scale*dy)
  
  if (dx == -1):
    renderXLine(0, scrn[0])
  if (dx == 1):
    renderXLine(scrn[2]-scrn[0] - 1, scrn[2])
  if (dy == -1):
    renderYLine(0, scrn[1])
  if (dy == 1):
    renderYLine(scrn[3]-scrn[1] - 1, scrn[3])
  

def renderXLine(x, wx):
  global scrn
  for b in range(0, scrn[3]-scrn[1]):
    drawBlock(x, b, wx, scrn[1] + b)

def renderXLineChecked(x, wx):
  global scrn
  for b in range(0, scrn[3]-scrn[1]):
    if (files.getBlock(wx, scrn[1] + b) == 0):
      drawBlock(x, b, wx, scrn[1] + b)

def renderYLine(y, wy):
  global scrn
  for a in range(0, scrn[2]-scrn[0]):
    drawBlock(a, y, scrn[0] + a, wy)

def clearXLine(x):
  global scrn
  for b in range(0, scrn[3]-scrn[1]):
    drawSprite(x, b, noTexture)

def clearYLine(y):
  global scrn
  for a in range(0, scrn[2]-scrn[0]):
    drawSprite(a, y, noTexture)

def drawFullScreen():
  for a in range(0, scrn[2]-scrn[0]):
    renderXLine(a, scrn[0] + a)

def checkAllAir():
  for a in range(0, scrn[2]-scrn[0]):
    renderXLineChecked(a, scrn[0] + a)

def drawInventory():
  global invSurface
  invSurface.fill((255, 255, 255))
  for a in range(6):
    for b in range(5):
      gfxdraw.rectangle(invSurface, (22 * a, 22*b, 24, 24), (0, 0, 0))

def drawToolBar(slot):
  global toolSurface
  toolSurface.fill((255, 255, 255))
  for a in range(10):
    col = (0, 0, 0)
    gfxdraw.rectangle(toolSurface, (22 * a, 0, 24, 24), col)
    drawTool(22*a + 1, 1, files.getInventoryItem(a))
  gfxdraw.rectangle(toolSurface, (22 * slot, 0, 24, 24), (255, 0, 0))
    

def drawHealthBar():
  global hbSurface
  health = logic.getHealth()
  hbSurface.fill((255, 255, 255))
  for a in range(10):
    for b in range(2):
      if ((10*b) + a <= health):
        filledRect(hbSurface, 22*a + 1, 22*b + 1, 20, 20, (255, 0, 0))



#do this when I want to respawn
def respawn():
  files.rePrepareWorld()