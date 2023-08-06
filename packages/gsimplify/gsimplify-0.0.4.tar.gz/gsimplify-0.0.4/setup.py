# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gsimplify']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0',
 'gitpython>=3.1.11,<4.0.0',
 'google-api-python-client>=1.12.5,<2.0.0',
 'google-auth-httplib2>=0.0.4,<0.0.5',
 'google-auth-oauthlib>=0.4.2,<0.5.0',
 'pydantic>=1.7.2,<2.0.0',
 'tqdm>=4.53.0,<5.0.0']

setup_kwargs = {
    'name': 'gsimplify',
    'version': '0.0.4',
    'description': '',
    'long_description': '# gsimplify\nA Google docs to html compiler.\n',
    'author': 'echapman2022',
    'author_email': 'ethan.chapman0@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ChoateProgrammingUnion/simplify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
