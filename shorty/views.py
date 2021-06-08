import json
from os import error
from time import timezone
from sqlalchemy import true
from sqlalchemy.sql.functions import count
from sqlalchemy.orm import Load
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect
from .models import Industry, User, Country, IndustryCountry
from .utils import expose, Pagination, render_template, session, url_for, validate_url

from secure_cookie.session import FilesystemSessionStore

session_store = FilesystemSessionStore()

language_enum = ("Afar", "Afrikaans", "Akan", "Algerian Arabic", "Amharic", "Arabic", "Balanta", \
        "Bambara", "Bariba", "Berber", "Bulu", "Chewa", "Chokwe", "Comorian", "Creole", "Dangme", "Dioula", "Duala", \
        "Dyula", "Egyptian Arabic", "English", "Ewe", "Fan", "Fang", "Fon", "French", "Fula", "Fulani", "Fulfulde", \
        "Ga", "Guan", "Hausa", "Igbo", "Italian", "Jola", "Kabiye", "Kalanga", "Kasem", "Khoekhoegowab", "Kikongo", \
        "Kimbundu", "Kinyarwanda", "Kirundi", "Kituba", "Krio", "Libyan Arabic", "Lingala", "Malagasy", "Mandinka", \
        "Manjak", "Mole-Dagbani", "Moore", "Moroccan Arabic", "Mwani", "Ndebele", "Oromo", "Oshiwambo", "Otjiherero", \
        "Pedi", "Pidgin-English", "Portuguese", "Pulaar", "RuKwangali", "Sango", "Serer", "Shona", "Somali", "Soninke", \
        "Sotho", "Spanish", "Susu", "Swahili", "Swati", "Swazi", "Teda", "Tigrinya", "Tonga", "Tshiluba", "Tsonga", "Tswana", \
        "Tunisian Arabic", "Umbundu", "Venda", "Wolof", "Xhosa", "Yoruba", "Zarma-Songhai", "Zulu")
city_enum = ("Abidjan", "Abuja", "Accra", "Addis Ababa", "Algiers", \
        "Antananarivo", "Asmara", "Bamako", "Bangui", "Banjul", "Bissau", "Brazzaville", "Bujumbura", \
        "Cairo", "Cape Town", "Casablanca", "Conakry", "Cotonou", "Dakar", "Dar es Salaam", "Djibouti",\
        "Dodoma", "Douala", "Freetown", "Gaborone", "Gitega", "Harare", "Johannesburg", "Juba", "Kampala",\
        "Khartoum", "Kigali", "Kinshasa", "Lagos", "Libreville", "Lilongwe", "Lobamba", "Lome", "Luanda", \
        "Lusaka", "Malabo", "Maputo", "Maseru", "Mbabane", "Mogadishu", "Monrovia", "Moroni", "N’Djamena", \
        "Nairobi", "Niamey", "Nouakchott", "Ouagadougou", "Port Louis", "Porto-Novo", "Praia", "Pretoria", \
        "Rabat", "Sao Tome", "Serekunda", "Tripoli", "Tunis", "Victoria", "Windhoek", "Yamoussoukro", "Yaounde")
currency_enum = ("Algerian dinar", "Angolan kwanza", "CFA franc", "Botswana pula", "CFA franc", "Burundian franc", "CFA franc", \
        "Cape Verdean escudo", "CFA franc", "CFA franc", "Comorian franc", "CFA franc", "Congolese franc", "Djiboutian franc", "Egyptian pound", \
        "CFA franc", "Eritrean nakfa", "Lilangeni", "Ethiopian birr", "CFA franc", "Dalasi", "Ghanaian cedi", "Guinean franc", "CFA franc", \
        "CFA franc", "Kenyan shilling", "Lesotho loti", "Liberian dollar", "Libyan dinar", "Malagasy ariary", "Malawian kwacha", "CFA franc", \
        "Ouguiya", "Mauritian rupee", "Moroccan dirham", "Mozambican metical", "Namibian dollar", "CFA franc", "Nigeria naira", "Rwandan franc", \
        "Saint Helena pound", "Sao Tome and Principe dobra", "CFA franc", "Seychellois rupee", "Sierra Leone leone", "Somali shilling", "South African rand", \
        "South Sudanese pound", "Sudanese pound", "Tanzanian shilling", "CFA Franc", "Tunisian dinar", "Ugandan shilling", "Zambian kwacha", "RTGS dollar")
area_number_enum = ("+20", "+27", "+211", "+212", "+213", "+216", "+218", "+220", "+221", "+222", "+223", \
        "+224", "+225", "+226", "+227", "+228", "+229", "+230", "+231", "+232", "+233", "+234", "+235", "+236", "+237",\
        "+238", "+239", "+240", "+241", "+242", "+243", "+244", "+245", "+248", "+249", "+250", "+251", "+252", "+253",\
        "+254", "+255", "+256", "+257", "+258", "+260", "+261", "+263", "+264", "+265", "+266", "+267", "+268", "+269", "+290", "+291")
region_enum = ("Southern Africa", "Central Africa", "East Africa", "North Africa", "West Africa", "East Central Africa", \
        "North East Africa", "North West Africa")
timezone_enum = ("GMT/UTC-1:00", "GMT/UTC+0:00", "GMT/UTC+1:00", "GMT/UTC+2:00", "GMT/UTC+3:00", "GMT/UTC+4:00")

def user_session(request):
    sid = request.cookies.get("wsessid")
    if not sid:
        return False

    the_session = session_store.get(sid)

    userdata = the_session['user']
    if not userdata:
        return False

    return json.loads(userdata)

def exist_empty(data):
    err_msg = {}
    for key, value in data.items():
        if value=="":
                err_msg[key]=True
    return err_msg

@expose("/test")
def test(request):
    our_user = session.query(User).filter_by(username='wang').first()
    our_user.last_name = 'naixu'
    session.commit()

    return render_template("test/login.html")

@expose("/")
def index(request):
    usersession = user_session(request)
    if not usersession:
        return render_template("index.html")
    else:
        print("USER SESSION: ", usersession)
        return render_template("index.html", usersession=usersession)

@expose("/signin")
def signin(request):
    login_err_msg=""
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        result = session.query(User).filter(User.email == email)

        if result.count() == 0:
            login_err_msg = "Invaild User!"
        for row in result:
            if row.password == password:
                print("User Info: ", row.username, row.password)

                session_data = {
                    "usertype": row.usertype,
                    "username": row.username,
                    "id"      : row.id
                }
                new_session = session_store.new()
                new_session['user'] = json.dumps(session_data)
                session_store.save(new_session)

                response = redirect(url_for("/"))
                response.set_cookie("wsessid", new_session.sid)
                return response
            else:
                login_err_msg = "wrong password"
    return render_template("signin.html", login_err_msg=login_err_msg)

@expose("/signup")
def signup(request):
    if request.method == 'POST':
        err_msg = ""
        email = request.form.get("email")
        password = request.form.get("password")
        result = session.query(User).filter(User.email == email)
        if result.count() > 0:
            err_msg = "Existing User!"
        elif len(password) < 6:
            err_msg = "Weak Password. At least 6 characters!"
        else:
            newUser = User()
            newUser.email = email
            newUser.password = password
            session.add(newUser)
            session.commit()
            return redirect(url_for('signin'))
        return render_template("signin.html", err_msg=err_msg)

@expose("/signout")
def signout(request):
    response = redirect(url_for("/"))
    response.set_cookie("wsessid")
    return response

@expose("/profile")
def profile(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    return render_template("profile.html", usersession=usersession)
# Country CRUD
@expose("/countries")
def countries(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    countries = session.query(Country).all()
    print("Countries: ", countries)
    return render_template("country/country_list.html", usersession=usersession, countries=countries)

@expose("/country/new")
def country_new(request):
    usersession = user_session(request)
    if not usersession or (usersession['usertype'] is not 1):
        return redirect(url_for('/'))

    industries = session.query(Industry).all()
    if request.method == 'POST':
        form_data = request.form.to_dict(flat=False)
        insert_data = {}
        insert_industries = ()

        for key, value in form_data.items():
            if len(value) == 1 and key != 'industries':
                insert_data[key] = value[0]
            elif key == 'industries':
                insert_industries = value
    
        country = Country()
        err_msg = exist_empty(insert_data)
        if len(insert_industries) == 0:
            err_msg['industries'] = True
        if err_msg:
            return render_template("country/country_form.html", err_msg=err_msg, insert_data=insert_data, industries=industries,\
                language_enum=language_enum, city_enum=city_enum, currency_enum=currency_enum, area_number_enum=area_number_enum, \
                region_enum=region_enum, timezone_enum=timezone_enum)
        print(err_msg, not err_msg)
        for key,value in insert_data.items():
            setattr(country, key, value)
        session.add(country)
        session.commit()
        print("RESULT: ", country.id)
        
        if len(insert_industries) > 0:
            for industry_id in insert_industries:
                industry_country = IndustryCountry()
                industry_country.industry_id = industry_id
                industry_country.country_id = country.id
                session.add(industry_country)
                session.commit()
        
        return redirect(url_for("countries"))
    return render_template("country/country_form.html", usersession=usersession, industries=industries, \
        language_enum=language_enum, city_enum=city_enum, currency_enum=currency_enum, area_number_enum=area_number_enum, \
        region_enum=region_enum, timezone_enum=timezone_enum)

@expose("/country/edit/<id>")
def country_edit(request, id):
    usersession = user_session(request)
    if not usersession or (usersession['usertype'] is not 1):
        return redirect(url_for('/'))
    if request.method == 'GET':
        country = session.query(Country).filter(Country.id == id).one()
        industries = session.query(Industry).all()
        selected_industries = session.query(Industry.id).filter(IndustryCountry.country_id == id).\
        join(IndustryCountry, Industry.id == IndustryCountry.industry_id).\
        options(
            Load(Industry).load_only("industry_name")
        ).all()
        selected_industries = [item[0] for item in selected_industries]
        return render_template("country/country_edit.html", usersession=usersession, country=country, industries=industries,\
            selected_industries=selected_industries, \
            language_enum=language_enum, city_enum=city_enum, currency_enum=currency_enum, area_number_enum=area_number_enum, \
            region_enum=region_enum, timezone_enum=timezone_enum)
    
    industries = session.query(Industry).all()
    if request.method == 'POST':
        form_data = request.form.to_dict(flat=False)
        insert_data = {}
        insert_industries = ()

        for key, value in form_data.items():
            if len(value) == 1 and key != 'industries':
                insert_data[key] = value[0]
            elif key == 'industries':
                insert_industries = value
    
        country = session.query(Country).filter(Country.id == id).one()
        err_msg = exist_empty(insert_data)
        for key,value in insert_data.items():
            setattr(country, key, value)

        if len(insert_industries) == 0:
            err_msg['industries'] = True
        if err_msg:
            return render_template("country/country_edit.html", err_msg=err_msg, country=country, industries=industries, \
                language_enum=language_enum, city_enum=city_enum, currency_enum=currency_enum, area_number_enum=area_number_enum, \
                region_enum=region_enum, timezone_enum=timezone_enum)
        
        session.commit()
        session.query(IndustryCountry).filter(IndustryCountry.country_id == id).delete()
        if len(insert_industries) > 0:
            for industry_id in insert_industries:
                industry_country = IndustryCountry()
                industry_country.industry_id = industry_id
                industry_country.country_id = country.id
                session.add(industry_country)
                session.commit()
        
        return redirect(url_for("country", id=id))
    return render_template("country/countries.html", usersession=usersession, industries=industries)

@expose("/country/delete/<id>")
def country_delete(request, id):
    usersession = user_session(request)
    if not usersession or (usersession['usertype'] is not 1):
        return redirect(url_for('/'))
    print("ID: ", id)
    session.query(Country).filter(Country.id == id).delete()
    session.query(IndustryCountry).filter(IndustryCountry.country_id == id).delete()
    session.commit()
    return redirect(url_for("countries"))

@expose("/news/<news_type>")
def news(request, news_type):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    return render_template("news.html", news_type=news_type, usersession=usersession)

@expose("/country/<id>")
def country(request, id):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    country = session.query(Country).filter(Country.id == id).one()
    industries = session.query(Industry).filter(IndustryCountry.country_id == id).\
        join(IndustryCountry, Industry.id == IndustryCountry.industry_id).\
        options(
            Load(Industry).load_only("industry_name")
        ).all()
    
    return render_template("country/country_profile.html", country=country, usersession=usersession, industries=industries)

@expose("/countryadd")
def countryadd(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    return render_template("country_form.html", usersession=usersession)

@expose("/companylist")
def companylist(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    return render_template("company_profile.html", usersession=usersession)

@expose("/companyprofile/<company>")
def companyprofile(request, company):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    return render_template("company_profile.html", companyname=company, usersession=usersession)

@expose("/companyadd")
def companyadd(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    return render_template("company_form.html", usersession=usersession)

@expose("/industries")
def industries(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    return render_template("./industry/index.html")

def not_found(request):
    return render_template("not_found.html")
