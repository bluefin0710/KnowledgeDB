"""
WSGI config for KnowledgeDB project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import sys

path = '/home/nmcmh01/nmcmh01.pythonanywhere.com/'
if path not in sys.path:
    sys.path.append(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KnowledgeDB.settings')
#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nmcmh01.pythonanywhere.com.settings')
#os.environ('DJANGO_SETTINGS_MODULE', 'KnowledgeDB.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
