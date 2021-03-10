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
    '''
    Voice assistant implementation.

    Parameters:
        LINE (str): Special line

        BEST_PLACES (dict): Alias for most important places for 
                            weather predictions

        DESCRIPTIONS (dict): Vocal commands that the Voice 
                             Assistant can support

        ACTIONS (dict): Functions related to vocal commands 

        recognizer (speech_recognition.Recognizer): Voice recognizer

    '''
    
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
        '''
        Convert a string to an audio file and play it.

        Args:
            audio_string (str): String to be converted into an
                                audio file
        '''

        tts = gTTS(text=audio_string, lang='it')
        temp_file = tempfile.gettempdir()+'/temp.mp3'
        tts.save(temp_file)
        playsound(temp_file)
        #music = pyglet.media.load(temp_file, streaming=False)
        #music.play()
        #sleep(music.duration)
        os.remove(temp_file)


    def listen(self):
        '''
        Listen to the user's speech and parse it.
        '''

        check = True
        question = True
        
        while check:
            if question:
                self.speak("Ha bisogno di qualcosa?")
                self.print_menu()

            #Record user's speech
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                request = self.recognizer.record(source, duration=3)
    
            parsed_request = ''

            try:
                #Parser of the user's speech
                parsed_request = self.recognizer.recognize_google(request, language='it-IT')
                
                print('Richiesta:', end=' ')
                cprint(parsed_request, 'yellow')

                #Select the action related to the user's speech
                check = self.action(parsed_request.lower())
                question = True

            except sr.UnknownValueError:
                #The Voice Assistant doesn't understand the user's speech
                self.speak("Non capisco, ripeta.")
                question = False
                continue

            except sr.RequestError:
                #The Voice Assistant doesn't listen anything
                self.speak("Nessuna richiesta rilevata, ripeta.")
                question = False
                continue


    def action(self, request):
        if request in self.ACTIONS.keys():
            #The vocal command exists
            self.call_me(request)

        elif request=='no':
            #Exit from program
            return False
        else:
            #Unknown vocal command
            self.speak('Comando sconosciuto')

        return True


    def call_me(self, arg):
        '''
        Call the function related to the parsed vocal command
        '''
        self.ACTIONS[arg].__get__(self, type(self))()


    def print_menu(self):
        '''
        Print the menu of Jarvis displaying all the possible options.
        '''

        cprint('{:^30s}'.format('MENU'), 'blue')
        cprint(f'{self.LINE}', 'blue')
        print('Attiva il microfono e rispondi con una delle seguenti opzioni')
        cprint(f'{self.LINE}', 'blue')
        

        for k in self.DESCRIPTIONS.keys():
            cprint('{:>10s}:'.format(k), 'green', end=' ')
            print(f'{self.DESCRIPTIONS[k]}')

        cprint(f'{self.LINE}', 'blue')


    def search(self):
        '''
        Google search.
        '''

        cprint('\n{:^50s}'.format('GOOGLE'), 'red')
        cprint(f'{self.LINE}', 'red')
        self.speak('Desidera qualcosa in particolare?')
        check = True

        while check:
            #Listen the user's speech to search it on Google
            request=''
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                request = self.recognizer.record(source, duration=6)
            
            parsed_request=''
            try:
                #Parser of the user's speech
                parsed_request = self.recognizer.recognize_google(request, language='it-IT')
                cprint(parsed_request, 'red')

                #If the user tells 'no', Voice Assistant opens Google home page 
                if parsed_request.lower() == 'no':
                    print('Aprendo Google...', end='  ')
                    
                    webbrowser.open('https://www.google.com/')
                    
                    cprint('[Google aperto]', 'green', end='  ')
                
                else:
                    #Voice Assistant searches parsed_request on Google
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
                #The Voice Assistant doesn't understand the user's speech
                self.speak("Non capisco, ripeta.")
                continue

            except sr.RequestError:
                #The Voice Assistant doesn't listen anything
                self.speak("Nessuna richiesta rilevata, ripeta.")
                continue

        cprint(f'{self.LINE}', 'red')


    def stackoverflow(self):
        '''
        Stackoverflow search.
        '''
        
        #Open Stackoverflow search bar.
        cprint('\n{:^50s}'.format('STACKOVERFLOW'), 'red')
        cprint(f'{self.LINE}', 'red')
        print('Aprendo Stackoverflow...', end='  ')

        webbrowser.open('https://www.stackoverflow.com/')

        cprint('[Stackoverflow aperto]', 'green', end='  ')
        cprint(f'{self.LINE}', 'red')


    def bash(self):
        '''
        Start bash.
        '''
        
        # Open terminal not related to current python3 (&) program
        # So if the program stops, the terminal won't be closed
        cprint('\n{:^50s}'.format('TERMINALE'), 'red')
        cprint(f'{self.LINE}', 'red')
        print('Aprendo Terminale...', end='  ')

        os.system("x-terminal-emulator -e /bin/zsh &")

        cprint('[Terminale aperto]', 'green', end='  ')
        cprint(f'{self.LINE}', 'red')


    def weather(self):
        '''
        Weather prediction search.
        '''

        cprint('\n{:^50s}'.format('METEO'), 'red')
        cprint(f'{self.LINE}', 'red')
        self.speak('In quale città?')

        check = True

        while check:
            #Listen to the user's speech
            request=''
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                request = self.recognizer.record(source, duration=3)
            
            parsed_request=''
            try:
                #Parse the user's speech
                parsed_request = self.recognizer.recognize_google(request, language='it-IT')
                print('Aprendo Meteo...')

                #Search the weather predictions
                if parsed_request.lower() in self.BEST_PLACES.keys():
                    #Search the weather predictions for the specified alias
                    webbrowser.open('https://www.ilmeteo.it/meteo/'+
                                    self.BEST_PLACES[parsed_request])
                
                else:
                    #Search the weather predictions for the specified town
                    webbrowser.open('https://www.ilmeteo.it/meteo/'+
                                    parsed_request[0].upper()+
                                    parsed_request[1:].lower())

                cprint('[Meteo aperto]', 'green', end='  ')
                print('Città:', end=' ')
                cprint(parsed_request, 'yellow')

                check = False

            except sr.UnknownValueError:
                #The Voice Assistant doesn't understand the user's speech
                self.speak("Non capisco, ripeta.")
                continue

            except sr.RequestError:
                #The Voice Assistant doesn't listen anything
                self.speak("Nessuna richiesta rilevata, ripeta.")
                continue

        cprint(f'{self.LINE}', 'red')


    def wikipedia(self):
        '''
        Wikipedia search.
        '''
        
        cprint('\n{:^50s}'.format('WIKIPEDIA'), 'red')
        cprint(f'{self.LINE}', 'red')
        self.speak('Desidera qualcosa in particolare?')

        check = True

        while check:
            #Listen to the user's speech
            request=''
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                request = self.recognizer.record(source, duration=6)
            
            try:
                #Parse the user's speech
                parsed_request = self.recognizer.recognize_google(request, language='it-IT')

                if parsed_request.lower() == 'no':
                    #If the user tells 'no', Voice Assistants opens 
                    #Wikipedia search home page 
                    print('Aprendo Wikipedia...')
                    
                    webbrowser.open('https://www.wikipedia.org/')
                    
                    cprint('[Wikipedia aperta]', 'green', end='  ')
                    print('Oggetto:', end=' ')
                    cprint('Nessuno', 'yellow')
                
                else:
                    #Voice Assistant searches parsed_request on Wikipedia
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
                #The Voice Assistant doesn't understand the user's speech
                self.speak("Non capisco, ripeta.")
                continue

            except sr.RequestError:
                #The Voice Assistant doesn't listen anything
                self.speak("Nessuna richiesta rilevata, ripeta.")
                continue

        cprint(f'{self.LINE}', 'red')


    def youtube(self):
        '''
        Youtube video search.
        '''

        cprint('\n{:^50s}'.format('YOUTUBE'), 'red')
        cprint(f'{self.LINE}', 'red')
        self.speak('Desidera qualcosa in particolare?')
        
        check = True

        while check:
            #Listen to the user's speech
            request=''
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source)
                request = self.recognizer.record(source, duration=6)
            
            parsed_request=''
            try:
                #Parse the user's speech
                parsed_request = self.recognizer.recognize_google(request, language='it-IT')
                cprint(parsed_request, 'red')

                if parsed_request.lower() == 'no':
                    #If the user tells 'no', Voice Assistants opens 
                    #Youtube home page 
                    print('Aprendo Youtube...')
                    webbrowser.open('https://www.youtube.com/')
                    cprint('[Youtube aperto]', 'green', end='  ')
                    print('Oggetto:', end=' ')
                    cprint('Nessuno', 'yellow')

                else:
                    #Voice Assistant searches parsed_request on Youtube
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
                #The Voice Assistant doesn't understand the user's speech
                self.speak("Non capisco, ripeta.")
                continue

            except sr.RequestError:
                #The Voice Assistant doesn't listen anything
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
    '''
    Define the greeting of Voice Assistant
    looking at the time of the day
    
    Returns:
        greeting (str): Greeting based on the time of the day 
                        when Voice Assistant is executed
    '''
    #Now
    localtime = time.localtime(time.time())
    my_hour = localtime.tm_hour*60+localtime.tm_min 
    #6:00 am
    am_6 = 360
    #Noon hour
    noon = am_6*2
    #6:00 pm
    pm_6 = am_6*3
    #Midnight hour
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