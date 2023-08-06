# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quickchart']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'quickchart.io',
    'version': '0.1.3',
    'description': 'A client for quickchart.io, a service that generates static chart images',
    'long_description': '# quickchart-python\n[![Build Status](https://travis-ci.com/typpo/quickchart-python.svg?branch=master)](https://travis-ci.com/typpo/quickchart-python)\n\nA Python client for the [quickchart.io](https://quickchart.io/) image charts web service.\n\n# Installation\n\nUse the `quickchart.py` library in this project, or install through [pip](https://pypi.org/project/quickchart.io/):\n\n```\npip install quickchart.io\n```\n\n# Usage\n\nThis library provides a `QuickChart` class.  Import and instantiate it.  Then set properties on it and specify a [Chart.js](https://chartjs.org) config:\n\n```python\nfrom quickchart import QuickChart\n\nqc = QuickChart()\nqc.width = 500\nqc.height = 300\nqc.device_pixel_ratio = 2.0\nqc.config = {\n    "type": "bar",\n    "data": {\n        "labels": ["Hello world", "Test"],\n        "datasets": [{\n            "label": "Foo",\n            "data": [1, 2]\n        }]\n    }\n}\n```\n\nUse `get_url()` on your quickchart object to get the encoded URL that renders your chart:\n\n```python\nprint(qc.get_url())\n# https://quickchart.io/chart?c=%7B%22chart%22%3A+%7B%22type%22%3A+%22bar%22%2C+%22data%22%3A+%7B%22labels%22%3A+%5B%22Hello+world%22%2C+%22Test%22%5D%2C+%22datasets%22%3A+%5B%7B%22label%22%3A+%22Foo%22%2C+%22data%22%3A+%5B1%2C+2%5D%7D%5D%7D%7D%7D&w=600&h=300&bkg=%23ffffff&devicePixelRatio=2.0&f=png\n```\n\nIf you have a long or complicated chart, use `get_short_url()` to get a fixed-length URL using the quickchart.io web service (note that these URLs only persist for a short time unless you have a subscription):\n\n```python\nprint(qc.get_short_url())\n# https://quickchart.io/chart/render/f-a1d3e804-dfea-442c-88b0-9801b9808401\n```\n\nThe URLs will render an image of a chart:\n\n<img src="https://quickchart.io/chart?c=%7B%22type%22%3A+%22bar%22%2C+%22data%22%3A+%7B%22labels%22%3A+%5B%22Hello+world%22%2C+%22Test%22%5D%2C+%22datasets%22%3A+%5B%7B%22label%22%3A+%22Foo%22%2C+%22data%22%3A+%5B1%2C+2%5D%7D%5D%7D%7D&w=600&h=300&bkg=%23ffffff&devicePixelRatio=2.0&f=png" width="500" />\n\n## Customizing your chart\n\nYou can set the following properties:\n\n### config: dict or str\nThe actual Chart.js chart configuration.\n\n### width: int\nWidth of the chart image in pixels.  Defaults to 500\n\n### height: int\nHeight of the chart image  in pixels.  Defaults to 300\n\n### format: str\nFormat of the chart. Defaults to png. svg is also valid.\n\n### background_color: str\nThe background color of the chart. Any valid HTML color works. Defaults to #ffffff (white). Also takes rgb, rgba, and hsl values.\n\n### device_pixel_ratio: float\nThe device pixel ratio of the chart. This will multiply the number of pixels by the value. This is usually used for retina displays. Defaults to 1.0.\n\n## Getting URLs\n\nThere are two ways to get a URL for your chart object.\n\n### get_url(): str\n\nReturns a URL that will display the chart image when loaded.\n\n### get_short_url(): str\n\nUses the quickchart.io web service to create a fixed-length chart URL that displays the chart image.  Returns a URL such as `https://quickchart.io/chart/render/f-a1d3e804-dfea-442c-88b0-9801b9808401`.\n\nNote that short URLs expire after a few days for users of the free service.  You can [subscribe](https://quickchart.io/pricing/) to keep them around longer.\n\n## Other functionality\n\n### get_bytes()\n\nReturns the bytes representing the chart image.\n\n### to_file(path: str)\n\nWrites the chart image to a file path.\n\n## More examples\n\nCheckout the `examples` directory to see other usage.\n',
    'author': 'Ian Webster',
    'author_email': 'ianw_pypi@ianww.com',
    'maintainer': 'Ian Webster',
    'maintainer_email': 'ianw_pypi@ianww.com',
    'url': 'https://quickchart.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
