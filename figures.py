from typing import Tuple, List
import pygame
from pygame import Color, Surface
import abc


# define types
Position = Tuple[int, int]


class Figure(abc.ABC):

    def __init__(self, position: Position, color: Color):
        self.position = position
        self.color = color

    @abc.abstractmethod
    def draw(self, screen: Surface):
        pass


class Point(Figure):

    def draw(self, screen: Surface):
        screen.set_at(self.position, self.color)


class Circle(Figure):

    def __init__(self, position: Position, radius: int, color: Color):
        super().__init__(position, color)
        self.radius = radius

    def draw(self, screen: Surface):
        pygame.draw.circle(screen, self.color, self.position, self.radius)


class Rectangle(Figure):

    def __init__(self, position: Position, width: int, height: int, color: Color):
        super().__init__(position, color)
        self.width = width
        self.height = height

    def draw(self, screen: Surface):
        pygame.draw.rect(screen, self.color, self.position + (self.width, self.height))


class Square(Rectangle):

    def __init__(self, position: Position, size: int, color: Color):
        super().__init__(position, size, size, color)


class Polygon(Figure):

    def __init__(self, position: Position, points: List[Position], color: Color):
        super().__init__(position, color)
        self.points = points

    def draw(self, screen: Surface):
        pygame.draw.polygon(screen, self.color, [(self.position[0] + p[0], self.position[1] + p[1]) for p in self.points])
