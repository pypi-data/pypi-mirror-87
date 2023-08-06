# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['md_to_pdf']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'md-to-pdf',
    'version': '0.1.0',
    'description': 'Yet another Markdown to PDF converter',
    'long_description': '# md-to-pdf\nYet another Markdown to PDF converter\n',
    'author': 'Vincent Poulailleau',
    'author_email': 'vpoulailleau@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vpoulailleau/md-to-pdf',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
