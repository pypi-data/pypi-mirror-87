# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trallnags_hello_python']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'trallnags-hello-python',
    'version': '0.2.0',
    'description': 'Just a test project',
    'long_description': '<!-- omit in toc -->\n# Hello Python\n\n[![Current Package Version](https://badge.fury.io/py/trallnags-hello-python.svg)](https://pypi.python.org/pypi/trallnags-hello-python)\n[![Maintenance](https://img.shields.io/badge/maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)\n[![Supported Python Versions](https://img.shields.io/pypi/pyversions/trallnags-hello-python.svg)](https://pypi.python.org/pypi/trallnags-hello-python)\n[![Downloads](https://pepy.tech/badge/trallnags-hello-python/month)](https://pepy.tech/project/trallnags-hello-python/month)\n[![docs](https://img.shields.io/badge/docs-here-blue)](https://trallnag.github.io/trallnags-hello-python/)\n\n![release](https://github.com/trallnag/hello-python/workflows/release/badge.svg)\n![commit](https://github.com/trallnag/hello-python/workflows/commit/badge.svg)\n[![Code Coverage with Codecov](https://codecov.io/gh/trallnag/trallnags-hello-python/branch/master/graph/badge.svg)](https://codecov.io/gh/trallnag/trallnags-hello-python)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nMy personal Python project "template".\n',
    'author': 'Tim Schwenke',
    'author_email': 'tim.and.trallnag+code@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/trallnag/hello-python',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
