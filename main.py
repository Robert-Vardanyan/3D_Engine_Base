from object_3d import *
from camera import *
from projection import *
import pygame as pg


class SoftwareRender:
    def __init__(self):
        # Инициализируем Pygame
        pg.init()  
        # Установка иконки и заголовка окна
        icon = pg.image.load('icon.png')
        pg.display.set_icon(icon)
        # Устанавливаем разрешение окна (ширина и высота)
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900  
        # Вычисляем половину ширины и высоты для удобства
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2  
        # Устанавливаем желаемую частоту кадров
        self.FPS = 60  
        # Создаем окно для отображения графики с заданным разрешением
        self.screen = pg.display.set_mode(self.RES)  
        # Создаем объект Clock для управления временем (например, задержки между кадрами)
        self.clock = pg.time.Clock()  
        # Вызываем метод для создания объектов сцены
        self.create_objects()  


    def create_objects(self):
        # Создаем объект камеры с начальной позицией
        self.camera = Camera(self, [0.5, 1, -7])
        # Создаем объект проекции для отображения 3D объектов на экране
        self.projection = Projection(self)
        # Создаем 3D объект и устанавливаем его начальное положение
        self.object = Object3d(self)
        self.object.translate([0.2, 0.4, 0.2])
        # Создаем оси для текущего объекта и устанавливаем их положение
        self.axes = Axes(self)
        self.axes.translate([0.7, 0.9, 0.7])
        # Создаем мировые оси (относительно всей сцены), устанавливаем их положение и масштабируем
        self.world_axes = Axes(self)
        # Отключаем движение мировых осей
        self.world_axes.movement_flag = False  
        # Масштабируем мировые оси
        self.world_axes.scale(2.5)  
        # Устанавливаем их позицию очень близко к начальной
        self.world_axes.translate([0.0001, 0.0001, 0.0001])  


    def draw(self):
        # Заполняем экран темно-серым цветом (фон)
        self.screen.fill(pg.Color((33, 33, 33)))  
        # Отрисовываем мировые оси
        self.world_axes.draw()  
        # Отрисовываем оси объекта
        self.axes.draw()  
        # Отрисовываем сам объект
        self.object.draw()  


    def run(self):
        while True:
            # Вызываем метод для отрисовки всех объектов на экране
            self.draw() 
            # Обрабатываем ввод пользователя для управления камерой 
            self.camera.control()  
            # Проверяем события (например, закрытие окна)
            [exit() for i in pg.event.get() if i.type == pg.QUIT]  
             # Обновляем заголовок окна с текущим FPS
            pg.display.set_caption(str(self.clock.get_fps())) 
            # Обновляем экран (двойная буферизация)
            pg.display.flip()  
            # Ограничиваем FPS до заданного значения
            self.clock.tick(self.FPS)  


if __name__ == '__main__':
    app = SoftwareRender()
    app.run()