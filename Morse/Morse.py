import pyaudio
import numpy as np
from termcolor import cprint, colored
from scipy.io import wavfile

LINE = '____________________________________________________'

class Morse:
    '''
    Morse encoder/decoder implementation.

    Args:
        volume (float): Volume level

        fs (int): Sampling rate

        freq (float): Frequence of the audio symbol

    Attributes:
        VOLUMES (dict): Dictionary of volume level for each symbol

        FS (int): Sampling rate

        F (float): Frequency of each symbol wave

        DURATIONS (dict): Dictionary of time durations for every symbols

        CODES (dict): Dictionary of symbols for every characters
    '''

    DURATIONS = {'-' : 0.6, '.' : 0.2, '|' : 1.0, ' ' : 2.0}
    CODES = { 'A' : '.-',
              'B' : '-...', 
              'C' : '-.-.',
              'D' : '-..',
              'E' : '.',
              'F' : '..-.', 
              'G' : '--.',
              'H' : '....', 
              'I' : '..',
              'J' : '.---', 
              'K' : '-.-',
              'L' : '.-..', 
              'M' : '--',
              'N' : '-.',
              'O' : '---', 
              'P' : '.--.',
              'Q' : '--.-',
              'R' : '.-.',
              'S' : '...',
              'T' : '-',
              'U' : '..-',
              'V' : '...-',
              'W' : '.--',
              'X' : '-..-',
              'Y' : '-.--',
              'Z' : '--..',
              '0' : '-----', 
              '1' : '.----', 
              '2' : '..---', 
              '3' : '...--', 
              '4' : '....-', 
              '5' : '.....', 
              '6' : '-....', 
              '7' : '--...', 
              '8' : '---..', 
              '9' : '----.',
              "'" : '.----.',
              '"' : '.-..-.',
              '.' : '.-.-.-',
              ',' : '--..--',
              ';' : '-.-.-.',
              ':' : '---...',
              '?' : '..--..',
              '-' : '-....-',
              '/' : '-..-.',
              '(' : '-.--.',
              ')' : '-.--.-',
              '+' : '.-.-.',
              '=' : '-...-',
              '$' : '...-..-',
              '@' : '.--.-.',
              '_' : '..--.-'}


    def __init__(self, volume=0.5, fs = 44100, freq = 440.0):
        self.VOLUMES = {'-' : volume, '.' : volume, '|' : 0.0, ' ' : 0.0}     # range [0.0, 1.0]
        self.FS = fs       # sampling rate, Hz, must be integer
        self.F = freq        # sine frequency, Hz, may be float


    def audio_encode(self, msg):
        '''
        Create the morse audio file from the input message

        Args:
            msg (str): message to be encrypted
        '''

        #Encode the message as a string
        cprint('MESSAGE: ', 'green', end='')
        print(f'{msg}')
        
        msg = self.encode(msg)

        cprint('ENCODED: ', 'red', end='')
        print(f'{msg}')

        #Define the audio sygnal for first symbol
        signal = (np.sin(2*np.pi*np.arange(self.FS*self.DURATIONS[msg[0]])*self.F/self.FS)).astype(np.float32)
        signal = self.VOLUMES[msg[0]]*signal

        #Define the audio sygnals for other symbols in the encoded strings
        for c in msg[1:]:
            sample_mute = np.zeros(int(0.1*self.FS)).astype(np.float32)
            sample = (np.sin(2*np.pi*np.arange(self.FS*self.DURATIONS[c])*self.F/self.FS)).astype(np.float32)
            signal = np.concatenate((signal, sample_mute))
            signal = np.concatenate((signal, self.VOLUMES[c]*sample))

        #Define the audio signal for the last mute symbol            
        sample_mute = np.zeros(int(0.2*self.FS)).astype(np.float32)
        signal = np.concatenate((signal, sample_mute))

        #Store the audio obtained
        wavfile.write('tmp.wav', self.FS, signal)

    def encode(self, msg):
        '''
            Encode the input message as a string using Morse code.
            
            Args:
                msg (str): message to be encrypted

            Returns:
                encoded_msg (str): encrypted Morse message

        '''

        if len(msg)>=1:
            #Upper case the message
            msg = msg.upper()
            encoded_msg = ''

            #Encode every character of the input message
            for c in msg:
                encoded_char = self.encode_character(c)

                if encoded_char == ' ':
                    encoded_msg = encoded_msg[:-1] + encoded_char
                else:
                    encoded_msg += (encoded_char + '|')

            if encoded_msg.endswith('|'):
                encoded_msg = encoded_msg[:-1]

            return encoded_msg

        else:
            raise ValueError


    def encode_character(self, character):
        '''
        Encode a character with Morse encoding

        Args:
            character (chr): Character to be encrypted

        Returns:
            encoded_char (str): Morse code related to character

        '''

        if character == ' ':
            return character
        elif character in list(self.CODES.keys()):
            return self.CODES[character]
        else:
            raise ValueError


def main():
    morse = Morse()
    cprint(f'\n   Insert alphabetic string to be Morse encrypted   \n{LINE}', 'blue')
    msg = input()
    cprint(LINE, 'blue')
    morse.audio_encode(msg)
    cprint(LINE, 'blue', end='\n\n')


if __name__=='__main__':
    main()