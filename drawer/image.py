from typing import Dict, List
import json
import re

from pygame import Color, Surface

from .figures import Figure, Circle, Polygon, Square, Rectangle, Point


Palette = Dict[str, Color]


class Image:

    def __init__(self, width: int, height: int, background: Color = Color('white')):
        self.width = width
        self.height = height
        self.background = background
        self.figures = []

    def draw(self, screen: Surface, x: int = 0, y: int = 0):
        screen.fill(self.background, (x, y, self.width, self.height))

        for fig in self.figures:
            fig.draw(screen)


def load_image(file: str) -> Image:
    data = json.load(open(file, "r"))

    # parse file
    palette = _parse_palette(data['Palette'])
    figures = _parse_figures(data['Figures'], palette)
    width = data['Screen']['width']
    height = data['Screen']['height']
    background = _parse_color(data['Screen']['bg_color'], palette)

    # create image
    img = Image(width, height, background)
    img.figures = figures

    return img


def _parse_palette(palette: dict) -> Palette:
    return {k: _parse_color(v) for k, v in palette.items()}


def _parse_color(color, palette: Dict[str, Color] = {}) -> Color:
    if color in palette:
        return palette[color]

    if isinstance(color, str):
        match = re.fullmatch('\((\d+),(\d+),(\d+)\)', color)
        if match is not None:
            return Color(int(match.group(1)), int(match.group(2)), int(match.group(3)))

    return Color(color)


def _parse_figures(figures: List[dict], palette: Dict[str, Color]) -> List[Figure]:
    result = []

    for fig in figures:

        color = Color('black')
        position = (0, 0)

        if 'color' in fig:
            color = _parse_color(fig['color'], palette)
        if 'x' in fig:
            position = (fig['x'], position[1])
        if 'y' in fig:
            position = (position[0], fig['y'])

        if fig['type'] == 'point':
            result.append(Point(position, color))

        elif fig['type'] == 'circle':
            result.append(Circle(position, fig['radius'], color))

        elif fig['type'] == 'rectangle':
            result.append(Rectangle(position, fig['width'], fig['height'], color))

        elif fig['type'] == 'square':
            result.append(Square(position, fig['size'], color))

        elif fig['type'] == 'polygon':
            result.append(Polygon(position, fig['points'], color))

    return result
