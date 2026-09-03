from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify({'error': 'Missing lat or lon'}), 400

    api_key = os.environ.get('OPENWEATHER_API_KEY')
    if not api_key:
        return jsonify({'error': 'Server missing OPENWEATHER_API_KEY env var'}), 500

    try:
        res = requests.get('https://api.openweathermap.org/data/2.5/weather', params={
            'lat': lat,
            'lon': lon,
            'appid': api_key,
            'units': 'metric'
        }, timeout=10)
        res.raise_for_status()
        data = res.json()

        weather = {
            'name': data.get('name'),
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
        }
        return jsonify(weather)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
