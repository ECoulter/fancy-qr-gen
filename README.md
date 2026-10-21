# Fancy-QR-Gen

![Example-QR](./Example_QR.svg)

This is just a simple python script that uses the fantastic qr-code library with some flags to control
colors and logo placement. Basically some bits to make it easy to clone and generate your own pretty QR codes.

Mix of Human and AI development, docs are fully hand-crafted by a human.

# Setup

Right now this just requires two libraries - [pillow](https://pypi.org/project/pillow/) for image generation and the [python-qrcode](https://github.com/lincolnloop/python-qrcode) library.
Versions are probably flexible, but I used `pip freeze` to generate `requirements.txt`.

* `git clone https://github.com/ECoulter/fancy-qr-gen`
* `cd fancy-qr-gen`
* `python -m venv ./logo-gen`
* `pip install -r ./requirements.txt`
* `source ./logo-gen/bin/activate`

# Usage

* `source ./logo-gen/bin/activate`
* Grab a logo: `wget https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg`
* `./gen_qr.py 'https://github.com/ECoulter/fancy-qr-gen' "./Octicons-mark-github.svg" -o Example_QR.svg --qr-color "#051E39" --border-color "#B39051" --logo-backg-color "#000000" --backg-color "#000000"`

# Advice

It's very helpful to have an svg logo with a transparent background! 
These do work in "dark mode" with a dark background and light qr-color.

# Additional flags

Thanks to the argparse library, we have a nice list of flags handy:

```
./gen_qr.py --help

usage: gen_qr.py [-h] [-o OUTPUT] [--logo-size LOGO_SIZE] [--qr-color QR_COLOR] [--logo-backg-color LOGO_BACKG_COLOR]
                 [--backg-color BACKG_COLOR] [--border-color BORDER_COLOR]
                 url logo_svg

Generate SVG QR code with embedded SVG logo.


positional arguments:
  url                   URL or text to encode
  logo_svg              Path to SVG logo

options:
  -h, --help            show this help message and exit
  -o, --output OUTPUT   Output SVG filename
  --logo-size LOGO_SIZE
                        Fraction of QR width occupied by logo (default: 0.20)
  --qr-color QR_COLOR   SVG QR code fill color
  --logo-backg-color LOGO_BACKG_COLOR
                        SVG QR code Logo background color
  --backg-color BACKG_COLOR
                        SVG QR code background color
  --border-color BORDER_COLOR
                        SVG QR code border color
```
