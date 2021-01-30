# rpi_animations

Raspberry Pi Python package to display scrolling messages selected at random from provided list, as well as images periodically moving position. While developed for a Raspberry Pi display, it should work on any device. Package developed on Windows.

## Installation

Setup a new virtual environment in your installation directory, activate virtual environment, then install package. Examples assume setup on a Raspberry Pi running Raspberry Pi OS.

Clone the git repository:
```bash
git clone https://github.com/Anski-D/rpi_animations.git
```

Move into the cloned git directory:
```bash
cd rpi_animations
```

Setup a virtual environment to isolate program. If using `venv`:
```
python3 -m venv .venv
```

Activate the virtual environment:
```bash
source .venv/bin/activate
```

Install the package:
```bash
pip install .
```

Make the `run.sh` script executable:
```bash
chmod +x run.sh
```

To get the program to run at startup, a systemd service needs to be added and registered. Using a text editor, add a service file to `/etc/systemd/system`, e.g. `/etc/systemd/system/rpi_animations.service`.

Add the following to the file:
```
[Unit]
Description=Run rpi_animations on display at startup
After=network.target

[Service]
ExecStart=<dir to run>/run.sh
WorkingDirectory=<dir to run>
StandardOutput=inherit
StandardError=inherit
Restart=always

[Install]
WantedBy=multi-user.target
```

Adjust `<dir to run>` to the *absolute* path to the location of program installation, where `run.sh` should be (e.g. `/home/pi/python-projects/rpi_animations`).

Enable the service:
```bash
sudo systemctl enable <service name>
```

Adjust `<service name>` to the service file name, e.g. `rpi_animations.service`.

Restart your Raspberry Pi.

## Usage

In the `inputs` directory, edit the `settings.json` file and then add the image files you want to use. The `settings.json` file has the following format:

```json
{
  "colours": "255,0,0;0,255,0;0,0,255",
  "messages": "EXAMPLE MESSAGE 1!;EXAMPLE MESSAGE 2!;EXAMPLE MESSAGE 3!;EXAMPLE MESSAGE 4!",
  "message_sep": "   ",
  "typeface": "Serif Regular",
  "text_size": 350,
  "bold_text": 1,
  "italic_text": 0,
  "text_aa": 0,
  "text_speed": 8,
  "outline_width": 3,
  "outline_colours": "0,0,0;255,255,255",
  "image_sources": "bday-cake.bmp;bday-hat.bmp;bday-present.bmp",
  "num_images": 10,
  "image_change_time": 2,
  "colour_change_time": 15,
  "fps": 30,
  "reposition_attempts": 50
}
```

colours
: Semicolon-separated list of colours that will be randomly selected and applied to the text and background. Colours will randomly alternate based on the time in `colour_change_time`. Background and message colour will always be different. 

messages
: Semicolon-separated list of messages that will be randomly selected to scroll across the screen. No whitespace is required before or after the message; message separation is controlled by the `message_sep` field.

message_sep
: A separator inserted between each randomly-selected message.

typeface
: Set the typeface to be used. At a python prompt, run `pygame.font.get_fonts()` to see available system fonts.

text_size
: Text height for scrolling text.

bold_text
: Sets the message text as bold. Should be set to 1 (True) or 0 (False).

italic_text
: Sets the message text as italic. Should be set to 1 (True) or 0 (False).

text_aa
: Turns message text anti-aliasing on or off. Can cause notable performance penalty with little visual benefit when activated on a Raspberry Pi 4B 4GB. Should be set to 1 (True) or 0 (False). 

text_speed
: Set the scrolling speed of the text. Value is approximately pixels per second, and should remain constant when fps is changed.

outline_width
: Sets a pixel width for the outline of the scrolling text.

outline_colours
: Semicolon-separated list of colours that will be randomly selected for the scrolling text outline. Only one colour is used per message.

image_sources
: Semicolon-separated list of images to display in the background, over which the text scrolls. List should just be the image filenames and extension. Images should be put in the `inputs` directory.

num_images
: Number of each image to be displayed. So if set to '10', 10 of each image will be rendered.

image_change_time
: Amount of time before the images are all randomly repositioned. Time is approximately in seconds.

colour_change_time
: Amount of time before the colours are changed by random. Time is approximately in seconds.

fps
: Frames per second rate at which the program should run. This helps maintain a consistent scroll speed as the message lengths vary. If the scroll speed appears to keep changing, try reducing this value.

reposition_attempts
: Number of times an individual image should be randomly repositioned to avoid collision with the other images.
