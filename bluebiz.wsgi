import sys
sys.path.insert(0, '/var/www/bluebiz')
from manage import make_app
application = make_app();
