from django.conf import settings

def pytest_configure():
    settings.configure(
        SESSION_ENGINE='django.contrib.sessions.backends.cache',
        CACHES={
            'default': {
                'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
            }
        }
    )
