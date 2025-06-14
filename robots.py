import random
import multiprocessing as mp
import viewer
import memoria_compartilhada as mc
init_mutex = mp.Value('i',1)

class Robot:

  def __init__(self,id):
    random.seed()
    self.forca = random.randint(1,10)
    self.energy = random.randint(10,100)
    self.speed = random.randint(1,5)
    self.id = id
    pass

  def initgame(self):
    for i in range(mc.line):
      if i == 0 or i == mc.line-1:
        for j in range(mc.colum):
          mc.grid[i*mc.colum+j] =  b'#'
      else:
        mc.grid[i*mc.colum] =  b'#'
        mc.grid[i*mc.colum+ mc.line-1] =  b'#'
    for i in range(1,mc.line-1):
      for j in range(1,mc.colum):
        mc.grid[i*mc.colum+j] = b' '
    pass

  def play(self):
    if(init_mutex.value):
      self.initgame()
      init_mutex.value -= 1
    #decidir acao

