from rpi_animations.text_animator import TextAnimator
import sys
import os

if __name__ == '__main__':
    # Set the settings files name. In future versions, might be able to customise this.
    settings_file = 'settings.json'

    # Get the execution path, required for finding resources
    resources = os.path.join(sys.path[0], 'inputs')

    # Create the text animator
    text_animator = TextAnimator(resources, settings_file)

    # Set the animator running
    text_animator.run()
