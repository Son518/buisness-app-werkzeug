import sys
sys.path.insert(0, '/var/www/bluebiz')
from manage import make_app
print(sys.version)
application = make_app();
