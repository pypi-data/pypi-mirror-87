# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['yasod']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'numpy>=1.19.4,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'pydantic>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'yasod',
    'version': '0.1.1',
    'description': 'Yet another simple object detector',
    'long_description': '![CI Status](https://github.com/michdr/yasod/workflows/CI/badge.svg)\n[![PyPI version](https://img.shields.io/pypi/v/yasod)](https://pypi.org/project/yasod)\n\n# yasod\n<!--- Don\'t edit the version line below manually. Let bump2version do it for you. -->\n> Version 0.1.1 \n>\n> Yet another simple object detector\n\n## Installing\n```bash\npip install yasod\n``` \n\n## Getting started\nAn example for a config and models could be found in `tests/data`. \n\nHere is a simple example how to detect the objects of a given `input-image.jpg` and draw an output image accordingly:\n```python\nfrom yasod import Yasod\n\nmodel = Yasod("simple-yasod-config.yml").get_model("yolov4-tiny")\nimg, detections = model.detect("input-image.jpg")\nmodel.draw_results(img, detections, "output-image.jpg")\n``` \n',
    'author': 'Michael Druk',
    'author_email': '2467184+michdr@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/michdr/yasod',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
