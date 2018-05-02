from typing import Tuple, List
from abc import ABC, abstractmethod

from pygame import Color, Surface, gfxdraw


# define types
Position = Tuple[int, int]


class Figure(ABC):

    def __init__(self, position: Position, color: Color):
        self.position = position
        self.color = color

    @property
    def x(self) -> int:
        return self.position[0]

    @property
    def y(self) -> int:
        return self.position[1]

    @abstractmethod
    def draw(self, screen: Surface):
        pass


class Point(Figure):

    def draw(self, screen: Surface):
        gfxdraw.pixel(screen, self.x, self.y, self.color)


class Circle(Figure):

    def __init__(self, position: Position, radius: int, color: Color):
        super().__init__(position, color)
        self.radius = radius

    def draw(self, screen: Surface):
        gfxdraw.aacircle(screen, self.x, self.y, self.radius, self.color)
        gfxdraw.filled_circle(screen, self.x, self.y, self.radius, self.color)


class Rectangle(Figure):

    def __init__(self, position: Position, width: int, height: int, color: Color):
        super().__init__(position, color)
        self.width = width
        self.height = height

    def draw(self, screen: Surface):
        gfxdraw.box(screen, (self.x - self.width/2, self.y - self.height/2, self.width, self.height), self.color)


class Square(Rectangle):

    def __init__(self, position: Position, size: int, color: Color):
        super().__init__(position, size, size, color)


class Polygon(Figure):

    def __init__(self, position: Position, points: List[Position], color: Color):
        super().__init__(position, color)
        self.points = points

    def draw(self, screen: Surface):
        gfxdraw.aapolygon(screen, [(self.y + p[0], self.y + p[1]) for p in self.points], self.color)
        gfxdraw.filled_polygon(screen, [(self.x + p[0], self.y + p[1]) for p in self.points], self.color)

