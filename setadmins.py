from sys import argv, exit
import sqlite3
from werkzeug.security import generate_password_hash

if len(argv) != 3:
    exit("USAGE: python3 setadmins [NAME] [PASSWORD]")


name = argv[1]
password = generate_password_hash(argv[2])

with sqlite3.connect("TWR.db") as con:
    db = con.cursor()

    db.execute("INSERT INTO admins (name, hash) VALUES (?,?)", (name, password))

    con.commit()

print("Done!")