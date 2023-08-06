# svgout

Manipulate SVG elements and export variations

## Install

On debian based distro:

```sh
sudo apt install libxml2-dev libxslt1-dev lib32z1-dev python3-dev
```

```sh
pip install svgout
```


## Usage

```txt
usage: svgout [-h] [-o OUTPUT_DIR] [-i INPUT_FILE] [-c CONFIG_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        SVG files created into this directory, default: creates `dist` directory beside the `input_file`
  -i INPUT_FILE, --input-file INPUT_FILE
                        Input SVG file path, default: trying to find first SVG file in current path
  -c CONFIG_FILE, --config-file CONFIG_FILE
                        svgout YAML config path, default: `{input_file}.svgout.yml`
```

## Configuration

Configuration structure in YAML format:

```yaml
OUTPUT_FILE_NAME:
  COMMAND:
    - ELEMENT_ID_REGEX
```

Example:
```yaml
first:
  hide:
    - element-1
    - element-2
  show:
    - element-3

second:
  hide:
    - element-*
  show:
    - element-3
```

That config will generate two file with names `first.svg` and `second.svg`.

Available commands:
  - hide
  - show
