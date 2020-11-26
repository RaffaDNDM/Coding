import speech_recognition as sr
from time import ctime, sleep
import time
import os
from gtts import gTTS
import tempfile
from playsound import playsound
from termcolor import cprint
import webbrowser
from urllib.parse import quote
import time

class VoiceAssistant:

    LINE = '__________________________________________________'
    BEST_PLACES = {'casa':'Atri', 'studio':'Padova'}
    DESCRIPTIONS = {'cerca': 'Apre google per una ricerca',
                    'meteo' : 'Apre ilmeteo.it per visionare le previsioni', 
                    'stack' : 'Apre stackoverflow per cercare soluzioni',
                    'terminale' : 'Apre un terminale linux zsh',
                    'wikipedia' : 'Apre wikipedia per svolgere una ricerca',
                    'youtube' : 'Apre youtube per cercare dei video',
                    'no' : 'Esce dal programma'}

    def __init__(self):
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
        check = True
        question = True
        
        while check:
            if question:
                self.speak("Ha bisogno di qualcosa?")
                self.print_menu()

            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                request = self.recognizer.record(source, duration=3)
    
            parsed_request = ''

            try:
                parsed_request = self.recognizer.recognize_google(request, language='it-IT')
                
                print('Richiesta:', end=' ')
                cprint(parsed_request, 'yellow')

                check = self.action(parsed_request.lower())
                question = True

            except sr.UnknownValueError:
                self.speak("Non capisco, ripeta.")
                question = False
                continue
            except sr.RequestError:
                self.speak("Nessuna richiesta rilevata, ripeta.")
                question = False
                continue


    def action(self, request):
        if request in self.ACTIONS.keys():
            self.call_me(request)
        elif request=='no':
            return False
        else:
            self.speak('Comando sconosciuto')

        return True


    def call_me(self, arg): 
        self.ACTIONS[arg].__get__(self, type(self))()


    def print_menu(self):
        cprint('{:^30s}'.format('MENU'), 'blue')
        cprint(f'{self.LINE}', 'blue')
        print('Attiva il microfono e rispondi con una delle seguenti opzioni')
        cprint(f'{self.LINE}', 'blue')
        

        for k in self.DESCRIPTIONS.keys():
            cprint('{:>10s}:'.format(k), 'green', end=' ')
            print(f'{self.DESCRIPTIONS[k]}')

        cprint(f'{self.LINE}', 'blue')


    def search(self):
        cprint('\n{:^50s}'.format('GOOGLE'), 'red')
        cprint(f'{self.LINE}', 'red')
        self.speak('Desidera qualcosa in particolare?')
        check = True

        while check:
            request=''
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                request = self.recognizer.record(source, duration=6)
            
            parsed_request=''
            try:
                parsed_request = self.recognizer.recognize_google(request, language='it-IT')
                cprint(parsed_request, 'red')

                if parsed_request.lower() == 'no':
                    print('Aprendo Google...', end='  ')
                    
                    webbrowser.open('https://www.google.com/')
                    
                    cprint('[Google aperto]', 'green', end='  ')
                
                else:
                    print('Aprendo Google...', end='  ')        
                
                    new = 2 # not really necessary (by default on many browsers)
                    base_url = 'http://www.google.com/?#q='
                    final_url = base_url + quote(parsed_request)
                    webbrowser.open(final_url, new=new)
                
                    cprint('[Google aperto]', 'green', end='  ')
                    print('Oggetto:', end=' ')
                    cprint(parsed_request, 'yellow')

                check = False

            except sr.UnknownValueError:
                self.speak("Non capisco, ripeta.")
                continue
            except sr.RequestError:
                self.speak("Nessuna richiesta rilevata, ripeta.")
                continue

        cprint(f'{self.LINE}', 'red')


    def stackoverflow(self):
        cprint('\n{:^50s}'.format('STACKOVERFLOW'), 'red')
        cprint(f'{self.LINE}', 'red')
        print('Aprendo Stackoverflow...', end='  ')

        webbrowser.open('https://www.stackoverflow.com/')

        cprint('[Stackoverflow aperto]', 'green', end='  ')
        cprint(f'{self.LINE}', 'red')


    def bash(self):
        # Open terminal not related to current python3 (&) program
        # So if the program stops, the terminal won't be closed
        cprint('\n{:^50s}'.format('TERMINALE'), 'red')
        cprint(f'{self.LINE}', 'red')
        print('Aprendo Terminale...', end='  ')

        os.system("x-terminal-emulator -e /bin/zsh &")

        cprint('[Terminale aperto]', 'green', end='  ')
        cprint(f'{self.LINE}', 'red')


    def weather(self):
        cprint('\n{:^50s}'.format('METEO'), 'red')
        cprint(f'{self.LINE}', 'red')
        self.speak('In quale città?')

        check = True

        while check:
            request=''
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                request = self.recognizer.record(source, duration=3)
            
            parsed_request=''
            try:
                parsed_request = self.recognizer.recognize_google(request, language='it-IT')
                print('Aprendo Meteo...')

                if parsed_request.lower() in self.BEST_PLACES.keys():
                    webbrowser.open('https://www.ilmeteo.it/meteo/'+
                                    self.BEST_PLACES[parsed_request])
                
                else:
                    webbrowser.open('https://www.ilmeteo.it/meteo/'+
                                    parsed_request[0].upper()+
                                    parsed_request[1:].lower())

                cprint('[Meteo aperto]', 'green', end='  ')
                print('Città:', end=' ')
                cprint(parsed_request, 'yellow')

                check = False

            except sr.UnknownValueError:
                self.speak("Non capisco, ripeta.")
                continue
            except sr.RequestError:
                self.speak("Nessuna richiesta rilevata, ripeta.")
                continue

        cprint(f'{self.LINE}', 'red')


    def wikipedia(self):
        cprint('\n{:^50s}'.format('WIKIPEDIA'), 'red')
        cprint(f'{self.LINE}', 'red')
        self.speak('Desidera qualcosa in particolare?')

        check = True

        while check:
            request=''

            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                request = self.recognizer.record(source, duration=6)
            
            try:
                parsed_request = self.recognizer.recognize_google(request, language='it-IT')

                if parsed_request.lower() == 'no':
                    print('Aprendo Wikipedia...')
                    
                    webbrowser.open('https://www.wikipedia.org/')
                    
                    cprint('[Wikipedia aperta]', 'green', end='  ')
                    print('Oggetto:', end=' ')
                    cprint('Nessuno', 'yellow')
                
                else:
                    print('Aprendo Wikipedia...')
                    
                    new = 2 # not really necessary (by default on many browsers)
                    base_url = 'https://www.wikipedia.org/wiki/'
                    final_url = base_url + quote(parsed_request)
                    webbrowser.open(final_url, new=new)
                    
                    cprint('[Wikipedia aperta]', 'green', end='  ')
                    print('Oggetto:', end=' ')
                    cprint(parsed_request, 'yellow')

                check = False
        
            except sr.UnknownValueError:
                self.speak("Non capisco, ripeta.")
                continue
            except sr.RequestError:
                self.speak("Nessuna richiesta rilevata, ripeta.")
                continue

        cprint(f'{self.LINE}', 'red')


    def youtube(self):
        cprint('\n{:^50s}'.format('YOUTUBE'), 'red')
        cprint(f'{self.LINE}', 'red')
        self.speak('Desidera qualcosa in particolare?')
        
        check = True

        while check:
            request=''
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                request = self.recognizer.record(source, duration=6)
            
            parsed_request=''
            try:
                parsed_request = self.recognizer.recognize_google(request, language='it-IT')
                cprint(parsed_request, 'red')

                if parsed_request.lower() == 'no':
                    print('Aprendo Youtube...')
                    webbrowser.open('https://www.youtube.com/')
                    cprint('[Youtube aperto]', 'green', end='  ')
                    print('Oggetto:', end=' ')
                    cprint('Nessuno', 'yellow')

                else:
                    print('Aprendo Youtube...')
                    new = 2 # not really necessary (by default on many browsers)
                    base_url = 'https://www.youtube.com/results?search_query='
                    final_url = base_url + quote(parsed_request)
                    webbrowser.open(final_url, new=new)

                    cprint('[Youtube aperto]', 'green', end='  ')
                    print('Oggetto:', end=' ')
                    cprint(parsed_request, 'yellow')

                check = False

            except sr.UnknownValueError:
                self.speak("Non capisco, ripeta.")
                continue
            except sr.RequestError:
                self.speak("Nessuna richiesta rilevata, ripeta.")
                continue

        cprint(f'{self.LINE}', 'red')


    ACTIONS = { 'cerca': search,
                'meteo' : weather, 
                'stack' : stackoverflow,
                'terminale' : bash,
                'wikipedia' : wikipedia,
                'youtube' : youtube}


def part_of_day():
    localtime = time.localtime(time.time())
    my_hour = localtime.tm_hour*60+localtime.tm_min 
    am_6 = 360
    noon = am_6*2
    pm_6 = am_6*3
    midnight = am_6*4

    if my_hour < am_6:
        return 'Salve'
    elif my_hour < noon:
        return 'Buongiorno'
    elif my_hour < pm_6:
        return 'Buon pomeriggio'
    else:
        return 'Buonasera'



def main():
    # Creation of Voice Assistant
    assist = VoiceAssistant()
    # Greeting to user, based on hour of the day
    assist.speak(part_of_day()+', signore!!!')
    # Voice assistant listens to user speech and
    assist.listen() 
    # performs different actions
    assist.speak('Arrivederci, signore!!!')
    # Voice assistant says good bye to user

if __name__=='__main__':
    main()