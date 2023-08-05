# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['holon', 'holon.formats', 'holon.ietf', 'holon.models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.7.2,<2.0.0']

setup_kwargs = {
    'name': 'holon',
    'version': '0.1.0',
    'description': 'Experimental API Design Dystem library',
    'long_description': '# Holon\n\nTool for build API Design Systems.\n\n**Currently in experimental mode. Interface will change.**\n',
    'author': 'Stephen Mizell',
    'author_email': 'smizell@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/smizell/holon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.6',
}


setup(**setup_kwargs)
