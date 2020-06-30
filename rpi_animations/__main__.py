from rpi_animations.text_animator import TextAnimator

if __name__ == '__main__':
    # Message to display
    message_file = 'message.json'

    # Create the text animator
    text_animator = TextAnimator(message_file)

    # Set the animator running
    text_animator.run()
