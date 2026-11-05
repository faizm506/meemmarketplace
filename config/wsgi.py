import os
from django.core.wsgi import get_wsgi_application
<<<<<<< HEAD

=======
>>>>>>> 45224bb2107e9c064747289981fd5709c63dc9c9
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
application = get_wsgi_application()
