from sqlalchemy import create_engine
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import NotFound
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.wrappers import Request
from werkzeug.wsgi import ClosingIterator

from . import views
from .utils import local
from .utils import local_manager
from .utils import metadata
from .utils import session
from .utils import STATIC_PATH
from .utils import url_map


class Shorty:
    def __init__(self, db_uri):
        local.application = self
        self.database_engine = create_engine(db_uri, convert_unicode=True)

        self.dispatch = SharedDataMiddleware(self.dispatch, {"/static": STATIC_PATH})

    def init_database(self):
        metadata.create_all(self.database_engine)

    def create_superuser(self, email, password):
        from cryptography.fernet import Fernet
        from .models import User
        superuser = User()
        # config other fields
        superuser.email = email
        superuser.username = 'admin'
        superuser.usertype = 1
        # password encrypt
        key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
        fernet = Fernet(key)
        encrypt_password = fernet.encrypt(password.encode())
        print("encrypt password: ", encrypt_password, encrypt_password.decode())
        superuser.password = encrypt_password

        session.add(superuser)
        session.commit()

    def dispatch(self, environ, start_response):
        local.application = self
        request = Request(environ)
        print("Session: ", session)
        local.url_adapter = adapter = url_map.bind_to_environ(environ)
        try:
            endpoint, values = adapter.match()
            handler = getattr(views, endpoint)
            response = handler(request, **values)
        except NotFound:
            response = views.not_found(request)
            response.status_code = 404
        except HTTPException as e:
            response = e
        return ClosingIterator(
            response(environ, start_response), [session.remove, local_manager.cleanup]
        )

    def __call__(self, environ, start_response):
        return self.dispatch(environ, start_response)
