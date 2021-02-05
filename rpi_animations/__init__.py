from rpi_animations.screen_animator import ScreenAnimator
import argparse


def get_args():
    # Determine any arguments set
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help='run the program in debug mode', action='store_true')
    parser.add_argument('-f', '--fps', help='add fps counter', action='store_true')
    parser.add_argument(
        '-s', '--settings',
        help='filename of settings JSON, defaults to "settings.json"',
        type=str,
        default='settings.json',
        nargs='?'
    )
    return parser.parse_args()


def main():
    # Get arguments
    args = get_args()

    # Create the text animator
    screen_animator = ScreenAnimator(args.settings, args.debug, args.fps)

    # Set the animator running
    screen_animator.run()
