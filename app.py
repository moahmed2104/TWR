from flask import Flask, redirect, render_template, request, session
from tempfile import mkdtemp
from flask_session import Session
import sqlite3
from flask_mail import Mail, Message
import os


app = Flask(__name__)
mail = Mail(app)


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

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except ValueError as e:
        print(f"The error '{e}' occurred")

    return connection


@app.route("/", methods =["GET", "POST"])
def index():
    with create_connection("TWR.db") as con:
        db = con.cursor()
        content = list(db.execute("SELECT text FROM articles;"))
        con.commit()
    
   
    ##email = request.form["email"]

    
    #if email:
    #    msg = Message("Hello", recipients=[email])
    #    mail.send(msg)
    
    return render_template("index.html", content=content)

#app rout for email --> send email --> add email to database--> redirect to #
@app.route("/email", methods=["GET", "POST"])
def email():
    return redirect("#")

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
