import cv2
import numpy as np
from time import sleep
import argparse

from environment import Environment, Parking1
from pathplanning import PathPlanning, ParkPathPlanning, interpolate_path
from control import Car_Dynamics, MPC_Controller, Linear_MPC_Controller
from utils import angle_of_line, make_square, DataLogger

class MainAutopark:
    def __init__(self, args):
        print(args)
        logger = DataLogger()

        # default variables
        start = np.array([args.x_start, args.y_start])
        end   = np.array([args.x_end, args.y_end])

        # environment margin  : 5
        # pathplanning margin : 5

        # defining obstacles
        parking1 = Parking1(args.parking)
        end, obs = parking1.generate_obstacles()

        if args.add_more_walls:
            # add squares
            square1 = make_square(10,65,20)
            square2 = make_square(15,30,20)
            square3 = make_square(50,50,10)
            obs = np.vstack([obs,square1,square2,square3])

        # new_obs = np.array([[78,78],[79,79],[78,79]])
        # obs = np.vstack([obs,new_obs])

        # initialization
        env = Environment(obs)
        my_car = Car_Dynamics(start[0], start[1], 0, np.deg2rad(args.psi_start), length=4, dt=0.2)
        MPC_HORIZON = 5
        controller = MPC_Controller()

        res = env.render(my_car.x, my_car.y, my_car.psi, 0)
        cv2.imshow('Parking System', res)
        key = cv2.waitKey(1)

        # path planning
        park_path_planner = ParkPathPlanning(obs)
        path_planner = PathPlanning(obs)

        print('Планирование сценария автоматической парковки ...')
        new_end, park_path, ensure_path1, ensure_path2 = park_path_planner.generate_park_scenario(int(start[0]),int(start[1]),int(end[0]),int(end[1]))
        
        print('Прокладывание маршрута ...')
        path = path_planner.plan_path(int(start[0]),int(start[1]),int(new_end[0]),int(new_end[1]))
        path = np.vstack([path, ensure_path1])

        print('Интерполяция ...')
        interpolated_path = interpolate_path(path, sample_rate=5)
        interpolated_park_path = interpolate_path(park_path, sample_rate=2)
        interpolated_park_path = np.vstack([ensure_path1[::-1], interpolated_park_path, ensure_path2[::-1]])

        env.draw_path(interpolated_path)
        env.draw_path(interpolated_park_path)

        final_path = np.vstack([interpolated_path, interpolated_park_path, ensure_path2])

        #############################################################################################

        ################################## control ##################################################
        print('Движение к цели ...')
        for i,point in enumerate(final_path):

                acc, delta = controller.optimize(my_car, final_path[i:i+MPC_HORIZON])
                my_car.update_state(my_car.move(acc,  delta))
                res = env.render(my_car.x, my_car.y, my_car.psi, delta)
                logger.log(point, my_car, acc, delta)
                cv2.imshow('Parking System', res)
                key = cv2.waitKey(1)
                if key == ord('s'):
                    cv2.imwrite('res.png', res*255)

        # zeroing car steer
        res = env.render(my_car.x, my_car.y, my_car.psi, 0)
        logger.save_data()
        cv2.imshow('Parking System', res)
        key = cv2.waitKey()
        #############################################################################################

        cv2.destroyAllWindows()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--x_start', type=int, default=0, help='стартовый X')
    parser.add_argument('--y_start', type=int, default=90, help='стартовый Y')
    parser.add_argument('--psi_start', type=int, default=0, help='стартовое направление')
    parser.add_argument('--x_end', type=int, default=90, help='конечное Х')
    parser.add_argument('--y_end', type=int, default=80, help='конечное Y')
    parser.add_argument('--parking', type=int, default=1, help='свободное парковочное место (от 1 до 24)')
    parser.add_argument('--add_more_walls', action=argparse.BooleanOptionalAction, help='добавление дополнительных заграждений')

    args = parser.parse_args()

    MainAutopark(args)