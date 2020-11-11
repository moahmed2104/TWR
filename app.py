from flask import Flask, redirect, render_template, request, session
from tempfile import mkdtemp
from flask_session import Session
import sqlite3

app = Flask(__name__)


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

userdb = create_connection("E:\\users.db")
articlesdb = create_connection("E:\\articles.db")
emailsdb = create_connection("E:\\emails.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/political")
def political():
    return render_template("article.html", title= "Political")

@app.route("/creative")
def creative():
    return render_template("article.html", title= "Creative")

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
