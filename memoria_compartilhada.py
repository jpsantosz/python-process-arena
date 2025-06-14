import multiprocessing as mp
from ctypes import c_char
line = 40
colum = 20
size = 40*20
grid = mp.Array(c_char,size)

robots = []
gameover = mp.Value('b',False)
