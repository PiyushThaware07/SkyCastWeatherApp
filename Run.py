from flask import Flask, render_template, request
import requests

app = Flask(__name__)


# Emoji
weather_emojis = {
    'clear sky': u'\U00002600',
    'few clouds': u'\U000026C5',
    'scattered clouds': u'\U0001F324',
    'broken clouds': u'\U0001F325',
    'clouds': u'\U00002601',
    'shower rain': u'\U0001F327',
    'rain': u'\U0001F327',
    'thunderstorm': u'\U000026C8',
    'snow': u'\U0001F328',
    'mist': u'\U0001F32B',
    'wind face': u'\U0001F32C',
    'cyclone': u'\U0001F300',
    'rainbow': u'\U0001F308',
    'umbrella': u'\U00002614',
    'sun behind cloud': u'\U0001F325',
    'sun behind rain cloud': u'\U0001F326',
    'sun behind large cloud': u'\U0001F324',
    'sun behind small cloud': u'\U0001F323',
    'cloud with rain': u'\U0001F327',
    'cloud with snow': u'\U0001F328',
    'cloud with lightning': u'\U0001F329',
    'tornado': u'\U0001F32A',
    'fog': u'\U0001F32B',
    'thermometer': u'\U0001F321',
    'snowman': u'\U000026C4',
    'snowflake': u'\U00002744',
    'sun with face': u'\U0001F31E',
    'full moon with face': u'\U0001F31D',
    'partly sunny': u'\U000026C5',
    'snow': u'\U0001F328',
    'mist': u'\U0001F32B',
    'haze': u'\U0001F32B',
    'light rain': u'\U0001F326'
}

weather_images = {
    'rain':'img/rain.jpg',
    'haze':'img/haze.jpg',
    'clear sky': 'img/clear_sky.jpg',
    'mist':'img/mist.jpg',
    'thunderstorm':'img/thunderstorm.jpg',
}


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
    else:
        # Default to Mumbai if no city is provided
        city = 'Nagpur'

    try:
        # Get weather data from OpenWeatherMap API
        API_KEY = "487f4c7891cfac10d2a5edaba36c2131"
        url = 'https://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'units': 'metric', 'appid': API_KEY}
        response = requests.get(url, params=params)
        data = response.json()

        # Extract relevant weather information from API response
        city = data["name"]
        description = data["weather"][0]["main"]
        temperature = data['main']['temp']
        pressure = data["main"]["pressure"]
        humidity = data["main"]["humidity"]
        visibility = data.get("visibility")
        wind_speed = data["wind"]["speed"]
        sunrise = data["sys"]["sunrise"]
        sunset = data["sys"]["sunset"]
        icon =  weather_emojis.get(description.lower(), '')
        background =  weather_images.get(description.lower(), 'img/bg.jpg')
    except Exception as e:
        city = "Not Found"
        description = "none"
        temperature = "none"
        pressure = "none"
        humidity = "none"
        visibility = "none"
        wind_speed = "none"
        sunrise = "none"
        sunset = "none"
        icon =  "none"
        background =  weather_images.get(description.lower(), 'img/bg.jpg')
    # Render template with weather data
    return render_template('index.html', city=city, 
                                        temperature=temperature,
                                        description=description,
                                        wind_speed=wind_speed,
                                        pressure=pressure,
                                        humidity=humidity,
                                        visibility=visibility,
                                        sunrise=sunrise,
                                        sunset=sunset,
                                        icon=icon,
                                        background=background
                                        )

if __name__ == '__main__':
    app.run(debug=True)
