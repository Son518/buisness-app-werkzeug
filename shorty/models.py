
from datetime import datetime
from decimal import Decimal
from unicodedata import category

from sqlalchemy import Boolean, Column, DateTime, Date, String, Integer, Text, Enum, DECIMAL, column
# from sqlalchemy.orm import mapper, relationship

from .utils import get_random_uid
from .utils import Base
from .utils import session
from .utils import url_for
import enum

news_categories = Enum("Business", "Market", "Politics", "Technology", "TV", "COVID-19")
type_enum = Enum("Public", "Private", "Government", "Co-operative")
language_enum = Enum("Afar", "Afrikaans", "Akan", "Algerian Arabic", "Amharic", "Arabic", "Balanta", \
        "Bambara", "Bariba", "Berber", "Bulu", "Chewa", "Chokwe", "Comorian", "Creole", "Dangme", "Dioula", "Duala", \
        "Dyula", "Egyptian Arabic", "English", "Ewe", "Fan", "Fang", "Fon", "French", "Fula", "Fulani", "Fulfulde", \
        "Ga", "Guan", "Hausa", "Igbo", "Italian", "Jola", "Kabiye", "Kalanga", "Kasem", "Khoekhoegowab", "Kikongo", \
        "Kimbundu", "Kinyarwanda", "Kirundi", "Kituba", "Krio", "Libyan Arabic", "Lingala", "Malagasy", "Mandinka", \
        "Manjak", "Mole-Dagbani", "Moore", "Moroccan Arabic", "Mwani", "Ndebele", "Oromo", "Oshiwambo", "Otjiherero", \
        "Pedi", "Pidgin-English", "Portuguese", "Pulaar", "RuKwangali", "Sango", "Serer", "Shona", "Somali", "Soninke", \
        "Sotho", "Spanish", "Susu", "Swahili", "Swati", "Swazi", "Teda", "Tigrinya", "Tonga", "Tshiluba", "Tsonga", "Tswana", \
        "Tunisian Arabic", "Umbundu", "Venda", "Wolof", "Xhosa", "Yoruba", "Zarma-Songhai", "Zulu")
city_enum = Enum("Abidjan", "Abuja", "Accra", "Addis Ababa", "Algiers", \
        "Antananarivo", "Asmara", "Bamako", "Bangui", "Banjul", "Bissau", "Brazzaville", "Bujumbura", \
        "Cairo", "Cape Town", "Casablanca", "Conakry", "Cotonou", "Dakar", "Dar es Salaam", "Djibouti",\
        "Dodoma", "Douala", "Freetown", "Gaborone", "Gitega", "Harare", "Johannesburg", "Juba", "Kampala",\
        "Khartoum", "Kigali", "Kinshasa", "Lagos", "Libreville", "Lilongwe", "Lobamba", "Lome", "Luanda", \
        "Lusaka", "Malabo", "Maputo", "Maseru", "Mbabane", "Mogadishu", "Monrovia", "Moroni", "N’Djamena", \
        "Nairobi", "Niamey", "Nouakchott", "Ouagadougou", "Port Louis", "Porto-Novo", "Praia", "Pretoria", \
        "Rabat", "Sao Tome", "Serekunda", "Tripoli", "Tunis", "Victoria", "Windhoek", "Yamoussoukro", "Yaounde")
currency_enum = Enum("Algerian dinar", "Angolan kwanza", "CFA franc", "Botswana pula", "CFA franc", "Burundian franc", "CFA franc", \
        "Cape Verdean escudo", "CFA franc", "CFA franc", "Comorian franc", "CFA franc", "Congolese franc", "Djiboutian franc", "Egyptian pound", \
        "CFA franc", "Eritrean nakfa", "Lilangeni", "Ethiopian birr", "CFA franc", "Dalasi", "Ghanaian cedi", "Guinean franc", "CFA franc", \
        "CFA franc", "Kenyan shilling", "Lesotho loti", "Liberian dollar", "Libyan dinar", "Malagasy ariary", "Malawian kwacha", "CFA franc", \
        "Ouguiya", "Mauritian rupee", "Moroccan dirham", "Mozambican metical", "Namibian dollar", "CFA franc", "Nigeria naira", "Rwandan franc", \
        "Saint Helena pound", "Sao Tome and Principe dobra", "CFA franc", "Seychellois rupee", "Sierra Leone leone", "Somali shilling", "South African rand", \
        "South Sudanese pound", "Sudanese pound", "Tanzanian shilling", "CFA Franc", "Tunisian dinar", "Ugandan shilling", "Zambian kwacha", "RTGS dollar")
area_number_enum = Enum("+20", "+27", "+211", "+212", "+213", "+216", "+218", "+220", "+221", "+222", "+223", \
        "+224", "+225", "+226", "+227", "+228", "+229", "+230", "+231", "+232", "+233", "+234", "+235", "+236", "+237",\
        "+238", "+239", "+240", "+241", "+242", "+243", "+244", "+245", "+248", "+249", "+250", "+251", "+252", "+253",\
        "+254", "+255", "+256", "+257", "+258", "+260", "+261", "+263", "+264", "+265", "+266", "+267", "+268", "+269", "+290", "+291")
region_enum = Enum("Southern Africa", "Central Africa", "East Africa", "North Africa", "West Africa", "East Central Africa", \
        "North East Africa", "North West Africa")
timezone_enum = Enum("GMT/UTC-1:00", "GMT/UTC+0:00", "GMT/UTC+1:00", "GMT/UTC+2:00", "GMT/UTC+3:00", "GMT/UTC+4:00")

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
    password = Column(String(255))
    birthday = Column(Date)
    phone = Column(String(30))
    usertype = Column(Integer)
    public = Column(Boolean)
    photo = Column(String(100))
    
    def __init__(self, ):
        pass
    def __repr__(self):
        return "<user('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')="">" % (self.username, self.email, self.first_name, self.last_name, 
        self.password, self.birthday, self.phone, self.usertype, self.public, self.photo)

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    country_name = Column(String(50))
    region = Column(region_enum)
    timezone = Column(timezone_enum)
    area_number = Column(area_number_enum)
    business_capital = Column(city_enum)
    administrative_capital = Column(city_enum)
    official_language1 = Column(language_enum)
    official_language2 = Column(language_enum)
    total_area = Column(DECIMAL(12,2))
    population = Column(DECIMAL(12,2))
    currency = Column(currency_enum)
    gdp = Column(String(50))
    gdp_per_capital = Column(String(100))
    exports = Column(String(100))
    main_export_partners = Column(String(100))
    imports = Column(String(100))
    import_partners = Column(String(100))
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
    company_type = Column(type_enum)
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
    company_product1 = Column(String(255))
    company_product2 = Column(String(255))
    company_product3 = Column(String(255))
    company_service1 = Column(String(255))
    company_service2 = Column(String(255))
    company_service3 = Column(String(255))
    company_ticker = Column(String(50))
    company_contact_name = Column(String(250))
    company_contact_title1 = Column(String(250))
    company_contact_title2 = Column(String(250))

class Executive(Base):
    __tablename__ = 'executives'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    title1 = Column(String(50))
    title2 = Column(String(50))
    photo = Column(String(50))
    company_id = Column(Integer)

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
    news_country = Column(String(255))
    news_category = Column(news_categories)
    news_title = Column(String(255))
    news_reporter = Column(String(255))
    news_created = Column(DateTime)
    news_source = Column(String(255))
    news_sharing_links = Column(String(255))
    news_image = Column(String(255))
    news_image_caption = Column(String(255))
    news_content = Column(String(255))

class IndustryCountry(Base):
    __tablename__ = "industry_country"
    id = Column(Integer, primary_key=True)
    industry_id = Column(Integer)
    country_id = Column(Integer)
    company_id = Column(Integer)

class Story(Base):
    __tablename__ = "company_stories"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    title1 = Column(String(255))
    content1 = Column(Text)
    title2 = Column(String(255))
    content2 = Column(Text)

class Video(Base):
    __tablename__ = "company_videos"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer)
    company_video = Column(String(255))
