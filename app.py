from flask import Flask, redirect, render_template, request, session
from tempfile import mkdtemp
from flask_session import Session
from flask_mail import Mail, Message
import os
from werkzeug.security import check_password_hash
from helpers import login_required, create_connection

app = Flask(__name__)
mail = Mail(app)



""" ##TODO

        make index/suggested/new
        finish /admin --> upload new articles add admin tags to identify uploads
        make our team responsive (awainting csv)
        upload all articles
        Make accounts for all admins
        ADd other headings in navbar (ask Alazne)
        DO get involved
        finish submissions
        finish emails/register and send an email when someone registers
        Create article view count (maybe a linked table in SQL)
        make script to upload initial articles
        Optimize for mobile
        make sure JS for all exec team members is in place
        Make junior columnist and Ambassador Forms and pages

"""

app.config["MAIL_DEFAULT_SENDER"] = "thewrittenrevolutions@gmail.com"
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "thewrittenrevolutions"


app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    with create_connection("TWR.db") as con:
        db = con.cursor()
        content = list(db.execute("SELECT text FROM articles;"))
        con.commit()

    #if email:
    #    msg = Message("Hello", recipients=[email])
    #    mail.send(msg)
    
    return render_template("index.html", content=content)


@app.route("/email", methods =["POST"])
def email():
    email = request.form["email"]
    return render_template("email.html", email=email)


@app.route("/political")
def political():
    return redirect("search?q=political")

@app.route("/creative")
def creative():
    return redirect("search?q=creative")

@app.route("/ourmission")
def ourmission():
    return render_template("mission.html")

@app.route("/ourteam")
def mission():
    return render_template("ourteam.html")

@app.route("/submissions")
def submissions():
    return render_template("submissions.html")

@app.route("/getinvolved")
def getinvolved():
    return render_template("getinvolved.html")

@app.route("/search")
def search():
    ##implement search
    query = request.args.get("q")
    with create_connection("TWR.db") as con:
        db = con.cursor()
        SQ = "%" + query + "%"
        cmd = """SELECT titles, authors, descriptions, image FROM articles 
                WHERE tags LIKE ? OR authors LIKE ? OR descriptions LIKE ? OR titles LIKE ?;"""
        articles = list(db.execute(cmd, (SQ, SQ, SQ, SQ)))
        con.commit()

    for article in articles:
        print(article[0])
    return render_template("articles.html", title=query, articles=articles)


@app.route("/register", methods=["POST"])
def register():
    email = str(request.form["email"])
    firstname = str(request.form["firstname"])
    lastname = str(request.form["lastname"])
    tagslist = request.form.getlist("tags")
    print(email)
    tags = ""

    for tag in tagslist:
        if tags == "":
            tags = tag
        else:
            tags = tags + ", " + tag


    with create_connection("TWR.db") as con:
        db = con.cursor()
        check_cmd = "SELECT email FROM users;"
        check = list(db.execute(check_cmd))
        checker = True

        print((email,))

        for comp in check:
            print(comp)
            if email in comp:
                checker = False
                print("YES!")


        if  checker:
            cmd = "INSERT INTO users (email, firstname, lastname, tags) VALUES (?, ?, ?, ?);"
            db.execute(cmd, (email, firstname, lastname, tags))
            con.commit()

        ##send email

    return redirect("/")



@app.route("/admin_login")
@app.route("/admin_login/<string:name>", methods=["GET", "POST"])
def admin_login(name = "NoName"):
    
    session.clear()

    if name == "NoName":
        return render_template("admin_login.html", NoName=True)
    
    if request.method == "POST":
        password = request.form.get("password")
        
        with create_connection("TWR.db") as con:
            db = con.cursor()

            cmd = "SELECT hash FROM admins WHERE name = (?)"
            dbname = (name, )

            hashstring = list(db.execute(cmd, dbname))
            con.commit()

        if len(hashstring) != 1 or not check_password_hash(hashstring[0][0], password):
            
            return render_template("admin_login.html", name=name, failed=True)
        
        session["user_id"] = name
        return redirect(f"/admin/{name}")

    return render_template("admin_login.html", name=name)

@app.route("/admin")
@app.route("/admin/<string:name>")
@login_required
def admin(name="NoName"):
    if name == "NoName" and session.get("user_id") is None:
        return redirect("/admin_login")
    elif name == "NoName":
        name = session.get("user_id")
        redirect(f"/admin/{name}")
    return render_template("admin.html", name=name)


@app.route("/post", methods=["POST"])
@login_required
def post():
    name = session.get("user_id")

    return redirect(f"/admin/{name}")
@app.route("/addName", methods=["POST"])
def addName():
    name = request.form["name"]
    return redirect(f"/admin_login/{name}")

