from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather')
def weather():
    # Accept either a zip/postal code or lat+lon
    zip_code = request.args.get('zip')
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not zip_code and (not lat or not lon):
        return jsonify({'error': 'Provide zip OR lat and lon'}), 400

    api_key = os.environ.get('OPENWEATHER_API_KEY')
    if not api_key:
        return jsonify({'error': 'Server missing OPENWEATHER_API_KEY env var'}), 500

    params = {'appid': api_key, 'units': 'metric'}
    if zip_code:
        # OpenWeather accepts 'zip' as e.g. '94040,us' or just '94040'
        params['zip'] = zip_code
    else:
        params['lat'] = lat
        params['lon'] = lon

    try:
        res = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params, timeout=10)
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
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    except Exception:
        return jsonify({'error': 'Unexpected response format from weather provider'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
