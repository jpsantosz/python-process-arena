import memoria_compartilhada as mc


def printgrid():
  for i in range(mc.line):
      for j in range(mc.colum):
        print(f"{mc.grid[i*mc.colum+j].decode()}")
      print('\n')
