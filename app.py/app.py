from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

# Veritabanı başlatma
def init_db():
    conn = sqlite3.connect('trips.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            departure_station TEXT NOT NULL,
            arrival_station TEXT NOT NULL,
            departure_time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/post-trip', methods=['GET', 'POST'])
def post_trip():
    if request.method == 'POST':
        departure_station = request.form['departure_station']
        arrival_station = request.form['arrival_station']
        departure_time = request.form['departure_time']

        conn = sqlite3.connect('trips.db')
        c = conn.cursor()
        c.execute('INSERT INTO trips (departure_station, arrival_station, departure_time) VALUES (?, ?, ?)',
                  (departure_station, arrival_station, departure_time))
        conn.commit()
        conn.close()

        return redirect(url_for('home'))

    return render_template('post_trip.html')

@app.route('/find-trip', methods=['GET', 'POST'])
def find_trip():
    if request.method == 'POST':
        departure_station = request.form['departure_station']
        arrival_station = request.form['arrival_station']
        departure_time = datetime.fromisoformat(request.form['departure_time'])

        conn = sqlite3.connect('trips.db')
        c = conn.cursor()
        c.execute('SELECT departure_station, arrival_station, departure_time FROM trips')
        all_trips = c.fetchall()
        conn.close()

        matches = []
        for trip
