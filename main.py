import multiprocessing as mp

import robots
import viewer

if __name__ == "__main__":
    robo1 = robots.Robot(1)
    robo1.play()
    viewer.printgrid()
    pass
