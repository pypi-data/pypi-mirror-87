from setuptools import setup, find_packages


def read_version(module_name):
    from re import match, S
    from os.path import join, dirname

    with open(join(dirname(__file__), module_name, "__init__.py")) as f:
        return match(r".*__version__.*('|\")(.*?)('|\")", f.read(), S).group(2)


setup(
    name="svgout",
    version=read_version("svgout"),
    description="Manipulate SVG elements and export variations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="http://github.com/meyt/svgout",
    author="Mahdi Ghane.g",
    license="MIT",
    keywords="svg",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries",
    ],
    install_requires=[
        "pyyaml==5.3.1",
        "lxml==4.6.2",
        "beautifulsoup4==4.9.3",
        "cssutils==1.0.2"
    ],
    entry_points={"console_scripts": ["svgout = svgout.cli:main"]},
)
