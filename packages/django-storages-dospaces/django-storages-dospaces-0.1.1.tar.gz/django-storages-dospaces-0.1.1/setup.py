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
    'version': '0.1.1',
    'description': 'Small wrapper over django-storages S3Boto3Storage with sane defaults for DigitalOcean Spaces usage.',
    'long_description': "# django-storages-dospaces\nSmall wrapper over django-storages S3Boto3Storage with sane defaults for DigitalOcean Spaces usage.\n\n\n## Installation via pip\n```\npip install django-storages-dospaces\n```\n\n## Usage\nIn order to use `django-storages-dospaces` all you need to do is to set it's backend as your default `STATICFILES_STORAGE` on your project's `settings.py` file and configure some settings on it. It's recommended to use environment variables to achieve it.\n\n### Environment variables\nThe following environment variables must be set in order to use this package with your DigitalOcean Space.\n\n`DO_SPACES_ENDPOINT_URL` must point to your Space server region, eg: if your space is on `sfo2`, the URL should be `https://sfo2.digitaloceanspaces.com`\n\n```\nDO_SPACES_ACCESS_KEY_ID='<your Space id >'\nDO_SPACES_CACHE_MAX_AGE='86400'\nDO_SPACES_DEFAULT_ACL='None'\nDO_SPACES_ENDPOINT_URL='https://<region>.digitaloceanspaces.com'\nDO_SPACES_SECRET_ACCESS_KEY='<your Space access key>'\nDO_SPACES_SPACE_FOLDER='<the folder where your files will be uploaded to>'\nDO_SPACES_SPACE_NAME='<the name of your Space as it appears in your dashboard>'\n```\n\nYou can set them using an script with `export` command before every line(if using `bash`) or another way of your preference.\n\nOnce they are set, they can be gotten from your `settings.py` file using `os.environ.get('<env var key>')`\n\n### Settings file\nIn order to enable this package behaviour you will have to set the following settings on your project's `settings.py` file\n\n```\n# Static files (CSS, JavaScript, Images)\n# https://docs.djangoproject.com/en/2.2/howto/static-files/\n\nSTATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')\nSTATIC_URL = '/static/'\n\n# Definitive configuration\nDO_SPACES_ACCESS_KEY_ID = os.environ.get(\n    'DO_SPACES_ACCESS_KEY_ID'\n)\nDO_SPACES_SECRET_ACCESS_KEY = os.environ.get(\n    'DO_SPACES_SECRET_ACCESS_KEY'\n)\nDO_SPACES_SPACE_NAME = os.environ.get(\n    'DO_SPACES_SPACE_NAME'\n)\nDO_SPACES_SPACE_FOLDER = os.environ.get(\n    'DO_SPACES_SPACE_FOLDER'\n)\nDO_SPACES_ENDPOINT_URL = os.environ.get(\n    'DO_SPACES_ENDPOINT_URL'\n)\nDO_SPACES_CACHE_MAX_AGE = int(\n    os.environ.get(\n        'DO_SPACES_CACHE_MAX_AGE',\n        86400\n    )\n)\nDO_SPACES_DEFAULT_ACL = None\n\n# Get DEFAULT_ACL from env vars\ntry:\n    DEFAULT_ACL = os.environ.get(\n        'DO_SPACES_DEFAULT_ACL'\n    )\n\n    if DEFAULT_ACL != 'None':\n        DO_SPACES_DEFAULT_ACL = DEFAULT_ACL\n\nexcept Exception as e:\n    pass\n\n# Set File locations\nDO_SPACES_STATIC_LOCATION = '{FOLDER}/static'.format(\n    FOLDER=DO_SPACES_SPACE_FOLDER\n)\nDO_SPACES_PUBLIC_MEDIA_LOCATION = '{FOLDER}/media/public'.format(\n    FOLDER=DO_SPACES_SPACE_FOLDER\n)\nDO_SPACES_PRIVATE_MEDIA_LOCATION = '{FOLDER}/media/private'.format(\n    FOLDER=DO_SPACES_SPACE_FOLDER\n)\n\n#  Static files config\nSTATIC_URL = 'https://{ENDPOINT_URL}/{STATIC_LOCATION}/'.format(\n    ENDPOINT_URL=DO_SPACES_ENDPOINT_URL,\n    STATIC_LOCATION=DO_SPACES_STATIC_LOCATION\n)\n\n# Configure file storage settings\nSTATICFILES_STORAGE = 'storages-dospaces.backends.do_spaces.DigitalOceanSpacesStaticStorage'\nDEFAULT_FILE_STORAGE = 'storages-dospaces.backends.do_spaces.DigitalOceanSpacesPublicMediaStorage'\nPRIVATE_FILE_STORAGE = 'storages-dospaces.backends.do_spaces.DigitalOceanSpacesPrivateMediaStorage'\n\n```\n",
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
