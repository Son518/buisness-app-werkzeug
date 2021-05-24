from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Date, String, Table, Integer, Text
from sqlalchemy.orm import mapper

from .utils import get_random_uid
from .utils import metadata
from .utils import session
from .utils import url_for

url_table = Table(
    "urls",
    metadata,
    Column("uid", String(140), primary_key=True),
    Column("target", String(500)),
    Column("added", DateTime),
    Column("public", Boolean),
)
users_table = Table(
    "users",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("username", String(500)),
    Column("first_name", String(500)),
    Column("last_name", String(500)),
    Column("email", String(500)),
    Column("password", String(500)),
    Column("birthday", Date),
    Column("phone", String(100)),
    Column("usertype", Integer),
    Column("public", Boolean),
)
country_table = Table(
    "countries",
    metadata,
    Column("country_id", Integer, primary_key=True),
    Column("country_name", String(50)),
    Column("timezone", String(20)),
    Column("area_number", String(20)),
    Column("business_capital", String(100)),
    Column("administrative_capital", String(100)),
    Column("official_language", String(100)),
    Column("total_area", String(100)),
    Column("population", String(100)),
    Column("currency", String(100)),
    Column("gdp", String(100)),
    Column("gdp_per_capital", String(100)),
    Column("key_industries", String(100)),
    Column("exports", String(100)),
    Column("main_export_partners", String(100)),
    Column("imports", String(100)),
    Column("import_partners", String(100)),
    Column("exports", String(100)),
    Column("economic_brief", Text)
)
company_table = Table(
    "companies",
    metadata,
    Column("company_id", Integer, primary_key=True),
    Column("company_name", String(100)),

)


class URL:
    query = session.query_property()

    def __init__(self, target, public=True, uid=None, added=None):
        self.target = target
        self.public = public
        self.added = added or datetime.utcnow()
        if not uid:
            while 1:
                uid = get_random_uid()
                if not URL.query.get(uid):
                    break
        self.uid = uid
        session.add(self)

    @property
    def short_url(self):
        return url_for("link", uid=self.uid, _external=True)

    def __repr__(self):
        return f"<URL {self.uid!r}>"



class User:
    query = session.query_property()
    email = Column(String)
    
    def __init__(self, ):
        pass

mapper(URL, url_table)
mapper(User, users_table)
