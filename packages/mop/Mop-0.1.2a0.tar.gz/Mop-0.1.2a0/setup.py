# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mop', 'mop.editor']

package_data = \
{'': ['*']}

install_requires = \
['PyGObject>=3.38.0', 'eyeD3[art-plugin]>=0.9.5', 'nicfit.py>=0.8.6']

entry_points = \
{'console_scripts': ['mop = mop.__main__:main']}

setup_kwargs = {
    'name': 'mop',
    'version': '0.1.2a0',
    'description': 'MPEG ID3 tagger using Python, eyeD3, and GTK+',
    'long_description': '\n\n.. image:: https://img.shields.io/pypi/v/eyeD3\n   :target: https://img.shields.io/pypi/v/eyeD3\n   :alt: \n\n\n.. image:: https://img.shields.io/pypi/pyversions/eyeD3\n   :target: https://img.shields.io/pypi/pyversions/eyeD3\n   :alt: \n\n\n.. image:: https://img.shields.io/pypi/l/eyeD3\n   :target: https://img.shields.io/pypi/l/eyeD3\n   :alt: \n\n\nMop\n===\n\nGTK+ ID3 tag editor.\nSupports ID3 v2.4, v2.3, v2.2 (read-only), and v1.x tags.\n\n\n.. image:: https://github.com/nicfit/Mop/raw/master/screenshot.png\n   :target: https://github.com/nicfit/Mop/raw/master/screenshot.png\n   :alt: Screenshot\n\n\nInstallation\n------------\n\nInstall via pip:\n\n.. code-block::\n\n   pip install Mop\n\n\nClone from GitHub:\n\n.. code-block::\n\n   git clone https://github.com/nicfit/Mop.git\n   cd Mop\n   pip install -e .\n\n\n\nUsage\n-----\n\nRun ``mop`` with no options will open a file dialog allowing you to select file or\ndirectories.  Alternatively files can be specified on the command line.\n\n.. code-block::\n\n   mop "./Hawkwind/1973 - Space Ritual/"\n\n\n\nAcknowledgements\n----------------\n\nMop\'s user interface is heavily inspired by `easytag <https://gitlab.gnome.org/GNOME/easytag>`_.\n\nLicense\n-------\n\n.. code-block::\n\n   Copyright (C) 2020 Travis Shirk\n\n   This program is free software: you can redistribute it and/or modify\n   it under the terms of the GNU General Public License as published by\n   the Free Software Foundation, either version 3 of the License, or\n   (at your option) any later version.\n\n   This program is distributed in the hope that it will be useful,\n   but WITHOUT ANY WARRANTY; without even the implied warranty of\n   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n   GNU General Public License for more details.\n',
    'author': 'Travis Shirk',
    'author_email': 'travis@pobox.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nicfit/Mop',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
