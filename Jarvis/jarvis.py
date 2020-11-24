import speech_recognition as sr
from time import ctime, sleep
import time
import os
from gtts import gTTS
import tempfile
from playsound import playsound
from termcolor import cprint
import webbrowser

class VoiceAssistant:
    def __init__(self, language):
        self.recognizer = sr.Recognizer()


    def speak(self, audio_string):
        tts = gTTS(text=audio_string, lang='it')
        temp_file = tempfile.gettempdir()+'/temp.mp3'
        tts.save(temp_file)
        playsound(temp_file)
        #music = pyglet.media.load(temp_file, streaming=False)
        #music.play()
        #sleep(music.duration)
        os.remove(temp_file)


    def listen(self):
        while True:
            self.speak("Hai bisogno di qualcosa?")
            print('RECORDING')

            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                request = self.recognizer.record(source, duration=3)
    
                parsed_request = ''

                try:
                    parsed_request = self.recognizer.recognize_google(request, language='it-IT')
                    cprint(parsed_request, 'red')

                except sr.UnknownValueError:
                    self.speak("Non capisco")
                except sr.RequestError:
                    self.speak("Nessuna richiesta")

                self.action(parsed_request.lower())


    def wikipedia(self):
        self.speak('Cosa vuoi cercare?')

        request=''
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            request = self.recognizer.record(source, duration=3)
        
        parsed_request=''
        try:
            parsed_request = self.recognizer.recognize_google(request, language='it-IT')
            cprint(parsed_request, 'red')

        except sr.UnknownValueError:
            self.speak("Non capisco")
        except sr.RequestError:
            self.speak("Nessuna richiesta")

        webbrowser.open('https://www.wikipedia.org/wiki/'+
                         parsed_request[0].upper()+
                        parsed_request[1:].lower())
    

    def meteo(self):
        self.speak('In quale città?')

        request=''
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            request = self.recognizer.record(source, duration=3)
        
        parsed_request=''
        try:
            parsed_request = self.recognizer.recognize_google(request, language='it-IT')
            cprint(parsed_request, 'red')

        except sr.UnknownValueError:
            self.speak("Non capisco")
        except sr.RequestError:
            self.speak("Nessuna richiesta")

        webbrowser.open('https://www.ilmeteo.it/meteo/'+
                         parsed_request[0].upper()+
                        parsed_request[1:].lower())


    def action(self, request):
        if request=='terminale':
            os.system("x-terminal-emulator -e /bin/zsh")
        elif request=='meteo':
            self.meteo()
        elif request=='stack':
            webbrowser.open('https://www.stackoverflow.com/')
        elif request=='youtube':
            webbrowser.open('https://www.youtube.com/')
        elif request=='cerca':
            webbrowser.open('https://www.google.com')
        elif request=='wikipedia':
            self.wikipedia()
        elif request=='no':
            exit(0)
        else:
            self.speak('Comando sconosciuto')


while True:
    assist = VoiceAssistant('it')
    assist.speak('Buongiorno, signore!!!')
    assist.listen()