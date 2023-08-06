# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['platonic_io']

package_data = \
{'': ['*'], 'platonic_io': ['models/*']}

install_requires = \
['Pillow>=8.0.1,<9.0.0',
 'click>=7.1.2,<8.0.0',
 'imageio-ffmpeg>=0.4.2,<0.5.0',
 'imageio>=2.9.0,<3.0.0',
 'keras>=2.4.3,<3.0.0',
 'matplotlib>=3.3.3,<4.0.0',
 'numpy>=1.18.4,<2.0.0',
 'openalpr>=1.1.0,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'pytesseract>=0.3.6,<0.4.0',
 'sklearn>=0.0,<0.1',
 'tensorflow>=2.3.1,<3.0.0',
 'tk>=0.1.0,<0.2.0']

extras_require = \
{'test': ['pytest>=6.1.2,<7.0.0', 'pytest-cov>=2.10.1,<3.0.0']}

entry_points = \
{'console_scripts': ['platonic-io = platonic_io.cli:main']}

setup_kwargs = {
    'name': 'platonic-io',
    'version': '0.2.1',
    'description': 'Package for recognizing registration plates',
    'long_description': '# Platonic-io\n\n[![PyPI version](https://badge.fury.io/py/platonic-io.svg)](https://badge.fury.io/py/platonic-io)\n![Test](https://github.com/nekeal/platonic-io/workflows/Test/badge.svg?branch=PLC-1_setup_project&event=push)\n![Quality](https://github.com/nekeal/platonic-io/workflows/Quality/badge.svg?branch=PLC-1_setup_project)\n[![Documentation Status](https://readthedocs.org/projects/platonic-io/badge/?version=stable)](https://platonic-io.readthedocs.io/en/latest/?badge=stable)\n![PyPI - Implementation](https://img.shields.io/pypi/implementation/platonic-io)\n\nPython package for text recognition of registration plates .\n\n-   Free software: MIT license\n-   Documentation: [Readthedocs](https://platonic-io.readthedocs.io/en/stable/)\n\n## Features\n\n- Reading text from single license plate.\n- Graphical user interface\n- License plates detection\n- Generating video with marked license plates\n\n## Installation\n[Installation](docs/installation.md)\n\n## Contributing\n[Contributing](CONTRIBUTING.md)\n\n## Authors\n\nMain authors of package:\n* Szymon Cader <szymon.sc.cader@gmail.com>\n* Patryk Kawa <kawapatryk99@gmail.com>\n* Bartosz Rudnicki <bartek@rudnicki.szczecin.pl>\n\n## Contributors\nNone yet. Why not be the first?\n',
    'author': 'Szymon Cader',
    'author_email': 'szymon.sc.cader@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nekeal/platonic-io/tree/minor_corrections',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
