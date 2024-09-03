import math
import numpy as np


'''
    1) Функция translate:
- Создает матрицу переноса (трансляции), которая смещает объект в пространстве по осям x, y и z.


    2) Функция rotate_x:
- Создает матрицу вращения вокруг оси X. Это позволяет вращать объект относительно оси X, что изменяет его положение по осям Y и Z.


    3) Функция rotate_y:
- Создает матрицу вращения вокруг оси Y. Вращение вокруг Y изменяет положение объекта по осям X и Z.


    4) Функция rotate_z:
- Создает матрицу вращения вокруг оси Z. Вращение вокруг Z изменяет положение объекта по осям X и Y.


    5) Функция scale:
- Создает матрицу масштабирования. Эта матрица увеличивает или уменьшает объект во всех направлениях (X, Y, Z) на заданный коэффициент n.
'''


# 1) Функция для создания матрицы переноса (трансляции) в пространстве
def translate(pos):
    # pos - это массив с координатами смещения по x, y и z
    tx, ty, tz = pos # Распаковываем координаты смещения
    
    return np.array([
        [1, 0, 0, 0],    # Первый столбец - единичная матрица (без изменения по оси x)
        [0, 1, 0, 0],    # Второй столбец - единичная матрица (без изменения по оси y)
        [0, 0, 1, 0],    # Третий столбец - единичная матрица (без изменения по оси z)
        [tx, ty, tz, 1]  # Четвертый столбец - добавляем смещение по x, y и z
    ])


# 2) Функция для создания матрицы вращения вокруг оси X
def rotate_x(a):
    # a - угол вращения в радианах
    
    return np.array([
        [1, 0, 0, 0],                       # Первый столбец - без изменения по оси x
        [0, math.cos(a), math.sin(a), 0],   # Вращение по осям y и z
        [0, -math.sin(a), math.cos(a), 0],  # Вращение по осям y и z
        [0, 0, 0, 1]                        # Четвертый столбец - без изменения по оси w (однородная координата)
    ])


# 3) Функция для создания матрицы вращения вокруг оси Y
def rotate_y(a):
    # a - угол вращения в радианах
    
    return np.array([
        [math.cos(a), 0, -math.sin(a), 0],  # Вращение по осям x и z
        [0, 1, 0, 0],                       # Второй столбец - без изменения по оси y
        [math.sin(a), 0, math.cos(a), 0],   # Вращение по осям x и z
        [0, 0, 0, 1]                        # Четвертый столбец - без изменения по оси w (однородная координата)
    ])


# 4) Функция для создания матрицы вращения вокруг оси Z
def rotate_z(a):
    # a - угол вращения в радианах
    
    return np.array([
        [math.cos(a), math.sin(a), 0, 0],   # Вращение по осям x и y
        [-math.sin(a), math.cos(a), 0, 0],  # Вращение по осям x и y
        [0, 0, 1, 0],                       # Третий столбец - без изменения по оси z
        [0, 0, 0, 1]                        # Четвертый столбец - без изменения по оси w (однородная координата)
    ])


# 5) Функция для создания матрицы масштабирования
def scale(n):
    # n - коэффициент масштабирования
    
    return np.array([
        [n, 0, 0, 0],  # Масштабируем по оси x
        [0, n, 0, 0],  # Масштабируем по оси y
        [0, 0, n, 0],  # Масштабируем по оси z
        [0, 0, 0, 1]   # Четвертый столбец - без изменения по оси w (однородная координата)
    ])