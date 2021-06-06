import json
from sqlalchemy import true
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect
from .models import URL, User
from .utils import expose, Pagination, render_template, session, url_for, validate_url

from secure_cookie.session import FilesystemSessionStore

session_store = FilesystemSessionStore()

def user_session(request):
    sid = request.cookies.get("wsessid")
    if not sid:
        return False

    the_session = session_store.get(sid)

    userdata = the_session['user']
    if not userdata:
        return False

    return userdata

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

@expose("/countries")
def countries(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    return render_template("country/country_list.html", usersession=usersession)

@expose("/newcountry")
def newcountry(request):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    
    if request.method == 'POST':
        print("Form DATA: ", request.form)
    return render_template("country/country_form.html", usersession=usersession)


@expose("/news/<news_type>")
def news(request, news_type):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    return render_template("news.html", news_type=news_type, usersession=usersession)

@expose("/country/<country>")
def country(request, country):
    usersession = user_session(request)
    if not usersession:
        return redirect(url_for('/'))
    print("Country Name: ", country)
    return render_template("country/country_profile.html", countryname=country, usersession=usersession)

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
