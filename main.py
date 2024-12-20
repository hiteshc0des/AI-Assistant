import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary  
import requests
import os
import google.generativeai as genai
from dotenv import load_dotenv

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi_key = "newsapi_key"


def speak(text):
    engine.say(text)
    engine.runAndWait()


def load_api_key():
    try:
        load_dotenv()
        return os.getenv('GEMINI_API_KEY')
    except FileNotFoundError:
        print("Error: API key not found.")
        return None


def get_generative_response(prompt):
    api_key = load_api_key()
    if not api_key:
        return None

    try:
        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(prompt)

        return response.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def process_command(command):

    if "open google" in command.lower():
        webbrowser.open("https://google.com")

    elif "open youtube" in command.lower():
        webbrowser.open("https://youtube.com")

    elif "open linkdin" in command.lower():
        webbrowser.open("https://linkdin.com")

    elif "open facebook" in command.lower():
        webbrowser.open("https://facebook.com")

    elif command.lower().startswith("play"):
        song = command.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in command.lower():
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi_key}")
            r.raise_for_status()
            data = r.json()
            articles = data['articles']

            for article in articles:
                speak(article['title'])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            speak("Sorry, I couldn't fetch the news right now. Please try again later.")
        except KeyError as e:
            print(f"Error parsing news data: {e}")
            speak("There was an error processing the news. Please try again.")

    elif command.lower().startswith("what is"):
        question = command.lower()[len("what is "):]
        answer = get_generative_response(question)
        if answer:
            speak(answer)
        else:
            speak("I don't have an answer for that yet. But I'm always learning!")

    else:
        pass


if __name__ == "__main__":
    speak("Initializing Jarvis...")

    while True:
        try:
          
            with sr.Microphone() as source:
                print("Listening for 'Jarvis'...")
                audio = recognizer.listen(source, timeout=5)

            word = recognizer.recognize_google(audio).lower()
            if word == "jarvis":
                speak("Yes")

                
                with sr.Microphone() as source:
                    print("Jarvis is listening...")
                    audio = recognizer.listen(source)

                command = recognizer.recognize_google(audio).lower()
                process_command(command)

        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            speak("Sorry, I didn't understand that")