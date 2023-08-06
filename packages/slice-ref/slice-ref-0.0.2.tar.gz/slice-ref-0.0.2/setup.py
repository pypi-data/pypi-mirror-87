# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['listy']
setup_kwargs = {
    'name': 'slice-ref',
    'version': '0.0.2',
    'description': "Reference implementation of Python's list slicing resolution",
    'long_description': "## Python Slicing Reference\n\nPython's builtin `list` type allows one to pass in slices\nto get, set or delete a range of elements.\n\n```python\n>>> my_list = ['a', 'b','c']\n>>> my_list[0:2]\n['a', 'b']\n>>> my_list[0:3:2]\n['a', 'b']\n>>> my_list[1:3] = [1, 2]\n>>> my_list\n['a', 1, 2]\n>>> my_list[::-1] = ['z', 'y', 'x']\n>>> my_list\n['x', 'y', 'z']\n```\n\nThe slice notation using colons is infact a `slice` builtin,\nwhere `start:stop:step` is equivalent to `slice(start, stop, step)`.\nThis looks an awful lot like the `range(start, stop, step)` builtin,\nbut 1-to-1 translating slices to ranges is not always appropiate.\n\nI have created this package as a reference implementation of `list`,\nspecifically to educate on how it deals with slices.\nI use [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) \nto test my custom class `listy` against Python's very own `list`,\nhopefully ensuring that all situations where slicing is involved\nis perfectly emulated.\n",
    'author': 'Matthew Barber',
    'author_email': 'quitesimplymatt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Honno/py-slicing-reference',
    'py_modules': modules,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
