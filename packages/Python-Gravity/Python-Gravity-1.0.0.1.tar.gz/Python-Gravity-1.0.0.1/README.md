# pygravity

![PyPI - Downloads](https://img.shields.io/pypi/dm/python-gravity)
![PyPI - License](https://img.shields.io/pypi/l/python-gravity)
![Libraries.io SourceRank](https://img.shields.io/librariesio/sourcerank/pypi/python-gravity?color=green)
![PyPI](https://img.shields.io/pypi/v/python-gravity)
![PyPI - Format](https://img.shields.io/pypi/format/python-gravity)
![GitHub last commit](https://img.shields.io/github/last-commit/gaming32/pygravity)
<!-- ![PyPI - Status](https://img.shields.io/pypi/status/python-gravity) -->
<!-- ![Dependents (via libraries.io)](https://img.shields.io/librariesio/dependents/pypi/python-gravity) -->
![Discord](https://img.shields.io/discord/673206188825116713?color=%237289DA&label=support&logo=discord&logoColor=white)

[Join the Discord channel for live tech support!](https://discord.com/channels/673206188825116713/783507379446087690)

pygravity is a library used for calculating gravity in Python.

## Installation

Either install from source: (Note that you will need a C compiler installed)
```shell
$ git clone https://github.com/gaming32/pygravity
$ cd pygravity
$ python setup.py install
```

Or install from pip:
```shell
$ python -m pip install pygravity
```

# Documentation

Pygravity is made up of a math module (`pygravity.math`) for generic gravity-related math, and a subpackage (`pygravity.twod`) for doing 2D calculations.

For in-depth documentation please install the package and use `pydoc` (`python -m pydoc -b`).

## pygravity.twod

This package has three lower-level modules for doing gravity math: `pygravity.twod.vector`, `pygravity.twod.physics`, and `pygravity.twod.gravity`.
It also provides two higher-level modules for doing simple math: `pygravity.twod.util` and `pygravity.twod.pygame_simulation`.
Most of `pygravity.twod.pygame_simulation` should be considered in beta and should not be used without examining it's code first.
