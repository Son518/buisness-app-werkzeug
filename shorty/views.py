from ast import Try
import json
from os import error
import os
from time import timezone
from sqlalchemy import true
from sqlalchemy.sql.functions import count
from sqlalchemy.orm import Load
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect
from werkzeug import secure_filename
from .models import Company, Industry, User, Country, IndustryCountry, Executive, News, Story, Video
from .utils import expose, Pagination, render_template, session, url_for, validate_url
from datetime import datetime
from nylas import APIClient
from cryptography.fernet import Fernet
from secure_cookie.session import FilesystemSessionStore
import random
import string

key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
fernet = Fernet(key)

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
    print(the_session)
    if 'user' in the_session:
        userdata = the_session['user']
        return json.loads(userdata)
    
    return False

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
        user = session.query(User).filter(User.email == email).one_or_none()
        
        if user is None:
            login_err_msg = "Invaild User!"
        else:
            print(fernet.decrypt(user.password.encode()).decode(), password)
            if fernet.decrypt(user.password.encode()).decode() == password:
                session_data = {
                    "usertype": user.usertype,
                    "username": user.username,
                    "id"      : user.id
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


# Profile
@expose("/profile/edit")
def profile_edit(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    user_id = usersession['id']
    user = session.query(User).filter(User.id == user_id).one_or_none()
    if request.method == "POST":
        form_data = request.form.to_dict(flat=True)
        print(form_data)
        for key in form_data:
            setattr(user, key, form_data[key])

        session.commit()
        return redirect(url_for('profile_view'))

    if user is not None:
        return render_template('account/edit.html', usersession=usersession, user=user)
    
    return redirect(url_for('/'))

@expose("/profile/view")
def profile_view(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    user_id = usersession['id']
    user = session.query(User).filter(User.id == user_id).one_or_none()
    return render_template('account/profile.html', usersession=usersession, user=user)

@expose('/forgot')
def forgot_password(request):
    if request.method == 'POST':
        email = request.form.get("email")
        user = session.query(User).filter(User.email==email).one_or_none()

        if user:
            letters = string.ascii_lowercase
            random_password = ''.join(random.choice(letters) for i in range(20))
            print("Random string of length", 20, "is:", random_password)

            encrypt_password = fernet.encrypt(random_password.encode())
            print("encrypt password: ", encrypt_password, encrypt_password.decode())

            user.password = encrypt_password
            session.commit()

            nylas = APIClient(
                "1rn7dql5wn17g16kpq1bngjk6",
                "cbwl6munoro37mvd23p39l9gf",
                "enSSJD52X0uyWsWIZEijt2ApOwTzYd",
            )
            draft = nylas.drafts.create()
            draft.subject = "BlueBiz Password Recovery"
            # Create the plain-text and HTML version of your message
            
            html = f"""\
            <html>
            <body>
                <p>Hi,<br>
                    Password Reset!<br>
                    <a href="http://www.bluebiz.com">BlueBiz</a>
                    Your New Password is {random_password}
                </p>
            </body>
            </html>
            """
            draft.body = html
            print("email content: ", html)
            draft.to = [{'name': 'BlueBiz Support Team', 'email': email}]

            draft.send()
            return render_template("email_sent.html")
            # return redirect(url_for("signin"))
        else:
            err_msg = "Not Registered Email!"
            return render_template("forgot_password.html", err_msg=err_msg)
    return render_template("forgot_password.html")

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
            
            encrypt_password = fernet.encrypt(password.encode())
            print("encrypt password: ", encrypt_password, encrypt_password.decode())
            newUser.password = encrypt_password
            session.add(newUser)
            session.commit()

            nylas = APIClient(
                "1rn7dql5wn17g16kpq1bngjk6",
                "cbwl6munoro37mvd23p39l9gf",
                "enSSJD52X0uyWsWIZEijt2ApOwTzYd",
            )
            draft = nylas.drafts.create()
            draft.subject = "BlueBiz Password Recovery"
            # Create the plain-text and HTML version of your message
            
            html = f"""\
            <html>
            <body>
                <p>Hi,<br>
                    Welcome to sign up Bluebiz!<br>
                    You signed up to Bluebiz.com successfully.
                    <a href="http://bluebiz.test.com">Please sign in</a>
                </p>
            </body>
            </html>
            """
            draft.body = html
            print("email content: ", html)
            draft.to = [{'name': 'BlueBiz Support Team', 'email': email}]

            draft.send()
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

# Country CRUD --------------
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
    industries = session.query(Industry).all()
    if request.method == 'GET':
        country = session.query(Country).filter(Country.id == id).one()
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

# Company CRUD ----------------
@expose("/companies")
def companies(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    
    company_type = request.args.get('type')
    if company_type is not None:
        companies = session.query(Company).filter(Company.company_type == company_type).all()
    else:
        companies = session.query(Company).all()

    for company in companies:
        company.industries= session.query(Industry.industry_name)\
            .join(IndustryCountry, IndustryCountry.industry_id==Industry.id)\
            .filter(company.id == IndustryCountry.company_id).all()
    
    return render_template("company/company_list.html", usersession=usersession, companies=companies)

@expose("/company/new")
def company_new(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    industries = session.query(Industry).all()
    if request.method == 'POST':
        form_data = request.form.to_dict(flat=False)
        insert_data = {}
        insert_industries = {}
        for key, value in form_data.items():
            if key == 'company_industry' or key == 'member_name' or key == 'member_title1' or key == 'member_title2':
                pass
            else:
                insert_data[key] = value[0]
        company = Company()
        for key,value in insert_data.items():
            setattr(company, key, value)
        if 'company_logo' in request.files:
            company_logo_file = request.files.get("company_logo")
            print("Company Logo File name: ", company_logo_file.filename)
            logo_path = os.path.join('./shorty/static/uploads/', secure_filename(company_logo_file.filename))
            company_logo_file.save(logo_path)
            company.company_logo = company_logo_file.filename

        session.add(company)
        session.commit()

        for key, value in form_data.items():
            if key == 'company_industry':
                insert_industries = value
            elif key == 'member_name':
                member_photos = request.files.getlist('member_photo')
                if len(member_photos) == 0:
                    pass
                index = 0
                for member_photo in member_photos:
                    path = os.path.join('./shorty/static/uploads/', secure_filename(member_photo.filename))
                    member_photo.save(path)
                    data = form_data
                    member_titles1 = data['member_title1']
                    member_titles2 = data['member_title2']
                    executive = Executive(name=value[index], title1=member_titles1[index], \
                        title2=member_titles2[index], photo=member_photo.filename, company_id=company.id)
                    index += 1
                    session.add(executive)
                    session.commit()
            elif key == 'member_title1' or key == 'member_title2': pass
            else:
                pass
       
        for industry_id in insert_industries:
            industry_country = IndustryCountry()
            industry_country.industry_id = industry_id
            industry_country.company_id = company.id
            session.add(industry_country)
            session.commit()
        return redirect(url_for("companies"))
    return render_template("company/company_form.html", usersession=usersession, industries=industries)

@expose("/company/<id>")
def company(request, id):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    company = session.query(Company).filter(Company.id == id).one()
    industries = session.query(Industry.industry_name).filter(IndustryCountry.company_id == id).\
        join(IndustryCountry, Industry.id == IndustryCountry.industry_id).all()
    executives = session.query(Executive).filter(Executive.company_id == id).all()
    return render_template("company/company_profile.html", company=company, usersession=usersession, industries=industries, executives=executives)

@expose("/company/edit/<id>")
def company_edit(request, id):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    company = session.query(Company).filter(Company.id == id).one()
    industries = session.query(Industry).all()
    if request.method == 'GET':
        selected_industries = session.query(Industry.id).filter(IndustryCountry.company_id == id).\
            join(IndustryCountry, Industry.id == IndustryCountry.industry_id).all()
        selected_industries = [item[0] for item in selected_industries]
        executives = session.query(Executive).filter(Executive.company_id == id).all()
        stories = session.query(Story).filter(Story.company_id == id).one_or_none()
        video = session.query(Video).filter(Video.company_id == id).one_or_none()
        print(industries, selected_industries)
        return render_template("company/company_edit.html", usersession=usersession, company=company, industries=industries, executives=executives, \
            selected_industries=selected_industries, stories=stories, video=video)
    
    if request.method == 'POST':
        form_data = request.form.to_dict(flat=False)

        insert_data = {}
        insert_industries = {}
        stories = {}

        for key, value in form_data.items():
            if key == 'company_industry':
                insert_industries = value
            elif key == 'member_name':
                member_photos = request.files.getlist('member_photo')
                # print("value: ", value)
            elif key == 'member_title1' or key == 'member_title2': pass
            elif key == 'title1' or key == 'title2' or key == 'content1' or key == 'content2':
                stories[key] = value[0]
            else:
                insert_data[key] = value[0]
        
        for key,value in insert_data.items():
            setattr(company, key, value)
        # if 'company_logo' in request.files:
        #     company_logo_file = request.files.get("company_logo")
        #     print("Company Logo File name: ", company_logo_file.filename)
        #     logo_path = os.path.join('./shorty/static/uploads/', secure_filename(company_logo_file.filename))
        #     company.company_logo = company_logo_file.filename
        session.commit()
        session.query(Story).filter(Story.company_id == id).delete()
        company_story = Story()
        print("Stories: ", stories)
        company_story.company_id = id
        company_story.title1 = stories['title1']
        company_story.title2 = stories['title2']
        company_story.content1 = stories['content1']
        company_story.content2 = stories['content2']
        session.add(company_story)
        session.commit()

        if 'company_video' in request.files:
            print("----------")
            video_file = request.files.get('company_video')
            path = os.path.join('./shorty/static/uploads/videos', secure_filename(video_file.filename))
            video_file.save(path)
            company_video = Video()
            company_video.company_id = id
            company_video.company_video = video_file.filename
            session.add(company_video)
            session.commit()

        session.query(IndustryCountry).filter(IndustryCountry.company_id == id).delete()
        for industry_id in insert_industries:
            industry_country = IndustryCountry()
            industry_country.industry_id = industry_id
            industry_country.company_id = company.id
            session.add(industry_country)
            session.commit()
        return redirect(url_for("companies"))

@expose("/company/byindustry")
def company_by_industry(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    industries = session.query(Industry).all()
    if request.method == 'GET':
        industry_id = request.args.get("industry")
        company_id = request.args.get("company")
        companies = None
        company = None
        executives = None
        industry_name = ''
        stories = {}
        video = {}
        if industry_id is not None:
            companies = session.query(Company.id, Company.company_name)\
                .join(IndustryCountry, IndustryCountry.company_id==Company.id)\
                .filter(IndustryCountry.industry_id == industry_id)\
                .all()
            industry_name = session.query(Industry.industry_name).filter(Industry.id == industry_id).one()
            print("Companies: ", companies, industry_name)
        if company_id is not None:
            company = session.query(Company).filter(Company.id == company_id).one()
            industries = session.query(Industry.industry_name).filter(IndustryCountry.company_id == company_id)\
                .join(IndustryCountry, Industry.id == IndustryCountry.industry_id).all()
            executives = session.query(Executive).filter(Executive.company_id == company_id).all()
            stories = session.query(Story).filter(Story.company_id == company_id).one_or_none()
            video = session.query(Video).filter(Video.company_id == company_id).one_or_none()
            print("Company: ", company, executives)
        if company or companies:
            return render_template('company/company_by_industry.html', companies=companies, \
                credential=industry_name.industry_name+" Industry?", company=company, industry_id=industry_id, \
                executives=executives, industries=industries, stories=stories, video=video, usersession=usersession)
    return render_template('company/company_by_industry.html', industries=industries, credential='Industry', usersession=usersession)

@expose("/company/delete/<id>")
def company_delete(request, id):
    session.query(Executive).filter(Executive.company_id == id).delete()
    session.query(IndustryCountry).filter(IndustryCountry.company_id == id).delete()
    session.query(Company).filter(Company.id == id).delete()
    session.commit()
    return redirect(url_for('companies'))

@expose("/industries")
def industries(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    return render_template("./industry/index.html")

def not_found(request):
    return render_template("not_found.html")

# News CRUD -------------------
@expose("/news/<news_type>")
def news(request, news_type):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    return render_template("news.html", news_type=news_type, usersession=usersession)

@expose("/newslist")
def newslist(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    allnews = session.query(News).all()
    return render_template("news/newslist.html", usersession=usersession, allnews=allnews)

@expose("/news/add")
def news_add(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))

    if request.method == "POST":
        form_data = request.form.to_dict(flat=False)
        insert_data = {}
        currentTime = datetime.now()
        insert_data['news_created'] = currentTime
        if 'news_image' in request.files:
            news_image = request.files.get("news_image")
            insert_data['news_image'] = news_image.filename
            print("news image name: ", news_image.filename)
            upload_folder = '/var/www/bluebiz/'
            path = os.path.join(upload_folder+'shorty/static/uploads/news/', secure_filename(news_image.filename))
            news_image.save(path)
        
        for key, value in form_data.items():
            insert_data[key] = value[0]
        news = News()
        for key,value in insert_data.items():
            setattr(news, key, value)
        session.add(news)
        session.commit()
        return redirect(url_for("newslist"))
    return render_template("news/newsadd.html", usersession=usersession)

@expose("/newsview/<id>")
def news_detail(request, id):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    news = session.query(News).filter(News.id==id).one()
    return render_template("news/newsdetail.html", usersession=usersession, news=news)

@expose("/news/edit/<id>")
def news_edit(request, id):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    news = session.query(News).filter(News.id==id).one()
    if request.method == "POST":
        form_data = request.form.to_dict(flat=False)
        print("Update News: ", form_data)
        insert_data = {}
        currentTime = datetime.now()
        insert_data['news_created'] = currentTime
        
        for key, value in form_data.items():
            insert_data[key] = value[0]
        
        print("Insert Data: ", insert_data)
        for key,value in insert_data.items():
            setattr(news, key, value)
        session.commit()
        return redirect(url_for("newslist"))
    return render_template("news/newsedit.html", usersession=usersession, news=news)

@expose("/news/delete/<id>")
def news_delete(request, id):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    session.query(News).filter(News.id==id).delete()
    session.commit()
    return redirect(url_for("newslist"))

@expose("/industres")
def industries(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    industries = session.query(Industry).all()
    return render_template('industry/index.html', industries=industries, usersession=usersession)

@expose("/industry/<id>")
def industry(request, id):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    industry = session.query(Industry).filter(Industry.id == id).one()

    if request.method == 'POST':
        industry_name = request.form.get('industry_name')
        print("Industry Name", industry_name)
        industry.industry_name = industry_name
        session.commit()
        return redirect(url_for("industries"))
    return render_template('industry/edit.html', industry=industry, usersession=usersession)

@expose("/industry/add")
def industry_add(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    if request.method == "POST":
        industry_name = request.form.get('industry_name')
        industry = Industry()
        industry.industry_name = industry_name
        session.add(industry)
        session.commit()
    return render_template('industry/add.html', usersession=usersession)

@expose("/industry/del/<id>")
def industry_del(request, id):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    session.query(Industry).filter(Industry.id == id).delete()
    session.commit()
    return redirect(url_for("industries"))

# footer links
@expose("/about")
def about_bluebiz(request):
    return render_template('footer/about_bluebiz.html')

@expose("/advertise")
def advertise(request):
    return render_template('footer/advertise.html')
    
@expose("/privacyPolicy")
def privacy_policy(request):
    return render_template('footer/privacy_policy.html')

@expose("/cookiePolicy")
def cookie_policy(request):
    return render_template('footer/cookie_policy.html')

@expose("/dataPolicy")
def data_policy(request):
    return render_template('footer/data_policy.html')

@expose("/careers")
def careers(request):
    return render_template('footer/careers.html')

@expose("/subscriberAgreement")
def subscriber_agreement(request):
    return render_template('footer/subscriber_agreement.html')

@expose("/trademarks")
def trademarks(request):
    return render_template('footer/trademarks.html')

@expose("/copyrightPolicy")
def copyright_policy(request):
    return render_template('footer/copyright_policy.html')

@expose("/contactus")
def contactus(request):
    return render_template('footer/contactus.html')

@expose("/helpcenter")
def helpcenter(request):
    return render_template('footer/help_center.html')
