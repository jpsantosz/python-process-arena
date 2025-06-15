import memoria_compartilhada as mc
import time
import os

def printgrid():
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(mc.line):
        line = ""
        for j in range(mc.colum):
            c = mc.grid[i * mc.colum + j].decode()
            line += c
        print(line)
    print("\n")

def viewer_loop():
    while not mc.gameover.value:
        printgrid()
        time.sleep(0.2)
    printgrid()
    print(f"O vencedor é {mc.vencedor.value}")
