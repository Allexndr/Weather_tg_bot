import telebot
import requests

bot_token = '6157704275:AAEkB5xTV6iUr6i5Weh0meWgXb6r-njHTnY'  # Замените YOUR_BOT_TOKEN на токен вашего бота

bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я бот погоды. Введите название города, чтобы узнать погоду.")

@bot.message_handler(commands=['weather'])
def get_weather(message):
    city = message.text[9:].strip()  # Получаем название города из сообщения после команды /weather и удаляем лишние пробелы
    if city:
        api_key = "28a2a1dd7d224c5c313950096ce1dd39"  # Замените YOUR_API_KEY на свой ключ API OpenWeatherMap
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        response = requests.get(url)
        data = response.json()
        print(data)  # Выводим ответ API OpenWeatherMap в консоль для дальнейшего анализа
        if data["cod"] == "404":
            bot.reply_to(message, "Город не найден.")
        else:
            try:
                weather = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                humidity = data["main"]["humidity"]

                result = f"Погода в {city}:\n\n{weather}\nТемпература: {round(temperature-273)}°C\nВлажность: {humidity}%"
                bot.reply_to(message, result)
            except KeyError:
                bot.reply_to(message, "Ошибка получения данных о погоде. Пожалуйста, попробуйте позже.")
    else:
        bot.reply_to(message, "Пожалуйста, введите название города.")

bot.polling()
