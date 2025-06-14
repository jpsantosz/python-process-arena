import memoria_compartilhada as mc
import time
import os

def printgrid():
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(mc.LINE):
        line = ""
        for j in range(mc.COLUMN):
            c = chr(mc.grid[i * mc.COLUMN + j])
            line += c
        print(line)
    print("\n")

def viewer_loop():
    while not mc.gameover.value:
        printgrid()
        time.sleep(0.2)