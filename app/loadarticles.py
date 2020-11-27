import csv
import sqlite3


file = open("static/articles.csv")

reader = csv.DictReader(file)

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except ValueError as e:
        print(f"The error '{e}' occurred")

    return connection
i =0
with create_connection("TWR.db") as con:
    db = con.cursor()
    for row in reader:
        sql = "INSERT INTO articles (titles, authors, descriptions, tags, text, image, date) VALUES (?, ?, ?, ?, ?, ?, ?);"
        db.execute(sql, (row["titles"], row["authors"], row["descriptions"], row["tags"], row["text"], row["image"], row["date"]))
        con.commit()
        i = i + 1

print(i)