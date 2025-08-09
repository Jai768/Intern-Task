from flask import Flask, render_template,request
import sqlite3
from main import scrape

app = Flask(__name__)

DB_FILE = "cases.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT,
            case_no INTEGER,
            scraped_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()

init_db()

def save_case(case_type, case_no, scraped_data):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO cases (case_type, case_no, scraped_data)
        VALUES (?, ?, ?)
        """, (case_type, case_no, scraped_data))
        conn.commit()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scrape",methods=["POST"])
def scrapy():
    case_no = request.form['case_no']
    case_type = request.form['ctype']
    response = scrape(case_type,case_no)
    save_case(case_type,case_no,str(response))
    return render_template("result.html",data=response)
app.run()