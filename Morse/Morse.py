import pyaudio
import numpy as np
from termcolor import cprint, colored
from scipy.io import wavfile

LINE = '____________________________________________________'

class Morse:

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
              'Z' : '--..' }


    def __init__(self, volume=0.5, fs = 44100, freq = 440.0):
        self.VOLUMES = {'-' : volume, '.' : volume, '|' : 0.0, ' ' : 0.0}     # range [0.0, 1.0]
        self.FS = fs       # sampling rate, Hz, must be integer
        self.F = freq        # sine frequency, Hz, may be float


    def audio_encode(self, msg):
        cprint('MESSAGE: ', 'green', end='')
        print(f'{msg}')
        
        msg = self.encode(msg)

        cprint('ENCODED: ', 'red', end='')
        print(f'{msg}')

        signal = (np.sin(2*np.pi*np.arange(self.FS*self.DURATIONS[msg[0]])*self.F/self.FS)).astype(np.float32)        
        signal = self.VOLUMES[msg[0]]*signal

        for c in msg[1:]:
            sample_mute = np.zeros(int(0.1*self.FS)).astype(np.float32)
            sample = (np.sin(2*np.pi*np.arange(self.FS*self.DURATIONS[c])*self.F/self.FS)).astype(np.float32)
            signal = np.concatenate((signal, sample_mute))
            signal = np.concatenate((signal, self.VOLUMES[c]*sample))
            
        sample_mute = np.zeros(int(0.2*self.FS)).astype(np.float32)
        signal = np.concatenate((signal, sample_mute))
        wavfile.write('tmp.wav', self.FS, signal)


    def encode(self, msg):
        if len(msg)>=1:
            msg = msg.upper()
            encoded_msg = self.encode_character(msg[0])

            if len(msg)>1:
                for c in msg[1:]:
                    encoded_char = self.encode_character(c)

                    if encoded_char == ' ':
                        encoded_msg += encoded_char
                    else:
                        encoded_msg += ('|' + encoded_char)
            
            return encoded_msg

        else:
            raise ValueError


    def encode_character(self, character):
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