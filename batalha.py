def duelo(robot_a, robot_b):
    # poder = 2F + E
    power_a = (2 * robot_a['F']) + robot_a['E']
    power_b = (2 * robot_b['F']) + robot_b['E']
    
    if power_a > power_b:
        robot_b['E'] = 0  # robô B morre
        return robot_a
    elif power_b > power_a:
        robot_a['E'] = 0  # robô A morre
        return robot_b
    else:
        robot_a['E'] = 0
        robot_b['E'] = 0  # ambos morrem
        return None