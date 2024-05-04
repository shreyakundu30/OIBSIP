import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again please...")
        return "None"
    return query

def assistant():
    speak("Hello! I am your voice assistant. How can I help you today?")
    while True:
        query = listen().lower()
        if 'hello' in query:
            speak("Hello! How can I assist you?")
        elif 'time' in query:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {time}")
        elif 'date' in query:
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            speak(f"Today's date is {date}")
        elif 'search' in query:
            speak("What do you want to search for?")
            search_query = listen().lower()
            url = f"https://www.google.com/search?q={search_query}"
            webbrowser.open(url)
        elif 'exit' in query:
            speak("Goodbye!")
            break

if __name__ == "__main__":
    assistant()
