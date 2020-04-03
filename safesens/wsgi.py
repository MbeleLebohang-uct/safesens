import os
import sys
from django.core.wsgi import get_wsgi_application
from dj_static import Cling

sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safesens.settings')

application = Cling(get_wsgi_application())
