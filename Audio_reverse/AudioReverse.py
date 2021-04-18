from termcolor import cprint
import colorama
import pyaudio
import argparse
import os
import scipy.io.wavfile as wave
import numpy as np

def uniform_dir_path(directory):
    """
    Return directory path with '/' at the end
    Args:
        directory (str): directory path that you want to uniform
    Returns:
        directory (str): modified directory path that ends with '/'
    """

    if directory.endswith('/') or directory.endswith('\\'):
        return directory
    else:
        return directory+'/'

class WrongFile(Exception):
    '''
        Exception raised when the format of the file, specified by the 
        user is wrong
    '''
    pass

class AudioReverse:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    _SIGNAL = []

    def __init__(self, input_file, output_path="."):        
        if input_file is None:
            self._OUTPUT_FILE=uniform_dir_path(output_path)+"recording.wav"
            self.record_audio()
        else:
            if os.path.isfile(input_file) and input_file.endswith(".wav"):
                self._INPUT_FILE = input_file
                self._OUTPUT_FILE=uniform_dir_path(output_path)+"reverse_"+os.path.basename(self._INPUT_FILE)
                self.read_audio()
            else:
                raise WrongFile()
        
    def record_audio(self):
        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        
        cprint('\n*** Recording ***', 'green', attrs=['bold'])

        #Recording        
        frames = []

        try:
            while True:
                data = stream.read(self.CHUNK)
                frames.append(data)
                
        except KeyboardInterrupt:
            pass

        stream.stop_stream()
        stream.close()
        p.terminate()

        audio_string = b''.join(frames)
        temp_signal = []

        for i in range(0, len(audio_string), 4):
            temp_signal.append(np.frombuffer(audio_string[i:i+4], dtype=np.int16, count=2))
        
        self._SIGNAL = np.array(temp_signal)
        
    def read_audio(self):
        self.RATE, self._SIGNAL = wave.read(self._INPUT_FILE)

    def reverse(self):
        wave.write(self._OUTPUT_FILE, self.RATE, self._SIGNAL[::-1].astype(np.int16))

def args_parser():
    '''
    Parser of command line arguments
    '''
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-f", "-file",
                        dest="input_file", 
                        help="""If specified, it is the path of the input file to be reversed.
                                Otherwise, the program records an audio file using the device microphone.""")

    parser.add_argument("-out", "-o",
                        dest="output_path", 
                        help="""Path of the output file, without filename.""")

    #Parse command line arguments
    args = parser.parse_args()

    return args.input_file, args.output_path

def main():
    #Colored print
    colorama.init()
    #Read command line arguments
    input_file, output_path = args_parser()

    try:
        audio = None

        if output_path is None:
            audio = AudioReverse(input_file)
        else:
            audio = AudioReverse(input_file, output_path)
    
        audio.reverse()
        
    except WrongFile:
        pass


if __name__=="__main__":
    main()