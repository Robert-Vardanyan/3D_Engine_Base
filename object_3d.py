import pygame as pg
from matrix_functions import *


'''
    1) Object3d
- Этот класс представляет 3D объект, который можно рисовать и манипулировать в пространстве. Включает методы для вращения, масштабирования и переноса объекта, а также для проекции объекта на 2D экран.
    

    2) Axes
- Этот класс наследуется от Object3d и представляет собой оси координат (X, Y, Z) для наглядности ориентации объектов в 3D пространстве. Оси имеют свои уникальные цвета и метки.
'''


class Object3d:
    # Конструктор класса Object3d, который представляет 3D объект
    def __init__(self, render):
        # Ссылка на объект рендера, который будет использоваться для отрисовки
        self.render = render    
        
        # Определяем вершины куба с координатами (x, y, z, 1), где 1 - однородная координата
        self.vertexes = np.array([(0,0,0,1), (0,1,0,1), (1,1,0,1), (1,0,0,1),
                                  (0,0,1,1), (0,1,1,1), (1,1,1,1), (1,0,1,1)])
        
        # Определяем грани куба, соединяющие вершины
        self.faces = np.array([(0,1,2,3), (4,5,6,7), (0,4,5,1), (2,3,7,6), (1,2,6,5), (0,3,7,4)])
        
        # Шрифт для отображения текста на экране
        self.font = pg.font.SysFont('Arial', 30)
        # Определяем цвет каждой грани
        self.color_faces = [(pg.Color('orange'), face) for face in self.faces]
        # Флаги для управления движением и отрисовкой вершин
        self.movement_flag, self.draw_vertexes = True, True
        # Метка для отображения текста
        self.label = ''


    # Основной метод отрисовки объекта
    def draw(self):
        # Проецируем 3D объект на 2D экран
        self.screen_projection()  
        # Выполняем движение объекта
        self.movement()  


    # Метод для вращения объекта вокруг оси Y, если установлен флаг движения
    def movement(self):
        if self.movement_flag:
            self.rotate_y(pg.time.get_ticks() % 0.005) # Вращение на малый угол


    # Проецируем вершины объекта на экран
    def screen_projection(self):
        vertexes = self.vertexes @ self.render.camera.camera_matrix()   # Применяем матрицу камеры
        vertexes = vertexes @ self.render.projection.projection_matrix  # Применяем матрицу проекции
        vertexes /= vertexes[:,-1].reshape(-1,1)                        # Приводим однородные координаты к обычным
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0                  # Отбрасываем вершины, выходящие за пределы видимости
        vertexes = vertexes @ self.render.projection.to_screen_matrix   # Преобразуем в координаты экрана
        vertexes = vertexes[:, :2]                                      # Оставляем только координаты x и y

        # Отрисовываем грани объекта
        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            # Получаем вершины текущей грани
            polygon = vertexes[face]  
            # Проверяем, что грани находятся в пределах экрана, и рисуем их
            if not np.any((polygon == self.render.H_WIDTH) | (polygon == self.render.H_HEIGHT)):
                pg.draw.polygon(self.render.screen, color, polygon, 3)
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color('white'))
                    self.render.screen.blit(text, polygon[-1])  # Отображаем текстовую метку на грани
        
        # Если включена отрисовка вершин, рисуем их 
        if self.draw_vertexes:
            for vertex in vertexes:
                if not np.any((vertex == self.render.H_WIDTH) | (vertex == self.render.H_HEIGHT)):
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 5)


    # Метод для переноса (трансляции) объекта в пространстве
    def translate(self, pos):
        self.vertexes = self.vertexes @ translate(pos)


    # Метод для масштабирования объекта
    def scale(self, scale_to):
        self.vertexes = self.vertexes @ scale(scale_to)


    # Метод для вращения объекта вокруг оси X
    def rotate_x(self, angle):
        self.vertexes = self.vertexes @ rotate_x(angle)


    # Метод для вращения объекта вокруг оси Y
    def rotate_y(self, angle):
        self.vertexes = self.vertexes @ rotate_y(angle)


    # Метод для вращения объекта вокруг оси Z
    def rotate_z(self, angle):
        self.vertexes = self.vertexes @ rotate_z(angle) 



# Конструктор класса Axes, который наследуется от Object3d
class Axes(Object3d):
    def __init__(self, render):
        super().__init__(render)
        # Определяем вершины осей координат
        self.vertexes = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        # Определяем грани (отрезки) осей координат
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        # Определяем цвета для каждой оси: красный для X, зеленый для Y, синий для Z
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        # Создаем список цветных отрезков для отрисовки
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        # Отключаем отрисовку вершин для осей координат
        self.draw_vertices = False
        # Устанавливаем метки для осей: X, Y и Z
        self.label = 'XYZ'



