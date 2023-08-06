import argparse

from os import getcwd, mkdir
from os.path import join, dirname, abspath, exists
from pathlib import Path

from svgout import __version__
from svgout.manipulator import Manipulator


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-o",
        "--output-dir",
        help=(
            "SVG files created into this directory, default: creates `dist` "
            "directory beside the `input_file`"
        ),
    )
    parser.add_argument(
        "-i",
        "--input-file",
        help=(
            "Input SVG file path, default: trying to find first SVG file in "
            "current path"
        ),
    )
    parser.add_argument(
        "-c",
        "--config-file",
        help="svgout YAML config path, default: `{input_file}.svgout.yml`",
    )
    args = parser.parse_args()
    print("svgout", __version__)
    input_file = args.input_file
    if not args.input_file:
        cwd = getcwd()
        for item in Path(cwd).iterdir():
            if item.is_file() and str(item).endswith(".svg"):
                input_file = str(item)
                break
    else:
        input_file = abspath(input_file)

    if not input_file:
        raise ValueError("Cannot find any SVG file")

    config_file = args.config_file
    if not config_file:
        config_file = join(
            dirname(input_file), input_file[:-4] + ".svgout.yml"
        )
    else:
        config_file = abspath(config_file)

    if not config_file:
        raise ValueError("Cannot find svgout config file")

    output_dir = args.output_dir
    if not output_dir:
        output_dir = join(dirname(input_file), "dist")

    if not exists(output_dir):
        try:
            mkdir(output_dir)
            print("output directory created")
        except Exception:
            raise ValueError("Destination directory not found")

    print("Processing...")
    m = Manipulator(config_file, input_file)
    m.process(output_dir)
    print("Done")
