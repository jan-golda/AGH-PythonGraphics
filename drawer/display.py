from typing import Tuple

import pygame

from .image import Image


def init(title: str = "Display", resolution: Tuple[int, int] = (0, 0)):
    pygame.init()
    pygame.display.set_mode(resolution)
    pygame.display.set_caption(title)


def get_screen() -> pygame.Surface:
    return pygame.display.get_surface()


def draw_image(img: Image):
    img.draw(get_screen())
    pygame.display.update()


def save_screen_to_file(file: str):
    pygame.image.save(get_screen(), file)


def wait_for_close():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
