import speech_recognition as sr
import pyttsx3
import pywhatkit
import webbrowser
from googletrans import Translator
import requests
from bs4 import BeautifulSoup
import os
import eel
import webbrowser

# Инициализация синтеза речи
engine = pyttsx3.init()
engine.setProperty("rate", 170)
engine.setProperty("voice", "ru")  # Русский язык

# Инициализация переводчика
translator = Translator()

# Функция для синтеза речи
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Функция для распознавания речи
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        eel.DisplayMessage("Я вас слушаю")
        speak("Я вас слушаю")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language="ru-RU")
        eel.DisplayMessage(f"Вы сказали: {text}")
        print(f"Вы сказали: {text}")
        return text.lower()
    except sr.UnknownValueError:
        eel.DisplayMessage("Не удалось распознать речь, повторите, пожалуйста.")
        speak("Не удалось распознать речь, повторите, пожалуйста.")
        return ""
    except sr.RequestError:
        eel.DisplayMessage("Ошибка подключения к сервису распознавания речи.")
        speak("Ошибка подключения к сервису распознавания речи.")
        return ""

# Функция получения прогноза погоды работает
def get_weather(city):
    try:
        api_key = "d2cb8c4d811a17e1829132ac3c5fc166"  # Вставьте свой ключ API OpenWeatherMap
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ru&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != 200:
            eel.DisplayMessage("Не удалось получить данные о погоде. Проверьте название города.")
            speak("Не удалось получить данные о погоде. Проверьте название города.")
            return

        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        eel.DisplayMessage(f"В городе {city} сейчас {weather}, температура {temp} градусов Цельсия.")
        speak(f"В городе {city} сейчас {weather}, температура {temp} градусов Цельсия.")
    except Exception as e:
        eel.DisplayMessage("Произошла ошибка при получении данных о погоде.")
        speak("Произошла ошибка при получении данных о погоде.")
        print(e)

# Функция выполнения поискового запроса работает
def search_web(query):
    webbrowser.open(f"https://ya.ru/search/?text={query}")
    eel.DisplayMessage(f"Вот результаты поиска для {query}")
    speak(f"Вот результаты поиска для {query}")

# Функция поиска видео на YouTube работает
def search_youtube(query):
    try:
        # Создаем ссылку на поисковый запрос
        youtube_search_url = f"https://www.youtube.com/results?search_query={query}"
        # Открываем браузер с результатами поиска
        webbrowser.open(youtube_search_url)
        speak(f"Вот результаты поиска на YouTube для {query}")
    except Exception as e:
        speak("Произошла ошибка при выполнении запроса на YouTube.")
        print(f"Ошибка: {e}")

# Функция перевода работает
def translate_text(text, dest="ru"):
    try:
        translation = translator.translate(text, dest=dest)
        eel.DisplayMessage(f"Перевод: {translation.text}")
        speak(f"Перевод: {translation.text}")
        return translation.text
    except Exception as e:
        eel.DisplayMessage("Произошла ошибка при переводе.")
        speak("Произошла ошибка при переводе.")
        print(e)

# Функция открытия приложений работает
def open_application(app_name):
    try:
        if "блокнот" in app_name:
            eel.DisplayMessage("Открываю Блокнот.")
            os.system("notepad")  # Открытие блокнота через системную команду
            speak("Открываю Блокнот.")
        elif "браузер" in app_name:
            eel.DisplayMessage("Открываю браузер.")
            os.system("start opera")  # Запуск браузера Chrome (или другого браузера)
            speak("Открываю браузер.")
        elif "калькулятор" in app_name:
            eel.DisplayMessage("Открываю Калькулятор.")
            os.system("calc")  # Запуск калькулятора
            speak("Открываю Калькулятор.")
        else:
            eel.DisplayMessage(f"Я пока не знаю, как открыть {app_name}.")
            speak(f"Я пока не знаю, как открыть {app_name}.")
    except Exception as e:
        eel.DisplayMessage("Произошла ошибка при попытке открыть приложение.")
        speak("Произошла ошибка при попытке открыть приложение.")
        print(f"Ошибка: {e}")

# Основная функция
@eel.expose
def main():
    eel.DisplayMessage("Привет! Чем могу помочь?")
    speak("Привет! Чем могу помочь?")
    while True:
        command = recognize_speech()

        if "погода" in command:
            eel.DisplayMessage("Укажите город, для которого вы хотите узнать погоду.")
            speak("Укажите город, для которого вы хотите узнать погоду.")
            city = recognize_speech()
            if city:
                get_weather(city)
        elif "поиск" in command:
            eel.DisplayMessage("Что вы хотите найти?")
            speak("Что вы хотите найти?")
            query = recognize_speech()
            if query:
                search_web(query)
        elif "видео" in command:
            eel.DisplayMessage("Что вы хотите найти на YouTube?")
            speak("Что вы хотите найти на YouTube?")
            query = recognize_speech()
            if query:
                search_youtube(query)
        elif "переведи" in command:
            eel.DisplayMessage("Что вы хотите перевести?")
            speak("Что вы хотите перевести?")
            text_to_translate = recognize_speech()
            if text_to_translate:
                eel.DisplayMessage("На какой язык перевести? Русский или английский?")
                speak("На какой язык перевести? Русский или английский?")
                lang = recognize_speech()
                dest_lang = "ru" if "русский" in lang else "en"
                translate_text(text_to_translate, dest=dest_lang)
        elif "открой" in command:
            eel.DisplayMessage("Какое приложение вы хотите открыть?")
            speak("Какое приложение вы хотите открыть?")
            app_name = recognize_speech()
            if app_name:
                open_application(app_name)
        elif "запиши" in command:
            eel.DisplayMessage("Диктуйте текст, я запишу.")
            speak("Диктуйте текст, я запишу.")
            text = recognize_speech()
            if text:
                with open("запись.txt", "w", encoding="utf-8") as file:
                    file.write(text)
                eel.DisplayMessage("Я записал текст в файл запись.txt.")
                speak("Я записал текст в файл запись.txt.")
        elif "привет" in command:
            eel.DisplayMessage("Здравствуйте!")
            speak("Здравствуйте!")
        elif "пока" in command or "до свидания" in command:
            eel.DisplayMessage("До свидания! Хорошего дня!")
            speak("До свидания! Хорошего дня!")
            eel.ShowHood()
            break
        else:
            eel.DisplayMessage("Извините, я не понял вашу команду.")
            speak("Извините, я не понял вашу команду.")

# Запуск программы
if __name__ == "__main__":
    main()
