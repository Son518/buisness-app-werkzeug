import re
from werkzeug.exceptions import NotFound
from werkzeug.utils import redirect
from werkzeug import Response
import json
from .models import URL, User
from .utils import expose, Pagination, render_template, session, url_for, validate_url

from secure_cookie.session import FilesystemSessionStore
# from werkzeug.wrappers import Request, Response

session_store = FilesystemSessionStore()

@expose("/test1")
def test1(request):

    # sid = request.cookies.get('cookie_name')
    #
    # if sid is None:
    #     request.session = session_store.new()
    # else:
    #     request.session = session_store.get(sid)

    new_session = session_store.new()

    new_session['user'] = 'Joe'

    session_store.save(new_session)

    # response = Response(do_stuff(request))
    response = Response('Hello World!')

    # if request.session.should_save:
    response.set_cookie("session_id", new_session.sid)

    return response

@expose("/test2")
def test2(request):
    sid = request.cookies.get("wsessid")
    the_session = session_store.get(sid)
    response = Response('User is ' + the_session['user'])
    return response

@expose("/")
def index(request):
    return render_template("index.html")

@expose("/signin")
def signin(request):
    return render_template("signin.html")

@expose("/onsignin")
def onsignin(request):
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        print("Email: ", email, " Password: ", password)
        result = session.query(User).filter(User.email == email)
        if not result:
            return redirect(url_for("/signin"))
        for row in result:
            if row.password == password:
                print(row.username, row.password)

                response = redirect(url_for("/"))

                new_session = session_store.new()
                new_session['user'] = 'Cathy'
                session_store.save(new_session)
                response..set_cookie("wsess", new_session.sid)

                return response

    # contents = json.dumps({'say': 'hello'})
    # return Response(contents, content_type="application/json")

@expose("/news/<news_type>")
def news(request, news_type):
    print("NEWS TYPE: ", news_type)
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

"""
https://upwork-usw2-prod-file-storage-wp1.s3.us-west-2.amazonaws.com/workplace/attachment/7aad6c5aa01b188ca465b5c2498f7815?response-content-disposition=inline%3B%20filename%3D%22Pasted%2520File%2520at%2520May%252013%252C%25202021%25208%253A20%2520AM.png%22%3B%20filename%2A%3Dutf-8%27%27Pasted%2520File%2520at%2520May%252013%252C%25202021%25208%253A20%2520AM.png&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEEkaCXVzLXdlc3QtMiJHMEUCIDboTmTauqDjzeisZS74z%2FX0GAcoOIedEXNr1%2BcLQcMEAiEAiIO0KxI%2BMCgntTA%2BJfFWs0ISBaj6dN4TCwTmTL%2FKwl8q1gQI0v%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw3Mzk5MzkxNzM4MTkiDH2UTZfyeX%2FXjYQxsCqqBLXvjTl0OvnXUD419ipArpiJM4vL%2BJb05DEudgl0QqOWp7FWViS9RwvRe5U%2Bop6%2BQ99qCTV%2F4gdOCiZNOQ2FVU2Gr9BwHa9RiNcVEEOhavAW7%2FCutBqOQYdCtq7fV4MFFhgaFv9ELXl3QGnHqvU7Mae0CMHwKjISl1mvrJ6cEEv6aP1YtShd575XqsZvrHKItApZ6rCh5O%2FSClEgfEyTjxXA3MDL8XZKlvMSUyZymcCakbZk%2B4dTasocArfL3p5xJ0AbLVCcG36qLI6laLwsdPpFmcomNsdCxlDTYp4ArprDEK%2Bo7m0G56ZO8iVVEzgg0JDAv%2BS57ZZWC92J5rLUjE57sERYu3Ytia3oAB8%2BZ3vZRtVtjxVTNBH9Q3XzastekjdTAV7%2BAjxq4zKWcZOofrijxnmxbBjYmoDT%2Bt5dwQ0irBaAOa6l7qbUBTijgoGE9B5yxxwNX69uQv%2BjYA6LdFbUajua6J%2FRiaEXhMaSo%2BQ%2FAJT79CjOJqN4CFF0JPxvtyRlMVdjCwWCypwS0nYHGlCY9%2BUI5gbfDeNbsfHgCLyxq9GRUNcOXZ6gWElX5GtJdw%2Fe8zEsZSj%2FKFMbRSs79svUz5tKRZwafZHNEWT5jCJoL0Jg%2BCc6J2W4byuMr5HS6bd6VW5aTYDZCX67vOv0H59qziMZuwsWiKLJhy0LYPaP1OYg6yq5eZyMPXijrRSJPizYoVSR%2FJWrCZWDD9IMpW2PasHgRNsvyzo6MIPN84QGOqcBiON2A%2BeCAHUd4rL1f%2Fw8ugTXBx%2FHosFx3mh9YXXjPbQn7K7zMPLom6JkUXSf8hhiHWELJ9ZHkzb2Htc14ZWIx9Lg%2FjMk%2B2CxR08iA%2FpE8mhGkFTWJYnpX%2FOc7%2Fh%2FXd2bpUjxTOxYnQyOQCQwdPVf9Npt0NXK5hb47nifmY3vL0shc%2Fh3Fipxy2gVIx8DFfg%2FjV0Ca8oJPBJAkckhKGQj2yYUh729eBs%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20210513T105644Z&X-Amz-SignedHeaders=host&X-Amz-Expires=599&X-Amz-Credential=ASIA2YR6PYW5YJTNLDHR%2F20210513%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Signature=7eda7af046888be4d0e46e204b0ff60edbace4d805753607b84b90f9a86685dc

(I don't need the purple arrow, just the text) """
