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
    'version': '0.2.0',
    'description': 'Package for recognizing registration plates',
    'long_description': None,
    'author': 'Szymon Cader',
    'author_email': 'szymon.sc.cader@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
