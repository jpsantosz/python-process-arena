import random
import multiprocessing as mp
import threading
import memoria_compartilhada as mc
import time

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
                idx = r.id * 6
                mc.robot_data[idx + 4] = x
                mc.robot_data[idx + 5] = y
                break

    for i in range(mc.battery):
        while True:
            x = random.randint(1, mc.line-1)
            y = random.randint(1, mc.colum-1)
            if(mc.grid[x*mc.colum+y].decode() == ' '):
                mc.grid[x*mc.colum+y] = bytes(str('*'), 'utf-8')[0:1]
                mc.battery_mutex[i] = 1
                mc.battery_mutex_xy[i*2] = x
                mc.battery_mutex_xy[i*2+1] = y
                break

  def duelo(self, id_a, id_b):
        idx_a = id_a * 6
        idx_b = id_b * 6

        fa = mc.robot_data[idx_a + 1]
        ea = mc.robot_data[idx_a + 2]
        fb = mc.robot_data[idx_b + 1]
        eb = mc.robot_data[idx_b + 2]

        power_a = (2 * fa) + ea
        power_b = (2 * fb) + eb

        if power_a > power_b:
            mc.robot_data[idx_b + 3] = 0
            mc.vivos.value -= 1
            mc.grid[mc.robot_data[idx_b + 4]*mc.colum + mc.robot_data[idx_b + 5]] = b' '
            print("Ganhei")
        elif power_b > power_a:
            mc.robot_data[idx_a + 3] = 0
            mc.vivos.value -= 1
            mc.grid[mc.robot_data[idx_a + 4]*mc.colum + mc.robot_data[idx_a + 5]] = b' '
            print("Perdi")
        else:
            mc.robot_data[idx_a + 3] = 0
            mc.robot_data[idx_b + 3] = 0
            mc.vivos.value -= 2
            mc.grid[mc.robot_data[idx_a + 4]*mc.colum + mc.robot_data[idx_a + 5]] = b' '
            mc.grid[mc.robot_data[idx_b + 4]*mc.colum + mc.robot_data[idx_b + 5]] = b' '
            print("2 morreu") 
          
  def housekeeping(self):
    idx = self.id * 6
    while not mc.gameover.value:
        time.sleep(1)
        with mc.grid_mutex, mc.robot_mutex:
            # Verifica se ainda está vivo
            if mc.robot_data[idx + 3] == 0:
                break

            #  Verifica se é o último vivo
            if mc.vivos.value <= 1 and mc.robot_data[idx + 3] == 1:
                mc.gameover.value = True
                mc.vencedor.value = self.id+1
                mc.grid[mc.robot_data[idx + 4]*mc.colum + mc.robot_data[idx + 5]] = bytes(str(self.id + 1), 'utf-8')
                break  # ganhou, sai do loop

            # Reduz energia
            mc.robot_data[idx + 2] -= 1

            # Verifica energia após redução
            if mc.robot_data[idx + 2] <= 0:
                mc.robot_data[idx + 3] = 0  # status = morto
                mc.vivos.value -= 1
                mc.grid[mc.robot_data[idx + 4]*mc.colum+mc.robot_data[idx + 5]] = b' '
                self.status = 0            
    
  def sense_act(self):
    EMPTY = b' '
    BATTERY = b'*'
    ENERGY_MAX = 100
    MAX_LINE = mc.line
    MAX_COLUM = mc.colum
    idx = self.id * 6
    is_in_battery = -1
    while mc.vencedor.value == -1 and self.status == 1:
        time.sleep(random.randint(1, 5) * 0.2)  # Delay de ação conforme a "velocidade"
        
        with mc.grid_mutex, mc.robot_mutex:
            
            #Autaliza o status
            self.status =  mc.robot_data[idx + 3]
            if self.status == 0:
                break
            x, y = mc.robot_data[idx + 4], mc.robot_data[idx + 5]
            dx, dy = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            nx, ny = x + dx, y + dy
            if 0 < nx < MAX_LINE-1 and 0 < ny < MAX_COLUM-1:
                target = mc.grid[nx * MAX_COLUM + ny]
                if target == EMPTY:
                    # Movimento
                    if is_in_battery != -1:
                        mc.grid[x * MAX_COLUM + y] = BATTERY
                        mc.battery_mutex[is_in_battery] = 1
                        is_in_battery = -1
                    else:
                        mc.grid[x * MAX_COLUM + y] = EMPTY
                    mc.grid[nx * MAX_COLUM + ny] = bytes(str(self.id + 1), 'utf-8')
                    mc.robot_data[idx + 4] = nx
                    mc.robot_data[idx + 5] = ny

                elif target == BATTERY:
                    # Recarrega energia
                    is_a_battery = mc.get_battery_mutex(nx,ny)
                    if mc.battery_mutex[is_a_battery] == 1:
                        mc.battery_mutex[is_a_battery] = 0
                        if is_in_battery != -1:
                            mc.grid[x * MAX_COLUM + y] = BATTERY
                            mc.battery_mutex[is_in_battery] = 1
                        else:
                            mc.grid[x * MAX_COLUM + y] = EMPTY
                        is_in_battery = is_a_battery
                    else:
                        continue
                    mc.grid[nx * MAX_COLUM + ny] = bytes(str(self.id + 1), 'utf-8')
                    mc.robot_data[idx + 4] = nx
                    mc.robot_data[idx + 5] = ny 
                    mc.robot_data[idx + 2] = min(ENERGY_MAX, mc.robot_data[idx + 2] + 20)

                elif target.decode().isdigit():
                    enemy_id = int(target.decode()) - 1
                    if enemy_id != self.id:
                        print("Duelo")
                        self.duelo(self.id, enemy_id)

  def play(self, all_robots):
    with mc.init_mutex.get_lock():
            if mc.init_mutex.value == 1:
                mc.init_mutex.value = 0
                self.initgame(all_robots)
    # Inicializa posição e status no robot_data
    idx = self.id * 6
    mc.robot_data[idx + 0] = self.id
    mc.robot_data[idx + 1] = self.forca
    mc.robot_data[idx + 2] = self.energy
    mc.robot_data[idx + 3] = self.status

    # Inicia comportamento do robô
    t1 = threading.Thread(target=self.sense_act)
    t2 = threading.Thread(target=self.housekeeping)  # novo método contínuo
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
