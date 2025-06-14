import random
import multiprocessing as mp
import viewer
import memoria_compartilhada as mc
import time

init_mutex = mp.Value('i',1)

class Robot:

  def __init__(self,id):
    random.seed()
    self.forca = random.randint(1,10)
    self.energy = random.randint(10,100)
    self.speed = random.randint(1,5)
    self.id = id
    self.status = 1  # 1 = vivo, 0 = morto
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

  def duelo(id_a, id_b):
    with mc.robots_mutex:
        idx_a = id_a * 8
        idx_b = id_b * 8

        fa = mc.robots[idx_a + 3]
        ea = mc.robots[idx_a + 4]
        fb = mc.robots[idx_b + 3]
        eb = mc.robots[idx_b + 4]

        power_a = (2 * fa) + ea
        power_b = (2 * fb) + eb

        if power_a > power_b:
            mc.robots[idx_b + 6] = 0  # morto
            return id_a
        elif power_b > power_a:
            mc.robots[idx_a + 6] = 0  # morto
            return id_b
        else:
            mc.robots[idx_a + 6] = 0
            mc.robots[idx_b + 6] = 0
            return None  
          
  def housekeeping(self):
        while self.status == 1 and not mc.gameover.value:
            time.sleep(1)  # a cada 1 segundo
            self.energy -= 1
            if self.energy <= 0:
                self.status = 0
            with mc.robots_mutex:
                idx = self.id * 8
                mc.robots[idx + 4] = self.energy
                mc.robots[idx + 6] = self.status

  def play(self):
    if(init_mutex.value):
      self.initgame()
      init_mutex.value -= 1
    #decidir acao

