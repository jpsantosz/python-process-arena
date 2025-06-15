import multiprocessing as mp
import memoria_compartilhada as mc
from robots import Robot
import viewer

def run_robot(robot, all_robots):
    robot.play(all_robots)


if __name__ == "__main__":
    viewer_process = mp.Process(target=viewer.viewer_loop)
    viewer_process.start()
    
    robots = [Robot(i) for i in range(4)]

    processes = []
    for robot in robots:
        p = mp.Process(target=run_robot, args=(robot, robots))
        p.start()
        processes.append(p)
        mc.vivos.value += 1
        
    for p in processes:
        p.join()

    mc.gameover.value = True
    viewer_process.join()
