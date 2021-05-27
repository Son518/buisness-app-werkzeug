from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Date, String, Integer, Text
# from sqlalchemy.orm import mapper, relationship

from .utils import get_random_uid
from .utils import Base
from .utils import session
from .utils import url_for

""" 
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
 """

class URL(Base):
    __tablename__ = "urls"

    uid = Column(String(140), primary_key=True)
    target = Column(String(500))
    added = Column(DateTime)
    public = Column(Boolean)

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


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    first_name = Column(String(30))
    last_name = Column(String(30))
    password = Column(String(30))
    birthday = Column(Date)
    phone = Column(String(30))
    usertype = Column(Integer)
    public = Column(Boolean)
    
    def __init__(self, ):
        pass
    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, first_name={self.first_name!r}, last_name={self.last_name!r})"

