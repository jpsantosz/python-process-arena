import multiprocessing as mp
from ctypes import c_char

# Dimensões do grid
line = 40
colum = 20
size = line * colum

# Grid compartilhado
grid = mp.Array(c_char, size)

# Dados dos robôs (6 campos por robô: id, força, energia, status, x, y)
robot_data = mp.Array('i', 4 * 6)  # 4 robôs * 6 dados cada

# Mutexes para controlar o acesso compartilhado
grid_mutex = mp.Lock()
robot_mutex = mp.Lock()

# Controle de fim de jogo
gameover = mp.Value('b', False)

# Vencedor (-1 significa ainda sem vencedor)
vencedor = mp.Value('i', -1)