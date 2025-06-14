import multiprocessing as mp
import memoria_compartilhada as mc
import robots
import viewer

def run_robot(rid):
    robo1 = robots.Robot(1)
    robo1.play()

if __name__ == "__main__":
    viewer.printgrid()
    
    robos = []
    for i in range(4):  # 4 robôs
        p = mp.Process(target=run_robot, args=(i,))
        robos.append(p)
        p.start()

    for p in robos:
        p.join()

    mc.gameover.value = True