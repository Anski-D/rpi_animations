import pygame
import json


class Message:
    def __init__(self, text_animator: object, message_file: str):
        # Save the text animator
        self.text_animator = text_animator

        # Load the message from the json file
        self._load_message(message_file)

    def _load_message(self, message_file: str):
        message = self._load_json(message_file)

        # Split the dictionary
        self.bg_colour = tuple(map(int, message['bg_colour'].split(',')))
        self.text_colour = tuple(map(int, message['text_colour'].split(',')))
        self.text = message['text']

    @staticmethod
    def _load_json(message_file: str):
        # Open the json file safely
        with open(message_file) as msg_file:
            # Load the json
            return json.load(msg_file)
