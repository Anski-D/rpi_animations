from rpi_animations.text_animator import TextAnimator
import sys
import os
import argparse


def get_args():
    # Determine any arguments set
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', help='run the program in debug mode', action='store_true')
    parser.add_argument(
        'settings',
        help='(optional) filename of settings JSON, defaults to \'settings.json\'',
        type=str,
        default='settings.json',
        nargs='?'
    )
    return parser.parse_args()


if __name__ == '__main__':
    # Get arguments
    args = get_args()

    # Get the execution path, required for finding resources
    resources = os.path.join(sys.path[0], 'inputs')

    # Create the text animator
    text_animator = TextAnimator(resources, args.settings, args.debug)

    # Set the animator running
    text_animator.run()
