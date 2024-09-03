import pygame as pg
from matrix_functions import *


'''
    1) Конструктор класса Camera
- self.render: Хранит объект рендера, который, связан с дисплеем или контекстом отрисовки.
- self.position: Массив NumPy, определяющий текущее положение камеры в 3D-пространстве. Здесь добавляется 1.0 для матричных преобразований.
- self.forward (Z), self.up (Y), self.right (X): Эти три вектора определяют ориентацию камеры в пространстве.
- self.h_fov и self.v_fov: Поля зрения камеры, задающие угол обзора по горизонтали и вертикали.
- self.near_plane и self.far_plane: Определяют расстояния до ближней и дальней плоскостей отсечения, которые ограничивают видимую область.
- self.moving_speed и self.rotate_speed: Определяют скорость движения и вращения камеры.


    2) Метод управления камерой
- key = pg.key.get_pressed(): Получает текущее состояние всех клавиш.
- В зависимости от нажатых клавиш, камера будет перемещаться вперед-назад, влево-вправо или вверх-вниз. Эти движения управляются изменением позиции камеры в направлении соответствующего вектора (right, forward, up).
- Вращение камеры происходит с помощью клавиш стрелок (LEFT, RIGHT, UP, DOWN), что вызывает методы camera_yaw (вокруг оси Y) и camera_pitch (вокруг оси X).

    
    3) Методы вращения камеры 
- camera_yaw и camera_pitch: Эти методы изменяют направление камеры путем вращения вокруг осей Y (для yaw) и X (для pitch).
- rotate = rotate_y(angle) и rotate_x(angle): Эти функции, находятся в модуле matrix_functions, и они создают матрицы вращения для соответствующих осей.
- Вектора forward, right, и up умножаются на матрицу вращения для изменения их направлений.


    4) Методы для создания матриц трансляции и вращения
- translate_matrix: Возвращает матрицу трансляции, которая перемещает камеру в пространство, компенсируя ее текущую позицию.
- rotate_matrix: Возвращает матрицу вращения, которая устанавливает ориентацию камеры в пространстве, используя вектора right, forward, и up.


    5) Метод camera_matrix
- Комбинирует матрицы трансляции и вращения для создания полной матрицы камеры, которая используется для преобразования объектов в пространстве относительно камеры.
'''


class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0])  # Позиция камеры, заданная в 3D-пространстве
        self.forward = np.array([0,0,1,1])  # Вектор направления вперед (оси Z)
        self.up = np.array([0,1,0,1])  # Вектор направления вверх (оси Y)
        self.right = np.array([1,0,0,1])  # Вектор направления вправо (оси X)
        self.h_fov = math.pi /3  # Горизонтальное поле зрения (в радианах)
        self.v_fov = self.h_fov * ( render.HEIGHT / render.WIDTH)  # Вертикальное поле зрения, пропорциональное горизонтальному
        self.near_plane = 0.1  # Ближняя плоскость отсечения
        self.far_plane = 100  # Дальняя плоскость отсечения
        self.moving_speed = 0.02  # Скорость движения камеры
        self.rotate_speed = 0.01  # Скорость вращения камеры


    # 2) Метод управления камерой
    def control(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position -= self.right * self.moving_speed
        if key[pg.K_d]:
            self.position += self.right * self.moving_speed
        if key[pg.K_w]:
            self.position += self.forward * self.moving_speed
        if key[pg.K_s]:
            self.position -= self.forward * self.moving_speed
        if key[pg.K_q]:
            self.position += self.up * self.moving_speed
        if key[pg.K_e]:
            self.position -= self.up * self.moving_speed

        if key[pg.K_LEFT]:
            self.camera_yaw(-self.rotate_speed)
        if key[pg.K_RIGHT]:
            self.camera_yaw(self.rotate_speed)
        if key[pg.K_UP]:
            self.camera_pitch(-self.rotate_speed)
        if key[pg.K_DOWN]:
            self.camera_pitch(self.rotate_speed)


    # 3) Методы вращения камеры 
    def camera_yaw(self, angle):
        rotate = rotate_y(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate

    def camera_pitch(self, angle):
        rotate = rotate_x(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate


    # 4) Методы для создания матриц трансляции и вращения
    def translate_matrix(self):
        x,y,z,w = self.position
        return np.array([
            [1,0,0,0],
            [0,1,0,1],
            [0,0,1,0],
            [-x,-y,-z,1]
        ])

    def rotate_matrix(self):
        rx,ry,rz,w = self.right
        fx,fy,fz,w = self.forward
        ux,uy,uz,w = self.up
        return np.array([
            [rx,ux,fx,0],
            [ry,uy,fy,0],
            [rz,uz,fz,0],
            [0,0,0,1]
        ])
    

    # 5) Метод camera_matrix
    def camera_matrix(self):
        return self.translate_matrix() @ self.rotate_matrix()
