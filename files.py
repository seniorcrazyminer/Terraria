import logic
import gui
import os


dim = [0, 0]
spawn = [0, 0]
iTextures = []
tempWorld = []
tempWorldVar = []

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
  global tempWorld, tempWorldVar
  dim = [x, y]
  if (len(tempWorld) != dim[0]*dim[1]):
    tempWorld = [0] * (dim[0]*dim[1])
  if (len(tempWorldVar) != dim[0]*dim[1]):
    tempWorldVar = [0] * (dim[0]*dim[1])

def getLine(fileName, lineNumber):
  l = ""
  with open(fileName, "r") as fs:
    ln = 1
    for line in fs:
      if (ln == lineNumber):
        l = line
      ln = ln + 1
    fs.close()
  return l

def getSetting(num):
  line = getLine("settings.config", num)
  setting = int(line.split(": ")[1])
  return setting


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
    iTextures.append([[l[i], l[i+1], l[i+2], l[i+3], l[i+4]] for i in range(0, 25, 5)])
  filestream.close()

def getTexture(num):
  return int(getLine("Textures/" + str(num), 1))
  
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

def listAllWorlds():
  directory = r'/home/runner/Terraria/Worlds/'
  list = []
  for filename in os.listdir(directory):
      if filename.endswith(".wrld"):
          list.append(filename[0:filename.find('.')])
      else:
          continue
  return list

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
  if (x >= 0 and x <= dim[0] - 1 and y >= 0 and y <= dim[1]-1):  
    return int(tempWorld[y + (dim[1] * x)])
  else:
    return -1

def getBlockType(block):
  return int(getLine("Textures/" + str(block), 2))

def getDrop(block):
  string =  getLine("Textures/" + str(block), 3).strip(')(\n').split(', ')
  return string


def setBlock(x, y, blk):
  global tempWorld
  global dim
  tempWorld[y + (dim[1] * x)] = str(blk)

def getInventoryItem(numSlot):
  global inv
  return int(inv[numSlot])

def getInventoryQuantity(numSlot):
  global qty
  return int(qty[numSlot])

def setInventoryItem(numSlot, itm, q):
  global inv, qty
  inv[numSlot] = itm
  qty[numSlot] = q

def prepareWorld(fileName):
  global spawn
  openWorld(fileName) 
  print(spawn)
  logic.setPlayerPos(spawn[0], spawn[1])
  padding = getSetting(4)
  sWidth = getSetting(2)
  sHeight = getSetting(3)
  msw = sWidth - padding
  msh = sHeight - padding
  gui.setScreen(spawn[0] - padding, spawn[1] - padding, spawn[0] + msw, spawn[1] + msh, 10)
  gui.drawFullScreen()
  gui.drawToolBar(0)
  gui.drawHealthBar()

def rePrepareWorld():
  global spawn
  print(spawn)
  logic.setPlayerPos(spawn[0], spawn[1])
  padding = getSetting(4)
  sWidth = getSetting(2)
  sHeight = getSetting(3)
  msw = sWidth - padding
  msh = sHeight - padding
  gui.setScreen(spawn[0] - padding, spawn[1] - padding, spawn[0] + msw, spawn[1] + msh, 10)
  gui.drawFullScreen()
  gui.drawToolBar(0)
  gui.drawHealthBar()