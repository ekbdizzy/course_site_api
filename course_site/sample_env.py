import os
import dj_database_url
DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '4!z#i6yh(t1$ipitm%=echsy$o7yb%zmu05!_th(se83q%)j*t'
# DB = {
#     'ENGINE': 'django.db.backends.sqlite3',
#     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
# }
DB = dj_database_url.config()