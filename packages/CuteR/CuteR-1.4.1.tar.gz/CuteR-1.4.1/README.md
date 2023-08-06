# CuteR
Combine QRCode with picture

## Sample

Commands:

```bash
CuteR -c 10 -e H -o sample_output.png -v 10 sample_input.png http://www.chinuno.com
CuteR -C -r 100 50 100 188 sample_input.png http://www.chinuno.com #colourful mode
```
### Input

![image](https://github.com/chinuno-usami/CuteR/raw/master/sample_input.png)

### Output

![image](https://github.com/chinuno-usami/CuteR/raw/master/sample_output.png)

### Output (colourful mode)

![image](https://github.com/chinuno-usami/CuteR/raw/master/sample_output_colourful.png)

## Install

### Install via pip

`CuteR` is distributed on [PyPI](https://pypi.python.org/pypi/CuteR) now.
```bash
$ pip install CuteR
```

### Git clone

```bash
$ git clone https://github.com/chinuno-usami/CuteR.git
```
### Download from GitHub

Download [zip archive](https://github.com/chinuno-usami/CuteR/archive/master.zip) and unzip

## Usage

### As python module

```python
from CuteR import CuteR as cr
output = cr.produce(text,image)
```

arguments:

      :txt: QR text
      :img: Image
      :ver: QR version
      :err_crt: QR error correct
      :bri: Brightness enhance
      :cont: Contrast enhance
      :colourful: If colourful mode
      :rgba: color to replace black
      :pixelate: pixelate
      :returns: Produced image

### As command tool

usage:
```
CuteR.py [-h] [-o OUTPUT] [-v VERSION] [-e {Q,H,M,L}] [-b BRIGHTNESS]
                [-c CONTRAST] [-C] [-r R G B A] [-p]
                image text

Combine your QR code with custom picture

positional arguments:
  image
  text                  QRcode Text.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Name of output file.
  -v VERSION, --version VERSION
                        QR version.In range of [1-40]
  -e {Q,H,M,L}, --errorcorrect {Q,H,M,L}
                        Error correct
  -b BRIGHTNESS, --brightness BRIGHTNESS
                        Brightness enhance
  -c CONTRAST, --contrast CONTRAST
                        Contrast enhance
  -C, --colourful       colourful mode
  -r R G B A, --rgba R G B A
                        color to replace black
  -p, --pixelate        pixelate

```
## Dependencies
- Python
- qrcode
- PIL or Pillow

## License
GPLv3
