from rpi_animations.text_animator import TextAnimator
import sys

if __name__ == '__main__':
    # Set the settings files name. In future versions, might be able to customise this.
    settings_file = 'settings.json'

    # Get the execution path, required for finding resources
    resources = sys.path[0]

    # Create the text animator
    text_animator = TextAnimator(resources, settings_file)

    # Set the animator running
    text_animator.run()
