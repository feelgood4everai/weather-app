from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# Get API key from environment variable
API_KEY = os.environ.get('OPENWEATHER_API_KEY', 'your-api-key')
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

@app.route('/')
def index():
    weather = None
    city = None
    error = None
    
    if request.args.get('city'):
        city = request.args.get('city')
        params = {'q': city, 'appid': API_KEY, 'units': 'metric'}
        
        try:
            response = requests.get(BASE_URL, params=params)
            data = response.json()
            
            if data.get('cod') == 200:
                weather = {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temp': round(data['main']['temp']),
                    'feels_like': round(data['main']['feels_like']),
                    'humidity': data['main']['humidity'],
                    'description': data['weather'][0]['description'].title(),
                    'icon': data['weather'][0]['icon']
                }
            else:
                error = f"City '{city}' not found. Please try again."
        except Exception as e:
            error = "Error fetching weather data."
    
    return render_template('index.html', weather=weather, city=city, error=error)

if __name__ == '__main__':
    app.run(debug=True)
