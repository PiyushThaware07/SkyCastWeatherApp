# pip install pyTelegramBotAPI
import telebot
import requests
import datetime
import json
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

print("Initializing the Bot...")
Token = "6045523083:AAH3uaBGHbhnbp5mF7LnJQgTsJ0304MT9aA"
bot = telebot.TeleBot(Token)

@bot.message_handler(commands=['start'])
def start(message):
    username = message.from_user.first_name
    bot.send_message(chat_id=message.chat.id, text=f"Hello {username},\nEnter the name of a city to see weather information.With the forecast button you can see forecasts for 5 days. :)try this /weather (cityname)")


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



@bot.message_handler(commands=['weather'])
def weather(message):
    try:
        get_city = message.text.split(' ')[1]
        API_KEY = "487f4c7891cfac10d2a5edaba36c2131"
        fetch = fetch_weather(get_city,API_KEY)
        # Checking Emoji
        emoji = weather_emojis.get(fetch["description"].lower(), '')
        response = f'Welcome to {get_city}, {fetch["celsius_temp"]}°C\nWeather: {fetch["description"]}{emoji}\n📊Pressure: {fetch["pressure"]} hPa\n💧Humidity: {fetch["humidity"]}%\n👁️Visibility: {fetch["visibility"]}\n🎐️Wind : {fetch["wind"]} Km/h\n🌄️Sunrise : {fetch["sunrise"]}\n🌇Subset : {fetch["sunset"]}',
        username = message.from_user.first_name
        print(response,username)

        # Create the inline keyboard and add a button to it
        keyboard = InlineKeyboardMarkup(row_width=1)
        hourly_button = InlineKeyboardButton(text="Show Hourly Forecast", callback_data=f"hourlyForecast_{get_city}")
        weekly_button = InlineKeyboardButton(text="Show Weekly Forecast", callback_data=f"weeklyForecast_{get_city}")
        keyboard.add(hourly_button)
        keyboard.add(weekly_button)

    except Exception as e:
        response = "Enter the city Please..."
        keyboard = None

    bot.send_message(chat_id=message.chat.id, text=response, reply_markup=keyboard)


def fetch_weather(city_name,API_KEY):
    print("Fetching data from API...")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}"
    response = requests.get(url).json()

    description = response["weather"][0]["main"]
    kelvin_temp = response['main']['temp']
    celsius_temp = int(kelvin_temp-273.15)
    pressure = response["main"]["pressure"]
    humidity = response["main"]["humidity"]
    visibility = response.get("visibility")
    wind = response["wind"]["speed"]
    sunrise = response["sys"]["sunrise"]
    sunset = response["sys"]["sunset"]

    return {
        "city_name": city_name,
        "description": description,
        "kelvin_temp": kelvin_temp,
        "celsius_temp": celsius_temp,
        "pressure": pressure,
        "humidity": humidity,
        "visibility": visibility,
        "wind":wind,
        "sunrise":sunrise,
        "sunset":sunset,
    }



# Handle the callback data when the button is pressed
@bot.callback_query_handler(func=lambda call: call.data.startswith('hourlyForecast_'))
def handle_callback(call):
    print("Hourly Forecast")
    # Get the city name from the query parameter
    city_name = call.data.split('_')[1]

    url = "https://api.openweathermap.org/data/2.5/forecast"
    api_key = "487f4c7891cfac10d2a5edaba36c2131"
    # Construct the API request URL
    query_params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(url, params=query_params)
    # Parse the response JSON data
    data = json.loads(response.text)
    # Create a list of hourly forecasts for the next 7 hours
    hourly_forecasts = []
    # Return the hourly forecasts as a string
    for hour in data["list"][:7]:
        hourly_forecasts.append((hour["dt_txt"], hour["main"]["temp"], hour["weather"][0]["description"]))
    print(hourly_forecasts)
    output = ""
    empoji=""
    for item in hourly_forecasts:
        date = item[0][:10]
        time = item[0][11:16]
        temp = item[1]
        desc = item[2]
        # Checking Emoji
        emoji = weather_emojis.get(desc.lower(), '')
        output += f"🔴{date} {time}: \n{emoji}{desc}\n🌡{temp:.2f} °C\n\n"

    bot.send_message(chat_id=call.message.chat.id, text=f"Hourly Weather Update for Next 24hrs\n\n\n{output}")



# Handle the callback data when the button is pressed
@bot.callback_query_handler(func=lambda call: call.data.startswith('weeklyForecast_'))
def handle_callback(call):
    print("Weekly Forecast")
    # Get the city name from the query parameter
    city_name = call.data.split('_')[1]

    url = "https://api.openweathermap.org/data/2.5/forecast"
    api_key = "487f4c7891cfac10d2a5edaba36c2131"
    # Construct the API request URL
    query_params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(url, params=query_params)
    # Parse the response JSON data
    data = json.loads(response.text)
    # Create a list of daily forecasts for the next 5 days
    daily_forecasts = {}
    for item in data["list"]:
        date = item["dt_txt"][:10]
        time = item["dt_txt"][11:16]
        if date not in daily_forecasts:
            daily_forecasts[date] = []
        daily_forecasts[date].append((time, item["main"]["temp"], item["weather"][0]["description"]))

    # Return the daily forecasts as a string
    output = ""
    for date, hourly_forecasts in daily_forecasts.items():
        output += f"🔴{date}:\n"
        for item in hourly_forecasts:
            time = item[0]
            temp = item[1]
            desc = item[2]
            # Checking Emoji
            emoji = weather_emojis.get(desc.lower(), '')
            output += f"{time}: {desc} ({temp:.2f}{emoji} °C)\n"
        output += "\n"

    bot.send_message(chat_id=call.message.chat.id, text=f"Weekly Weather Update for Next 7 Days\n\n{output}")


bot.polling()
