import multiprocessing as mp
from ctypes import c_char

# Dimensões do grid
line = 20
colum = 40
size = line * colum
battery =20
# Grid compartilhado
grid = mp.Array(c_char, size)

# Dados dos robôs (6 campos por robô: id, força, energia, status, x, y)
robot_data = mp.Array('i', 4 * 6)  # 4 robôs * 6 dados cada

# Mutexes para controlar o acesso compartilhado
grid_mutex = mp.Lock()
robot_mutex = mp.Lock()
battery_mutex = mp.Array('i',battery)
battery_mutex_xy = mp.Array('i',battery*2)
#Conta a quantidade de robos vivos
vivos = mp.Value('i', 0)
# Controle de fim de jogo
gameover = mp.Value('b', False)
#Controla inicio do jogo
init_mutex = mp.Value('i',1)
# Vencedor (-1 significa ainda sem vencedor)
vencedor = mp.Value('i', -1)


def get_battery_mutex(x,y):
  for i in range(battery):
    if x == battery_mutex_xy[i*2] and y == battery_mutex_xy[i*2+1]:
      return i
