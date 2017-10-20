# blog/settings.py
from django.conf import settings
USER_ACCOUNTS = getattr(settings, 'USER_ACCOUNTS', 'False')
