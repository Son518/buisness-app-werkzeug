import json
from sqlalchemy import true
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect
from .models import URL, User
from .utils import expose, Pagination, render_template, session, url_for, validate_url, auth_check, session_store

from secure_cookie.session import FilesystemSessionStore

session_store = FilesystemSessionStore()

def user_session(request):
    sid = request.cookies.get("wsessid")
    if not sid:
        return False

    the_session = session_store.get(sid)
    user = the_session['user']
    if not user or user != 'Joe':
        return redirect(url_for("test_login"))

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
    return render_template("signin.html")

@expose("/onsignin")
def onsignin(request):
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        result = session.query(User).filter(User.email == email)
        print("dddds", result.count())
        if result.count() == 0:
            return redirect(url_for('/'))
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
                print("wrong password")
                return redirect(url_for('signin'))

@expose("/signup")
def signup(request):
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if password == confirm_password:
<<<<<<< HEAD
            newUser = User()
            newUser.email = email
            newUser.password = password
            session.add(newUser)
            session.flush()
            result = session.query(User).filter(User.email == email)
            print("SIGN UP: ", result.count())
=======
            session.query(User).filter(User.email == email)

        print("SIGN UP: ", email, password, confirm_password)
>>>>>>> 2b9913c145508f958bdde6d24327ba4c8ce924f3
        if email is True:
            return 'ddd'
        return redirect(url_for('/'))

@expose("/signout")
def signout(request):
    response = redirect(url_for("/"))
    response.set_cookie("wsessid")
    return response

@expose("/profile")
def profile(request):
    usersession = user_session(request)
    print("usersession on profile: ", usersession)
    if not usersession:
        return redirect(url_for('/'))
    return render_template("profile.html", usersession=usersession)

@expose("/news/<news_type>")
def news(request, news_type):
    return render_template("news.html", news_type=news_type)

@expose("/countryprofile/<country>")
def countryprofile(request, country):
    print("Country Name: ", country)
    return render_template("country_profile.html", countryname=country)

@expose("/countryadd")
def countryadd(request):
    return render_template("country_form.html")

@expose("/companylist")
def companylist(request):
    return render_template("company_profile.html")

@expose("/companyprofile/<company>")
def companyprofile(request, company):
    return render_template("company_profile.html", companyname=company)

@expose("/companyadd")
def companyadd(request):
    return render_template("company_form.html")

@expose("/industries")
def industries(request):
    return render_template("./industry/index.html")

@expose("/new")
def new(request):
    error = url = ""
    if request.method == "POST":
        url = request.form.get("url")
        alias = request.form.get("alias")
        if not validate_url(url):
            error = "I'm sorry but you cannot shorten this URL."
        elif alias:
            if len(alias) > 140:
                error = "Your alias is too long"
            elif "/" in alias:
                error = "Your alias might not include a slash"
            elif URL.query.get(alias):
                error = "The alias you have requested exists already"
        if not error:
            uid = URL(url, "private" not in request.form, alias).uid
            session.commit()
            return redirect(url_for("display", uid=uid))
    return render_template("new.html", error=error, url=url)

@expose("/display/<uid>")
def display(request, uid):
    url = URL.query.get(uid)
    print("UID: ", uid)
    if not url:
        raise NotFound()
    return render_template("display.html", url=url)


@expose("/u/<uid>")
def link(request, uid):
    url = URL.query.get(uid)
    if not url:
        raise NotFound()
    return redirect(url.target, 301)


@expose("/list/", defaults={"page": 1})
@expose("/list/<int:page>")
def list(request, page):
    query = URL.query.filter_by(public=True)
    pagination = Pagination(query, 30, page, "list")
    if pagination.page > 1 and not pagination.entries:
        raise NotFound()
    return render_template("list.html", pagination=pagination)


def not_found(request):
    return render_template("not_found.html")
