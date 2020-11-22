from flask import redirect, request, session
from functools import wraps
import sqlite3

def create_con(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except ValueError as e:
        print(f"The error '{e}' occurred")

    return connection

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin_id") is None:
            return redirect("/admin_login")
        return f(*args, **kwargs)
    return decorated_function