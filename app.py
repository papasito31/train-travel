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
            departure_time TEXT NOT NULL,
            nickname TEXT,
            contact_info TEXT
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
        nickname = request.form['nickname']
        contact_info = request.form['contact_info']

        conn = sqlite3.connect('trips.db')
        c = conn.cursor()
        c.execute('INSERT INTO trips (departure_station, arrival_station, departure_time, nickname, contact_info) VALUES (?, ?, ?, ?, ?)',
                  (departure_station, arrival_station, departure_time, nickname, contact_info))
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
        c.execute('SELECT departure_station, arrival_station, departure_time, nickname, contact_info FROM trips')
        all_trips = c.fetchall()
        conn.close()

        matches = []
        for trip in all_trips:
            trip_departure, trip_arrival, trip_time, nickname, contact_info = trip
            trip_time_dt = datetime.fromisoformat(trip_time)

            if (trip_departure.lower() == departure_station.lower() and
                trip_arrival.lower() == arrival_station.lower() and
                abs((trip_time_dt - departure_time).total_seconds()) <= 1800):
                matches.append({
                    'departure_station': trip_departure,
                    'arrival_station': trip_arrival,
                    'departure_time': trip_time_dt.strftime('%Y-%m-%d %H:%M'),
                    'nickname': nickname,
                    'contact_info': contact_info
                })

        return render_template('match_results.html', matches=matches)

    return render_template('find_trip.html')

if __name__ == '__main__':
    app.run(debug=True)
