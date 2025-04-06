import speech_recognition as sr
import pyttsx3
import pywhatkit
import os
import webbrowser
import datetime
import sys

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Set to a female voice; change index for different voices

def talk(text):
    """Function to convert text to speech."""
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def take_command():
    """Function to take voice or text input from the user."""
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening... (Say 'stop' or 'exit' to quit)")
        talk("I'm listening")
        
        # Check for typed input first
        typed_command = input("Type your command (or press Enter to use voice): ").lower()
        if typed_command in ['stop', 'exit']:
            return 'stop'
        if typed_command:
            return typed_command
        
        try:
            listener.adjust_for_ambient_noise(source, duration=1)
            print("Recognizing...")
            audio = listener.listen(source, timeout=5, phrase_time_limit=10)
            command = listener.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.WaitTimeoutError:
            print("Listening timed out due to inactivity.")
            return 'stop'
        except sr.UnknownValueError:
            talk("Sorry, I didn't catch that. Could you please repeat?")
            return ""
        except sr.RequestError:
            talk("Speech recognition service is unavailable.")
            return 'stop'

def run_assistant():
    """Function to run the assistant and execute commands."""
    command = take_command()

    if 'stop' in command or 'exit' in command:
        talk("Goodbye!")
        sys.exit()

    elif 'open youtube' in command:
        talk('Opening YouTube')
        webbrowser.open('https://www.youtube.com')

    elif 'open gmail' in command:
        talk('Opening Gmail')
        webbrowser.open('https://mail.google.com')

    elif 'open google' in command:
        talk('Opening Google')
        webbrowser.open('https://www.google.com')

    elif 'open whatsapp' in command:
        talk('Opening WhatsApp')
        webbrowser.open('https://web.whatsapp.com')

    elif 'open vs code' in command or 'open visual studio code' in command:
        talk('Opening Visual Studio Code')
        os.system("code")  # Ensure 'code' is in your system's PATH

    elif 'play' in command:
        song = command.replace('play', '').strip()
        talk(f'Playing {song}')
        pywhatkit.playonyt(song)

    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f'Current time is {current_time}')

    else:
        talk("I'm sorry, I didn't understand that command.")

# Continuous loop to keep the assistant running
while True:
    run_assistant()
