import argparse

from drawer import display, load_image


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

    # load image
    img = load_image(args.file)

    # setup display
    display.init(args.file, (img.width, img.height))

    # draw image
    display.draw_image(img)

    # save screen
    if args.output is not None:
        display.save_screen_to_file(args.output)

    # wait for screen
    display.wait_for_close()
