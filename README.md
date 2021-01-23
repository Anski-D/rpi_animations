# rpi_animations

Raspberry Pi Python package to display scrolling messages selected at random from provided list, as well as images constantly moving position. While developed for a Raspberry Pi display, it should work on any device. Package developed on Windows.

## Installation

Setup a new virtual environment in your installation directory, activate virtual environment, then install package.

Example setup of virtual environment if using `venv`:
```
python -m venv .venv
```

Activate virtual environment (Windows example):
```cmd
.venv\Scripts\activate
```

Activate virtual environment (Linux example):
```bash
source .venv/bin/activate
```

Install package:
```
pip install rpi_animations
``` 

## Usage

Words.

```json
{
  "colours": "0,0,255;0,255,0;255,0,0",
  "text": "MESSAGE 1!;MESSAGE 2!;MESSAGE 3!",
  "message_sep": "   ",
  "typeface": "Serif Regular",
  "text_size": 350,
  "text_speed": 8,
  "outline_width": 3,
  "outline_colours": "255,255,255;0,0,0",
  "image_sources": "example1.bmp;example2.bmp;example3.bmp",
  "num_images": 5,
  "image_change_time": 2,
  "colour_change_time": 15,
  "fps": 30
}
```
colours
: Definition

text
: Definition

message_sep
: Definition

typeface
: Definition

text_size
: Definition

text_speed
: Definition

outline_width
: Definition

outline_colours
: Definition

image_sources
: Definition

num_images
: Definition

image_change_time
: Definition

colour_change_time
: Definition

fps
: Definition