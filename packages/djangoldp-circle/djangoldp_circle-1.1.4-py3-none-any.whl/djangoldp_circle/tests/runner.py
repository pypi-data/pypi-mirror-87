import sys

import django
from django.conf import settings
from djangoldp.tests import settings_default

settings.configure(default_settings=settings_default,
                   DJANGOLDP_PACKAGES=['djangoldp_circle', 'djangoldp_circle.tests', ],
                   INSTALLED_APPS=('django.contrib.auth',
                                   'django.contrib.contenttypes',
                                   'django.contrib.sessions',
                                   'django.contrib.admin',
                                   'django.contrib.messages',
                                   'django.contrib.staticfiles',
                                   'guardian',
                                   'djangoldp_circle',
                                   'djangoldp_circle.tests',
                                   'djangoldp',
                                   ),
                   SITE_URL='http://happy-dev.fr',
                   BASE_URL='http://happy-dev.fr',
                   REST_FRAMEWORK = {
                       'DEFAULT_PAGINATION_CLASS': 'djangoldp.pagination.LDPPagination',
                       'PAGE_SIZE': 5
                   },
                   SEND_BACKLINKS=False,
                   JABBER_DEFAULT_HOST=None,
                   PERMISSIONS_CACHE=False,
                   ANONYMOUS_USER_NAME=None,
                   SERIALIZER_CACHE=False
                   )

django.setup()
from django.test.runner import DiscoverRunner

test_runner = DiscoverRunner(verbosity=1)

failures = test_runner.run_tests([
    'djangoldp_circle.tests.tests_permissions',
    'djangoldp_circle.tests.tests_save'
])
if failures:
    sys.exit(failures)
