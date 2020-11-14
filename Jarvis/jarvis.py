import speech_recognition as sr
from time import ctime, sleep
import time
import os
from gtts import gTTS
import tempfile
import pyglet

class VoiceAssistant:
    def __init__(self, language):
        self.recognizer = sr.Recognizer()


    def speak(self, audio_string):
        tts = gTTS(text=audio_string, lang='en')
        temp_file = tempfile.gettempdir()+'/temp.mp3'
        tts.save(temp_file)
        music = pyglet.media.load(temp_file, streaming=False)
        music.play()
        sleep(music.duration)
        os.remove(temp_file)


    def listen(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=5)

            while True:
                self.speak("Do you need something?")
                request = self.recognizer.listen(source)
                parsed_request = ''

                confirmed = False
                try:
                    parsed_request = self.recognizer.recognize_google(request)
                    check = False

                    while not check:
                        check_string = self.recognizer.listen(source)
                        parsed_check = self.recognizer.recognize_google(check_string)
                        self.speak('Do you confirm your request?')

                        if parsed_check == 'yes':
                            check = True
                            confirmed = True
                        elif parsed_check == 'no':
                            check = True
                            confirmed = False
                        else:
                            self.speak('Please answer yes or no')

                except sr.UnknownValueError:
                    self.speak("I can't understand")
                except sr.RequestError:
                    self.speak("No request ")

                if confirmed:
                    self.action(parsed_request)


    def action(self, request):
        if request=='t':
            os.system("x-terminal-emulator -e /bin/zsh")



while True:
    assist = VoiceAssistant('en')
    assist.speak('Good morning Sir')
    assist.listen()