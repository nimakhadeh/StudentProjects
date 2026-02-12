"""
ASGI config for car_shop project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_shop.settings')

application = get_asgi_application()
