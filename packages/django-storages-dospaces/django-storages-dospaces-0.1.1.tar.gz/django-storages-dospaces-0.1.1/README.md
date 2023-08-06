# django-storages-dospaces
Small wrapper over django-storages S3Boto3Storage with sane defaults for DigitalOcean Spaces usage.


## Installation via pip
```
pip install django-storages-dospaces
```

## Usage
In order to use `django-storages-dospaces` all you need to do is to set it's backend as your default `STATICFILES_STORAGE` on your project's `settings.py` file and configure some settings on it. It's recommended to use environment variables to achieve it.

### Environment variables
The following environment variables must be set in order to use this package with your DigitalOcean Space.

`DO_SPACES_ENDPOINT_URL` must point to your Space server region, eg: if your space is on `sfo2`, the URL should be `https://sfo2.digitaloceanspaces.com`

```
DO_SPACES_ACCESS_KEY_ID='<your Space id >'
DO_SPACES_CACHE_MAX_AGE='86400'
DO_SPACES_DEFAULT_ACL='None'
DO_SPACES_ENDPOINT_URL='https://<region>.digitaloceanspaces.com'
DO_SPACES_SECRET_ACCESS_KEY='<your Space access key>'
DO_SPACES_SPACE_FOLDER='<the folder where your files will be uploaded to>'
DO_SPACES_SPACE_NAME='<the name of your Space as it appears in your dashboard>'
```

You can set them using an script with `export` command before every line(if using `bash`) or another way of your preference.

Once they are set, they can be gotten from your `settings.py` file using `os.environ.get('<env var key>')`

### Settings file
In order to enable this package behaviour you will have to set the following settings on your project's `settings.py` file

```
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'

# Definitive configuration
DO_SPACES_ACCESS_KEY_ID = os.environ.get(
    'DO_SPACES_ACCESS_KEY_ID'
)
DO_SPACES_SECRET_ACCESS_KEY = os.environ.get(
    'DO_SPACES_SECRET_ACCESS_KEY'
)
DO_SPACES_SPACE_NAME = os.environ.get(
    'DO_SPACES_SPACE_NAME'
)
DO_SPACES_SPACE_FOLDER = os.environ.get(
    'DO_SPACES_SPACE_FOLDER'
)
DO_SPACES_ENDPOINT_URL = os.environ.get(
    'DO_SPACES_ENDPOINT_URL'
)
DO_SPACES_CACHE_MAX_AGE = int(
    os.environ.get(
        'DO_SPACES_CACHE_MAX_AGE',
        86400
    )
)
DO_SPACES_DEFAULT_ACL = None

# Get DEFAULT_ACL from env vars
try:
    DEFAULT_ACL = os.environ.get(
        'DO_SPACES_DEFAULT_ACL'
    )

    if DEFAULT_ACL != 'None':
        DO_SPACES_DEFAULT_ACL = DEFAULT_ACL

except Exception as e:
    pass

# Set File locations
DO_SPACES_STATIC_LOCATION = '{FOLDER}/static'.format(
    FOLDER=DO_SPACES_SPACE_FOLDER
)
DO_SPACES_PUBLIC_MEDIA_LOCATION = '{FOLDER}/media/public'.format(
    FOLDER=DO_SPACES_SPACE_FOLDER
)
DO_SPACES_PRIVATE_MEDIA_LOCATION = '{FOLDER}/media/private'.format(
    FOLDER=DO_SPACES_SPACE_FOLDER
)

#  Static files config
STATIC_URL = 'https://{ENDPOINT_URL}/{STATIC_LOCATION}/'.format(
    ENDPOINT_URL=DO_SPACES_ENDPOINT_URL,
    STATIC_LOCATION=DO_SPACES_STATIC_LOCATION
)

# Configure file storage settings
STATICFILES_STORAGE = 'storages-dospaces.backends.do_spaces.DigitalOceanSpacesStaticStorage'
DEFAULT_FILE_STORAGE = 'storages-dospaces.backends.do_spaces.DigitalOceanSpacesPublicMediaStorage'
PRIVATE_FILE_STORAGE = 'storages-dospaces.backends.do_spaces.DigitalOceanSpacesPrivateMediaStorage'

```
