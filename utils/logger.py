import sys
import os
from django.conf import settings
import loguru

log_file = os.path.join(settings.BASE_DIR, 'debug.log')

logging = loguru.logger
logging.add(log_file, rotation="100 KB")
logging.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")
