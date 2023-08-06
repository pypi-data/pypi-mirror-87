# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyliter', 'pyliter.resources']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'pyglet>=1.4.8,<2.0.0',
 'pyyaml>=5.2,<6.0',
 'typer>=0.3.2,<0.4.0',
 'webcolors>=1.11.1,<2.0.0']

entry_points = \
{'console_scripts': ['pyliter = pyliter.__main__:cli']}

setup_kwargs = {
    'name': 'pyliter',
    'version': '1.4.0',
    'description': 'Generate color syntax highlighted PNG image from python source files.',
    'long_description': 'pyliter - Python syntax highlighting\n====================================\n\n``pyliter`` is a Python 3 command-line tool that generates PNG files\nfrom python source. \n\n\nFeatures\n--------\n\n- syntax highlighting\n- PNG files\n- preview mode\n- OpenGL rendering using pyglet\n\nInstall\n-------\n\n::\n\n   $ pip install pyliter\n\n\n::\n\n   $ pip install git+https://github.com/JnyJny/pyliter\n\n\nUsage\n-----\n\n::\n\n   $ pyliter --help\n   Usage: pyliter [OPTIONS] [INPUT_FILE]\n   \n     Python syntax highlighting\n   \n     Renders syntax-highlighted text to PNG file and optional previews the\n     render in a window before saving.\n   \n     If the optional output path is omitted, preview is enabled.\n   \n   Options:\n     -o, --output-file PATH    Creates a PNG with the supplied path.\n     -l, --start-line INTEGER  Line number to begin display.  [default: 0]\n     -n, --line-count INTEGER  Number of lines to display.  [default: 10]\n     -N, --no-line-numbers     Disable line numbers in output.  [default: False]\n     -p, --preview             Previews output in window.  [default: False]\n     -t, --transparent         Write output PNG with transparency.  [default:\n                               False]\n     -s, --style-name TEXT     Style to apply to input file.  [default: default]\n     -f, --font-name TEXT      Font name.  [default: courier]\n     -S, --font-size INTEGER   Font size  [default: 24]\n     -L, --list-styles         List available styles and exits.\n     --version                 Show the version and exit.\n     --help                    Show this message and exit.\n\n\nExample\n-------\n\n.. image:: https://github.com/JnyJny/pyliter/blob/master/examples/screenshot.png\n\t   :width: 400\n\t   :alt: Super Awesome PNG Screenshot\n\n \n',
    'author': 'jnyjny',
    'author_email': 'erik.oshaughnessy@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JnyJny/pyliter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
