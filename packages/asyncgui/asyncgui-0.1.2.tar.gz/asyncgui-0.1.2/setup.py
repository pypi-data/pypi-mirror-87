# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['asyncgui', 'asyncgui.adaptor']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'asyncgui',
    'version': '0.1.2',
    'description': 'async library that works on top of an existing gui event loop',
    'long_description': '# AsyncGui\n\nAn async library that works on top of an existing gui event loop.\nThis is not for application developers, but for async-library developers.\n\n## Async-libraries who use this\n\n- [asynckivy](https://github.com/gottadiveintopython/asynckivy)\n- [asynctkinter](https://github.com/gottadiveintopython/asynctkinter)\n\n## TODO\n\n- `or_()` が中斷/完了のどちらか片方だけを待てるようにする\n- `Trio` -> `asyncgui` 方向へのadaptor\n\n',
    'author': 'Nattōsai Mitō',
    'author_email': 'flow4re2c@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gottadiveintopython/asyncgui',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
