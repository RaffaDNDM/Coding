import speech_recognition as sr
from time import ctime, sleep
import time
import os
from gtts import gTTS
import tempfile
import pyglet

def speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    temp_file = tempfile.gettempdir()+'/temp.mp3'
    tts.save(temp_file)
    music = pyglet.media.load(temp_file, streaming=False)
    music.play()
    sleep(music.duration)
    os.remove(temp_file)

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone as source:
        print("What do you need?")
    
        not_confirmed = True

        while not_confirmed:
            request = recognizer.listen(source)

            parsed_request = ''
            try:
                parsed_request = recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                speak("I can't understand")
            except sr.RequestError:
                speak("No request ")

            try:

                if check.upper() == 'YES' or check.upper() == 'NO':
                    check.upper() == 'YES'
                else:
                    speak('Please answer yes or no')

            except sr.UnknownValueError:
                speak("I can't understand")
            except sr.RequestError:
                speak("No request ")


speak('Good morning Sir')