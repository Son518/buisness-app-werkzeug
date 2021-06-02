from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Date, String, Integer, Text, Enum
# from sqlalchemy.orm import mapper, relationship

from .utils import get_random_uid
from .utils import Base
from .utils import session
from .utils import url_for

import enum
class TypeEnum(enum.Enum):
    Public = 1
    Private = 2
    Government = 3

class NewsEnum(enum.Enum):
    Business = 1
    Market = 2
    Politics = 3
    Technology = 4
    TV = 5
    Covid = 6

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
    email = Column(String(30))
    first_name = Column(String(30))
    last_name = Column(String(30))
    password = Column(String(30))
    birthday = Column(Date)
    phone = Column(String(30))
    usertype = Column(Integer)
    public = Column(Boolean)
    photo = Column(String(100))
    
    def __init__(self, ):
        pass
    def __repr__(self):
        return "<user('%s','%s','%s','%s','%s','%s','%s','%s','%s')="">" % (self.username, self.first_name, self.last_name, 
        self.password, self.birthday, self.phone, self.usertype, self.public, self.photo)

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    country_name = Column(String(50))
    timezone = Column(String(20))
    area_number = Column(String(20))
    business_capital = Column(String(100))
    administrative_capital = Column(String(100))
    official_language = Column(String(100))
    total_area = Column(String(100))
    population = Column(String(100))
    currency = Column(String(100))
    gdp = Column(String(100))
    gdp_per_capital = Column(String(100))
    key_industries = Column(String(100))
    exports = Column(String(100))
    main_export_partners = Column(String(100))
    imports = Column(String(100))
    import_partners = Column(String(100))
    exports = Column(String(100))
    economic_brief = Column(Text)
    
    def __init__(self, ):
        pass
    def __repr__(self):
        return f"-----"

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    company_logo = Column(String(255))
    company_name = Column(String(255))
    industry_id = Column(Integer)
    company_type = Column(Enum(TypeEnum))
    company_intro = Column(String(500))
    company_vision = Column(String(255))
    company_mission = Column(String(255))
    company_desc = Column(String(255))
    company_employees = Column(String(255))
    company_market = Column(String(255))
    company_postal_address = Column(String(255))
    company_physical_street = Column(String(255))
    company_physical_district = Column(String(255))
    company_physical_city = Column(String(255))
    company_physical_country = Column(String(255))
    company_tel = Column(String(255))
    company_fax = Column(String(255))
    company_email = Column(String(255))
    company_web = Column(String(255))

class Industry(Base):
    __tablename__ = "industries"
    id = Column(Integer, primary_key=True)
    industry_name = Column(String(255))

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    product_name = Column(String(255))

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True)
    service_name = Column(String(255))

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    contact_name = Column(String(255))
    contact_title = Column(String(255))
    contact_photo = Column(String(255))

class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    news_title = Column(String(255))
    news_content = Column(String(255))
    news_created = Column(DateTime)
    new_type = Column(Enum(NewsEnum))
