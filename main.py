from typing import Dict, List
import json
import argparse
import re

import pygame
from pygame import Color, Surface

from figures import Figure, Point, Circle, Rectangle, Square, Polygon


def draw_from_file(input_file: str, output_file: str = None):
    # parse data
    data = json.load(open(input_file, "r"))

    # parse color palette
    palette = _parse_palette(data['Palette'])

    # parse figures
    figures = _parse_figures(data['Figures'], palette)

    # setup screen
    screen = __setup_screen(data['Screen'], palette)

    # set screen title
    pygame.display.set_caption("Visualization of: " + input_file)

    # draw figures
    for fig in figures:
        fig.draw(screen)

    # update display
    pygame.display.update()

    # save to file if output file is provided
    if output_file is not None:
        _save_to_file(screen, output_file)

    # wait for window to be closed
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


def __setup_screen(options: dict, palette: Dict[str, Color]) -> Surface:
    pygame.init()
    screen = pygame.display.set_mode((options['width'], options['height']))
    screen.fill(_parse_color(options['bg_color'], palette))
    return screen


def _parse_palette(palette: dict) -> Dict[str, Color]:
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

        color = Color(0, 0, 0)
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


def _save_to_file(screen: Surface, output_file: str):
    pygame.image.save(screen, output_file)


def _parse_cmd_line() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Draws 2D graphics defined in json file.')

    # json file
    parser.add_argument(
        "file",
        type=str,
        help='Json file containing description of graphics to display'
    )

    # flag if output to file
    parser.add_argument(
        '-o', '--output',
        type=str,
        help='File to which created graphics will be saved'
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_cmd_line()
    draw_from_file(args.file, args.output)
