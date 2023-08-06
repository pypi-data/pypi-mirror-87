import re
import yaml
import logging
import cssutils

from os.path import join
from bs4 import BeautifulSoup


cssutils.log.setLevel(logging.CRITICAL)


class ElementStyle:
    def __init__(self, bs_element):
        self.el = bs_element
        self.style = cssutils.parseStyle(self.el["style"])

    def __getitem__(self, key):
        return self.style[key]

    def __setitem__(self, key, val):
        self.style[key] = val
        self.el["style"] = self.style.cssText

    def __delitem__(self, key):
        self.style.removeProperty(key)
        self.el["style"] = self.style.cssText


class Element:
    def __init__(self, bs_element):
        self.el = bs_element

    @property
    def style(self):
        return ElementStyle(self.el)

    def hide(self):
        self.style["display"] = "none"

    def show(self):
        del self.style["display"]


class Manipulator:
    def __init__(self, config_filename: str, svg_filename: str):
        with open(config_filename, "r") as f:
            self.config = yaml.load(f, Loader=yaml.Loader)

        with open(svg_filename, "r") as f:
            self.bs = BeautifulSoup(f.read(), "xml")

    def save(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(self.bs))

    def process(self, output_dir: str, stdout: bool = True):
        config = self.config
        bs = self.bs
        for outkey, outval in config.items():
            output_filename = join(output_dir, outkey + ".svg")
            if stdout:
                print(output_filename)
            for command, elementpatterns in outval.items():
                for elementpattern in elementpatterns:
                    elements = bs.findAll(id=re.compile(elementpattern))
                    for bs_element in elements:
                        el = Element(bs_element)
                        getattr(el, command)()
            self.save(output_filename)
