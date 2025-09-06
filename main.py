from flask import Flask, render_template
from database.database import SessionLocal, init_db
from database.models import Apartment, Contact

app = Flask(__name__)

@app.route('/')
def index():
    db_session = SessionLocal()
    apartments = db_session.query(Apartment).all()
    return render_template('index.html', apartments=apartments)

@app.route('/contacts')
def contacts():
    db_session = SessionLocal()
    contacts = db_session.query(Contact).all()
    return render_template('contacts.html', contacts=contacts)

from apscheduler.schedulers.background import BackgroundScheduler
from scrapers.main import run_scrapers

if __name__ == "__main__":
    init_db()
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_scrapers, 'interval', days=1)
    scheduler.start()
    app.run(host='0.0.0.0', port=3000)

