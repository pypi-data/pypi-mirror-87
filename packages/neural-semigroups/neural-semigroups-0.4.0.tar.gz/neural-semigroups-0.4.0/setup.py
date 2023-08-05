# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neural_semigroups']

package_data = \
{'': ['*']}

install_requires = \
['pandas', 'pytorch-ignite', 'tensorboard', 'torch', 'tqdm']

setup_kwargs = {
    'name': 'neural-semigroups',
    'version': '0.4.0',
    'description': 'Neural networks powered research of semigroups',
    'long_description': "[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/inpefess/neural-semigroups/blob/master/examples/train_a_model.ipynb) [![PyPI version](https://badge.fury.io/py/neural-semigroups.svg)](https://badge.fury.io/py/neural-semigroups) [![CircleCI](https://circleci.com/gh/inpefess/neural-semigroups.svg?style=svg)](https://circleci.com/gh/inpefess/neural-semigroups) [![Documentation Status](https://readthedocs.org/projects/neural-semigroups/badge/?version=latest)](https://neural-semigroups.readthedocs.io/en/latest/?badge=latest) [![codecov](https://codecov.io/gh/inpefess/neural-semigroups/branch/master/graph/badge.svg)](https://codecov.io/gh/inpefess/neural-semigroups)\n\n# Neural Semigroups\n\nHere we try to model Cayley tables of semigroups using neural networks.\n\nThe simplest way to get started is to [use Google Colaboratory](https://colab.research.google.com/github/inpefess/neural-semigroups/blob/master/examples/train_a_model.ipynb)\n\nMore documentation can be found \n[here](https://neural-semigroups.readthedocs.io).\n\n## Motivation\n\nThis work was inspired by [a sudoku\nsolver](https://github.com/Kyubyong/sudoku). A solved Sudoku puzzle\nis nothing more than a Cayley table of a quasigroup from 9 items with\nsome well-known additional properties. So, one can imagine a puzzle\nmade from a Cayley table of any other magma, e. g. a semigroup, by\nhiding part of its cells.\n\nThere are two major differences between sudoku and puzzles based on\nsemigroups:\n\n1) it's easy to take a glance on a table to understand whether it is\na sudoku or not. That's why it was possible to encode numbers in a\ntable cells as colour intensities. Sudoku is a picture, and a\nsemigroup is not. It's difficult to check a Cayley table's\nassociativity with a naked eye;\n\n2) sudoku puzzles are solved by humans for fun and thus catalogued.\nWhen solving a sudoku one knows for sure that there is a unique\nsolution. On the contrary, nobody guesses values in a partially\nfilled Cayley table of a semigroup as a form of amuzement. As a\nresult, one can create a puzzle from a full Cayley table of a\nsemigroup but there may be many distinct solutions.\n",
    'author': 'Boris Shminke',
    'author_email': 'boris@shminke.ml',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/inpefess/neural-semigroups',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
