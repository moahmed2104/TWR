from flask import Flask, redirect, render_template, request, session, flash
from tempfile import mkdtemp
from flask_session import Session
from flask_mail import Mail, Message
import os
import werkzeug
from werkzeug.security import check_password_hash
from helpers import *
import csv
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
mail = Mail(app)

UPLOAD_FOLDER = "/uploads"


""" ##TODO
        Make accounts for all admins
        Make the email have html so it looks nice
        email all users that have signed-up whenever an article with their tag is posted "SELECT email FROM users WHERE tags LIKE '%tag_of_the_article%';" 
        
        Post Production:
            Make suggested usingg cookies and add cookie disclaimer
            add eazter egg using gmap on ze coin in hansonz image linking to sommezing estubid
            mmake submissions accept files and email them
"""

## SET configurations
app.config["MAIL_DEFAULT_SENDER"] = "thewrittenrevolutions@gmail.com"#"yelmays@icloud.com" #"moahmed2104@gmail.com"
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_PORT"] = 587#465#
app.config["MAIL_SERVER"] = "smtp.gmail.com"#"smtp.mail.me.com"#
app.config["MAIL_USE_TLS"] = True
#app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "thewrittenrevolutions@gmail.com"#"yelmays@icloud.com"#"moahmed2104@gmail.com"
app.config["MAIL_ASCII_ATTACHMENTS"] = True

app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

Session(app)

mail = Mail(app)


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

#index
@app.route("/")
def index():
    with create_con("TWR.db") as con:
        db = con.cursor()
        ##Select 9 last articles
        db.execute("SELECT titles, authors, descriptions, image, id, date FROM articles ORDER BY id DESC LIMIT 5;")
        content = db.fetchall()
        con.commit()

        db.execute("SELECT  titles, authors, descriptions, image, id, date FROM articles ORDER BY count DESC LIMIT 3;")
        popular = db.fetchall()
        con.commit()

    return render_template("index.html", articles=content, popular=popular)

#email function
@app.route("/email", methods =["POST"])
def email():
    email = request.form["email"]
    return render_template("email.html", email=email)

@app.route("/ourmission")
def ourmission():
    return render_template("mission.html")

#Executive page getting the team information from the .csv
@app.route("/execs")
def mission():
    people = []
    with open("static/execs.csv") as f:
        reader = csv.DictReader(f)

        for row in reader:
            row["profile_photo"] = row["profile_photo"].rpartition('id=')[2]
            print(row["profile_photo"].rpartition('id='))
            print(row["fullname"], row["profile_photo"])
            people.append(row)
    
    return render_template("execs.html", people=people)

@app.route("/junior")
def junior():
    people = []
    with open("static/junior.csv") as f:
        reader = csv.DictReader(f)

        for row in reader:
            row["profile_photo"] = row["profile_photo"].rpartition('id=')[2]
            print(row["profile_photo"].rpartition('id='))
            print(row["fullname"], row["profile_photo"])
            people.append(row)
    
    return render_template("junior.html", people=people)

@app.route("/amb")
def amb():
    people = []
    with open("static/amb.csv") as f:
        reader = csv.DictReader(f)

        for row in reader:
            row["profile_photo"] = row["profile_photo"].rpartition('id=')[2]
            print(row["profile_photo"].rpartition('id='))
            print(row["fullname"], row["profile_photo"])
            people.append(row)
    
    return render_template("amb.html", people=people)

@app.route("/submissions", methods=["GET","POST"])
def submissions():
    if request.method == "POST":
        print(request.files)

        if 'fileemail' not in request.files:
            flash('No file part')
            return redirect(request.url)
        msg = Message('New Submission!', recipients = ['moahmed2104@gmail.com'])
        name = request.form["name"]
        email = request.form["email"]
        f = request.files["fileemail"]
        
        if f: 
            filename = secure_filename(f.filename)            
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            msg.body = f"Submission by: {name} <{email}> \n"
            with app.open_resource(filename) as fp:
                msg.attach(os.path.join(app.config['UPLOAD_FOLDER'], filename), fp.read())
            mail.send(msg)
            return render_template("index.html", sent = True)
        flash('No selected file')
        return redirect(request.url)

    return render_template("submissions.html")

@app.route("/search")
def search():
    ##get query
    query = request.args.get("q")

    ##interact with database
    with create_con("TWR.db") as con:
        db = con.cursor()
        SQ = "%" + query + "%"
        cmd = """SELECT titles, authors, descriptions, image, date, id FROM articles 
                WHERE tags LIKE ? OR authors LIKE ? OR descriptions LIKE ? OR titles LIKE ? 
                ORDER BY id DESC;"""
        articles = list(db.execute(cmd, (SQ, SQ, SQ, SQ)))
        con.commit()

    return render_template("articles.html", title=query, articles=articles)

#email registration function
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


    with create_con("TWR.db") as con:
        db = con.cursor()
        check_cmd = "SELECT id FROM users WHERE email = ?;"  #Selecting emails from database to email
        check = list(db.execute(check_cmd, (email,)))
        checker = True

        if check:
            checker = False
            print("YES!")


        if  checker:
            print("HI")
            cmd = "INSERT INTO users (email, firstname, lastname, tags) VALUES (?, ?, ?, ?);"
            db.execute(cmd, (email, firstname, lastname, tags))
            con.commit()
        print("passed!")
        msg = Message('TWR Subscription!', recipients = [f"{email}"])
        print("Good Job")
        msg.body="Thank you for subscribing to The Written Revolutions email updates, you will get an email whenever there is a post related to one of the topics you are interested in."
        print("almost there")
        mail.send(msg)
        print("All done!")

    return redirect("/")



@app.route("/admin_login")
@app.route("/admin_login/<string:name>", methods=["GET", "POST"])
def admin_login(name = "NoName"):
    
    session.clear()

    if name == "NoName":
        return render_template("admin_login.html", NoName=True)
    
    if request.method == "POST":
        password = request.form.get("password")
        
        with create_con("TWR.db") as con:
            db = con.cursor()

            cmd = "SELECT hash FROM admins WHERE name = (?)"
            dbname = (str(name).lower(), )

            hashstring = list(db.execute(cmd, dbname))
            con.commit()

        if len(hashstring) != 1 or not check_password_hash(hashstring[0][0], password):
            
            return render_template("admin_login.html", name=name, failed=True)
        
        session["admin_id"] = name
        return redirect(f"/admin/{name}")
        
    return render_template("admin_login.html", name=name)

@app.route("/admin")
@app.route("/admin/<string:name>")
@login_required
def admin(name="NoName"):
    if name == "NoName" and session.get("admin_id") is None:
        return redirect("/admin_login")
    elif name == "NoName":
        name = session.get("admin_id")
        redirect(f"/admin/{name}")
    return render_template("admin.html", name=name)


@app.route("/post", methods=["POST"])
@login_required
def post():
    name = session.get("admin_id")
    title = request.form.get("title")
    authors = request.form.get("authors")
    description = request.form.get("description")
    content = request.form.get("content")
    tags = request.form.get("tags")
    img = request.form.get("image")
    date = request.form.get("date")

    email_tags = request.form.getlist("email_tags")

    with create_con("TWR.db") as con:
        db = con.cursor()
        MAXID = list(db.execute("SELECT MAX(id) FROM articles"))
        id = MAXID[0][0] + 1
        admin_id = list(db.execute("SELECT id FROM admins WHERE name = ?", (name, )))

        db.execute("INSERT INTO articles (titles, authors, descriptions, tags, text, image, date, admin_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", (title, authors, description, tags, f"static/articles/{id}.txt", img, date, admin_id))
    

    f = open(f"static/articles/{id}.txt", "w")
    f.write(content)
    f.close()


    return redirect(f"/admin/{name}")
@app.route("/addName", methods=["POST"])
def addName():
    name = request.form["name"]
    return redirect(f"/admin_login/{name}")


@app.route("/article")#/<string:articleid>")
def article():
    articleid = request.args.get("articleid")

    with create_con("TWR.DB") as con:
        db = con.cursor()
        print(articleid)
        id = list(db.execute("SELECT id FROM articles WHERE id = ?", (articleid,)))
        print(id[0][0])
        
        contents = list(db.execute("SELECT titles, authors, image, count, date FROM articles WHERE id = ?", id[0]))
        print(contents)
        db.execute("UPDATE articles set count = ? WHERE id = ?", (int(contents[0][3]) + 1, id[0][0]))



    print(contents)

    file = open(f"static/articles/{articleid}.txt", "r")
    text = file.read()
    file.close()

    return render_template("article.html", contents=contents, text = text)