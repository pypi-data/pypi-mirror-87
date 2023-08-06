# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['storages-dospaces', 'storages-dospaces.backends']

package_data = \
{'': ['*']}

install_requires = \
['django-storages>=1.10.1,<2.0.0']

setup_kwargs = {
    'name': 'django-storages-dospaces',
    'version': '0.1.0',
    'description': 'Small wrapper over django-storages S3Boto3Storage with sane defaults for DigitalOcean Spaces usage.',
    'long_description': None,
    'author': 'Marcelo Cueto',
    'author_email': 'cueto@live.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
