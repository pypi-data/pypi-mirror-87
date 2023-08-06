# ipyd3

[![Version](https://img.shields.io/pypi/v/ipyd3.svg)](https://pypi.python.org/pypi/ipyd3)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gl/teia_engineering%2Fipyd3/master?filepath=examples)
[![Documentation Status](http://readthedocs.org/projects/ipyd3/badge/?version=latest)](https://ipyd3.readthedocs.io/)

Library for visualizing d3 inside Jupyter

## Installation

To install use pip:

    $ pip install ipyd3
    $ jupyter nbextension enable --py --sys-prefix ipyd3

To install for jupyterlab

    $ jupyter labextension install ipyd3

For a development installation (requires npm),

    $ git clone https://github.com//ipyd3.git
    $ cd ipyd3
    $ pip install -e .
    $ jupyter nbextension install --py --symlink --sys-prefix ipyd3
    $ jupyter nbextension enable --py --sys-prefix ipyd3
    $ jupyter labextension install js

When actively developing your extension, build Jupyter Lab with the command:

    $ jupyter lab --watch

This takes a minute or so to get started, but then automatically rebuilds JupyterLab when your javascript changes.

Note on first `jupyter lab --watch`, you may need to touch a file to get Jupyter Lab to open.
