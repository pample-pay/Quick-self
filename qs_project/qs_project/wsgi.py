"""
WSGI config for qs_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from whitenoise import WhiteNoise
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qs_project.settings')

application = get_wsgi_application()

application = WhiteNoise(application, root='')
application.add_files('/web/qs_project/.static', prefix='')