# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_session_header_11']

package_data = \
{'': ['*']}

install_requires = \
['django>=1.11,<2.0']

extras_require = \
{'drf': ['djangorestframework>=3.9,<4.0']}

setup_kwargs = {
    'name': 'django-session-header-11',
    'version': '1.0.1',
    'description': 'Identify the Django Session by a Header',
    'long_description': "Django Session Header: Identify the session through a header\n============================================================\n\nThere are some situations where the browser\nmay not allow any cookies at all to be used.\nIn those cases, we would like to be able to fall back\nto something that is both secure, and capable.\nThis package allows you to manually pass the\nsessionid using a header, so that you can continue\nto use Django's excellent session management.\n\nIt extends Django's built-in sessions to support\nsessions in places where cookies are not allowed.\nFor most views, the handling will be seamless.\nThose that need to have sessions that persist despite the\nabsence of cookies, there are a few extra features.\n\n\nUsage\n=====\n\nFirst, install the package.\n\n.. code-block:: sh\n\n    pip install django-session-header\n\nReplace ``django.contrib.sessions.middleware.SessionMiddleware``\nin your ``settings.py`` with the following:\n\n.. code-block:: python\n\n    MIDDLEWARE_CLASSES = [\n       # ...\n       # 'django.contrib.session.middleware.SessionMiddleware',\n       'django_session_header.middleware.SessionMiddleware',\n    ]\n\nAnd replace the Django Rest Framework ``SessionAuthentication``\nclass with ``django_session_header.authentication.SessionAuthentication``:\n\n.. code-block:: python\n\n    REST_FRAMEWORK = {\n        'DEFAUlT_AUTHENTICATION_CLASSES': [\n            # ...\n            # 'rest_framework.authentication.SessionAuthentication',\n            'django_session_header.authentication.SessionAuthentication',\n        ]\n    }\n\nIf a session was obtained via a session header,\nthen ``request.session.csrf_exempt`` will be ``True``.\nYou can use this to conditionally apply CSRF protection.\nOr, if you prefer, you can replace Django's normal CSRF middleware\nwith ``django_session_header.middleware.CsrfViewMiddleware``:\n\n.. code-block:: python\n\n    MIDDLEWARE_CLASSES = [\n        # ...\n        # 'django.middleware.csrf.CsrfViewMiddleware',\n        'django_session_header.middleware.CsrfViewMiddleware',\n    ]\n\nThe ``sessionid`` will be available in the ``X-SessionID`` response header,\nand you can now set the ``X-SessionID`` header on the request manually\nto avoid needing cookies to power your sessions.\n",
    'author': 'Ryan Hiebert',
    'author_email': 'ryan@ryanhiebert.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ryanhiebert/django-session-header',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
