from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # You can change this later

# ✅ Initialize DB if not exists
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

# ✅ Home route
@app.route('/')
def home():
    return render_template('home.html')

# ✅ Post trip
@app.route('/post-trip', methods=['GET', 'POST'])
def post_trip():
    if request.method == 'POST':
        data = {
            'departure_station': request.form['departure_station'],
            'arrival_station': request.form['arrival_station'],
            'departure_time': request.form['departure_time'],
            'nickname': request.form['nickname'],
            'contact_info': request.form['contact_info']
        }

        conn = sqlite3.connect('trips.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO trips (departure_station, arrival_station, departure_time, nickname, contact_info)
            VALUES (:departure_station, :arrival_station, :departure_time, :nickname, :contact_info)
        ''', data)
        conn.commit()
        conn.close()

        flash('✅ Trip successfully posted!')
        return redirect(url_for('home'))

    return render_template('post_trip.html')

# ✅ Find trip
@app.route('/find-trip', methods=['GET', 'POST'])
def find_trip():
    if request.method == 'POST':
        departure = request.form['departure_station']
        arrival = request.form['arrival_station']
        requested_time = datetime.fromisoformat(request.form['departure_time'])

        conn = sqlite3.connect('trips.db')
        c = conn.cursor()
        c.execute('SELECT departure_station, arrival_station, departure_time, nickname, contact_info FROM trips')
        trips = c.fetchall()
        conn.close()

        matches = []
        other_matches = []

        for trip in trips:
            trip_departure, trip_arrival, trip_time_str, nickname, contact_info = trip
            trip_time = datetime.fromisoformat(trip_time_str)

            if trip_departure.lower() == departure.lower() and trip_arrival.lower() == arrival.lower():
                if abs((trip_time - requested_time).total_seconds()) <= 1800:
                    matches.append({
                        'departure_station': trip_departure,
                        'arrival_station': trip_arrival,
                        'departure_time': trip_time.strftime('%Y-%m-%d %H:%M'),
                        'nickname': nickname,
                        'contact_info': contact_info
                    })
                elif trip_time.date() == requested_time.date():
                    other_matches.append({
                        'departure_station': trip_departure,
                        'arrival_station': trip_arrival,
                        'departure_time': trip_time.strftime('%Y-%m-%d %H:%M'),
                        'nickname': nickname,
                        'contact_info': contact_info
                    })

        return render_template('match_results.html', matches=matches, other_matches=other_matches)

    return render_template('find_trip.html')

# ✅ About route
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
