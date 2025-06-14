import random
import multiprocessing as mp
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
    self.x = -1
    self.y = -1
    pass

  def initgame(self, robots):
    for i in range(1, mc.line-1):
        for j in range(1, mc.colum-1):
            mc.grid[i*mc.colum+j] = b' '
    for i in range(mc.line):
        if i == 0 or i == mc.line-1:
            for j in range(mc.colum):
                mc.grid[i*mc.colum+j] =  b'#'
        else:
            mc.grid[i*mc.colum] =  b'#'
            mc.grid[i*mc.colum+ mc.colum-1] =  b'#'
    for r in robots:
        while True:
            x = random.randint(1, mc.line-1)
            y = random.randint(1, mc.colum-1)
            if(mc.grid[x*mc.colum+y].decode() == ' '):
                mc.grid[x*mc.colum+y] = bytes(str(r.id + 1), 'utf-8')[0:1]
                r.x = x
                r.y = y
                break

    for i in range(4):
        while True:
            x = random.randint(1, mc.line-1)
            y = random.randint(1, mc.colum-1)
            if(mc.grid[x*mc.colum+y].decode() == ' '):
                mc.grid[x*mc.colum+y] = bytes(str('*'), 'utf-8')[0:1]
                break

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
        time.sleep(1)  # Executa a cada 1 segundo
        with mc.robot_mutex:
            idx = self.id * 6
            # Reduz energia diretamente no array compartilhado
            mc.robot_data[idx + 2] -= 1

            # Verifica energia após redução
            if mc.robot_data[idx + 2] <= 0:
                mc.robot_data[idx + 3] = 0  # status = morto
                self.status = 0

                
  def sense_act(self):
    EMPTY = b' '
    BATTERY = b'*'
    ENERGY_MAX = 100
    GRID_WIDTH = mc.colum
    GRID_HEIGHT = mc.line

    while mc.vencedor.value == -1 and self.status == 1:
        time.sleep(random.randint(1, 5) * 0.2)  # Delay de ação conforme a "velocidade"

        with mc.grid_mutex, mc.robot_mutex:
            idx = self.id * 6
            E = mc.robot_data[idx + 2]

            if E <= 0:
                self.status = 0
                return

            x, y = mc.robot_data[idx + 4], mc.robot_data[idx + 5]
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            nx, ny = x + dx, y + dy

            if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT:
                target = mc.grid[ny * GRID_WIDTH + nx]

                if target == EMPTY[0]:
                    # Movimento
                    mc.grid[y * GRID_WIDTH + x] = EMPTY[0]
                    mc.grid[ny * GRID_WIDTH + nx] = bytes(str(self.id + 1), 'utf-8')[0]
                    mc.robot_data[idx + 4] = nx
                    mc.robot_data[idx + 5] = ny
                    mc.robot_data[idx + 2] -= 1  # Consome energia

                elif target == BATTERY[0]:
                    # Recarrega energia
                    mc.robot_data[idx + 2] = min(ENERGY_MAX, E + 20)

                elif target.decode().isdigit():
                    enemy_id = int(target.decode()) - 1
                    if enemy_id != self.id:
                        self.duel(self.id, enemy_id)


  def play(self, all_robots):
    with init_mutex.get_lock():
        if init_mutex.value:
            self.initgame(all_robots)
            init_mutex.value = 0

    # Inicializa posição e status no robot_data
    idx = self.id * 6
    with mc.robot_mutex:
        mc.robot_data[idx + 0] = self.id
        mc.robot_data[idx + 1] = self.forca
        mc.robot_data[idx + 2] = self.energy
        mc.robot_data[idx + 3] = self.status
        mc.robot_data[idx + 4] = self.x
        mc.robot_data[idx + 5] = self.y

    # Inicia comportamento do robô
    self.sense_act()