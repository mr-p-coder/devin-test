# Devin Test — Simple Weather App

This is a minimal Flask app that returns current weather for the browser's location.

Requirements:
- Python 3.8+
- An OpenWeather API key (https://openweathermap.org/api). Set it as OPENWEATHER_API_KEY.

Run locally:
1. python -m venv venv
2. source venv/bin/activate   # Windows: venv\\Scripts\\activate
3. pip install -r requirements.txt
4. export OPENWEATHER_API_KEY=your_key_here   # Windows: set OPENWEATHER_API_KEY=your_key_here
5. python app.py
6. Open http://127.0.0.1:5000 in your browser and click "Get weather for my location".

Notes:
- The server must be able to reach the OpenWeather API.
- For production, don't run with debug=True and consider using a WSGI server.
