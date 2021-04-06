import logic
import gui

dim = [0, 0]
spawn = [0, 0]
textures = []
iTextures = []
tempWorld = []

inv = []
qty = []

def world():
  return [0, 0, dim[0], dim[1]]

def inventory():
  global inv
  return inv

def quantity():
  global qty
  return qty

def split(word): 
    return [char for char in word]

def setSpawn(x, y):
  global spawn
  spawn = [x, y]

def setDim(x, y):
  global dim
  global tempWorld
  dim = [x, y]
  if (len(tempWorld) != dim[0]*dim[1]):
    tempWorld = [0] * (dim[0]*dim[1])

def getLine(fileName, lineNumber):
  with open(fileName, "r") as fs:
    ln = 1
    for line in fs:
      if (ln == lineNumber):
        return line
      ln = ln + 1


def loadTextures(fileName, fileName1):
  global textures
  global iTextures
  textures = []
  lines = []
  iTextures = []
  lines = []
  with open(fileName1, "r") as filestream:
    for line in filestream:
        cl = line.split(".")
        lines.append(cl)
  for l in lines:
    iTextures.append([[l[0], l[1], l[2], l[3], l[4]], [l[5], l[6], l[7], l[8], l[9]], [l[10], l[11], l[12], l[13], l[14]], [l[15], l[16], l[17], l[18], l[19]], [l[20], l[21], l[22], l[23], l[24]]])
  filestream.close()

def getTexture(num):
  global textures
  tex = getLine("Textures/" + str(num), 3)
  l = tex.split(".")
  return [[l[0], l[1], l[2], l[3]], [l[4], l[5], l[6], l[7]], [l[8], l[9], l[10], l[11]], [l[12], l[13], l[14], l[15]]]
  
def getItemTexture(num):
  global iTextures
  if (num < len(iTextures)):
    text = iTextures[num]
    return text
  else:
    return iTextures[0]

def openInventory(fileName, fileNameq):
  global dim
  global inv
  global qty
  invt = open(fileName, "r")
  lines = invt.read()
  inv = split(lines)
  invt.close()
  q = open(fileNameq, "r")
  lines = q.read()
  qty = split(lines)
  q.close()

def openWorld(fileName):
  global dim
  global spawn
  global tempWorld
  wd = open(fileName, "r")
  lines = wd.read()
  data = lines.split(",")
  dim = [int(data[0]), int(data[1])]
  spawn = [int(data[2]), int(data[3])]
  if (len(split(data[4])) == dim[0]*dim[1]):
    tempWorld = split(data[4])
  else:
    tempWorld = [0] * (dim[0]*dim[1])
  wd.close()

def saveWorld(fileName):
  global tempWorld
  global dim
  global spawn
  print("saving...")
  with open(fileName, "w") as wd:
    wd.seek(0, 0)
    wd.write(str(dim[0]))
    wd.write(",")
    wd.write(str(dim[1]))
    wd.write(",")
    wd.write(str(spawn[0]))
    wd.write(",")
    wd.write(str(spawn[1]))
    wd.write(",")
    for block in tempWorld:
        wd.write(block)
  wd.close()

def getBlock(x, y):
  global tempWorld
  global dim
  #wd = open("world.txt", "r")
  #wd.seek(y + (dim[1] * x), 0)
  if (y < dim[1]):  
    return int(tempWorld[y + (dim[1] * x)])
  else:
    return 0

def getBlockType(block):
  if (block == 0):
    return 0
  if (block == 1):
    return 2
  if (block == 2):
    return 2
  if (block == 3):
    return 2
  if (block == 4):
    return 1
  if (block == 5):
    return 1
  if (block == 6):
    return 1
  if (block == 7):
    return 1


def setBlock(x, y, num):
  global tempWorld
  global dim
  tempWorld[y + (dim[1] * x)] = str(num)

def getInventoryItem(numSlot):
  global inv
  return int(inv[numSlot])

def setInventoryItem(numSlot, itm, q):
  global inv
  inv[numSlot] = itm
  qty[numSlot] = q

def prepareWorld(fileName):
  global spawn
  openWorld(fileName) 
  print(spawn)
  logic.setPlayerPos(spawn[0], spawn[1])
  gui.setScreen(spawn[0] - 10, spawn[1] - 10, spawn[0] + 22, spawn[1] + 14, 10)
  gui.drawFullScreen()
  gui.drawToolBar(0)
  gui.drawHealthBar()

def rePrepareWorld():
  global spawn
  print(spawn)
  logic.setPlayerPos(spawn[0], spawn[1])
  gui.setScreen(spawn[0] - 10, spawn[1] - 10, spawn[0] + 22, spawn[1] + 14, 10)
  gui.drawFullScreen()
  gui.drawToolBar(0)
  gui.drawHealthBar()