import multiprocessing as mp
import memoria_compartilhada as mc
from robots import Robot
import viewer

def run_robot(rid):
    robo1 = robots.Robot(1)
    robo1.play()

if __name__ == "__main__":
    viewer_process = mp.Process(target=viewer.viewer_loop)
    viewer_process.start()
    
    robots = [Robot(i) for i in range(4)]

    processes = []
    for robot in robots:
        p = mp.Process(target=robot.play, args=(robots,))
        p.start()
        processes.append(p)


    mc.gameover.value = True
    viewer_process.join()