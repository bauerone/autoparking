import math
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager

def angle_of_line(x1, y1, x2, y2):
    return math.atan2(y2-y1, x2-x1)

def make_square(x, y, width):
    square = np.array([[x-int(width/2),i] for i in range(y-int(width/2),y+int(width/2))] +\
                      [[x+int(width/2),i] for i in range(y-int(width/2),y+int(width/2))] +\
                      [[i,y-int(width/2)] for i in range(x-int(width/2),x+int(width/2))] +\
                      [[i,y+int(width/2)] for i in range(x-int(width/2),x+int(width/2))]) 
    return square

class DataLogger:
    def __init__(self):
        self.path = []
        self.car_state = []
        self.u = []

    def log(self, point, my_car, acc, delta):
        self.path.append(point)
        self.car_state.append([my_car.x, my_car.y, my_car.v, my_car.psi])
        self.u.append([acc, delta])

    def save_data(self):
        os.makedirs('log_results', exist_ok=True)
        t = np.arange(0,len(self.path)/5,0.2)
        self.path = np.array(self.path)
        self.car_state = np.array(self.car_state)
        self.u = np.array(self.u)
        font = font_manager.FontProperties(family='Times New Roman', weight='bold',style='normal', size=20)

        # plot x
        plt.figure(figsize=(12,8))
        plt.plot(t, self.path[:,0], color='b', linewidth=5)
        plt.plot(t, self.car_state[:,0], color='r', linewidth=4)
        plt.title('положение автомобиля относительно по оси x относительно времени',fontsize=20)
        plt.xlabel('время (секунды)',fontsize=20)
        plt.ylabel('x (метры)',fontsize=20)
        plt.grid()
        plt.legend(['оптимальное положение', 'x автомобиля'], prop=font)
        plt.savefig('log_results/x.png')

        # plot y
        plt.figure(figsize=(12,8))
        plt.plot(t, self.path[:,1], color='b', linewidth=5)
        plt.plot(t, self.car_state[:,1], color='r', linewidth=4)
        plt.title('положение автомобиля относительно по оси y относительно времени',fontsize=20)
        plt.xlabel('время (секунды)',fontsize=20)
        plt.ylabel('y (метры)',fontsize=20)
        plt.grid()
        plt.legend(['reference', 'car\'s y'], prop=font)
        plt.savefig('log_results/y.png')

        # plot v
        plt.figure(figsize=(12,8))
        plt.plot(t, self.car_state[:,2], color='r', linewidth=4)
        plt.title('скорость автомобиля относительно времени',fontsize=20)
        plt.xlabel('время (секунды)',fontsize=20)
        plt.ylabel('скорость (метры в секунды)',fontsize=20)
        plt.grid()
        plt.legend(['скорость авотомился (метры в секунду)'], prop=font)
        plt.savefig('log_results/v.png')

        # plot psi
        plt.figure(figsize=(12,8))
        plt.plot(t, np.rad2deg(self.car_state[:,3]), color='r', linewidth=4)
        plt.title('направление автомобиля относительно времени',fontsize=20)
        plt.xlabel('время (секунды)',fontsize=20)
        plt.ylabel('навпраление (градусы)',fontsize=20)
        plt.grid()
        plt.legend(['направление автомобиля (градусы)'], prop=font)
        plt.savefig('log_results/psi.png')

        # plot position
        plt.figure(figsize=(12,12))
        plt.plot(self.path[:,0], self.path[:,1], color='b', linewidth=5)
        plt.plot(self.car_state[:,0], self.car_state[:,1], color='r', linewidth=4)
        plt.title('позиция автомобиля относительно времени',fontsize=20)
        plt.xlabel('x (метры)',fontsize=20)
        plt.ylabel('y (метры)',fontsize=20)
        plt.grid()
        plt.legend(['оптимальное пложение','положение автомобиля'], prop=font)
        plt.savefig('log_results/position.png')

        # plot accelerate
        plt.figure(figsize=(12,8))
        plt.plot(t, self.u[:,0], color='r', linewidth=4)
        plt.title('ускорение автомобиля относительно времени',fontsize=20)
        plt.xlabel('время (секунды)',fontsize=20)
        plt.ylabel('ускорение (метр^2/секунды)',fontsize=20)
        plt.grid()
        plt.legend(['ускорение автомобиля (метр^2/секунды)'], prop=font)
        plt.savefig('log_results/accelerate.png')

        # plot delta
        plt.figure(figsize=(12,8))
        plt.plot(t, np.rad2deg(self.u[:,1]), color='r', linewidth=4)
        plt.title('угол поворота автомобился относительно времени',fontsize=20)
        plt.xlabel('время (секунды)',fontsize=20)
        plt.ylabel('поворот (градусы)',fontsize=20)
        plt.grid()
        plt.legend(['угол поворота автомобиля (градусы)'], prop=font)
        plt.savefig('log_results/steer.png')

        print('Все данные сохранены в директорию логирования ...')
