import os
import argparse
from termcolor import cprint

class WrongFile(Exception):
    '''
        Exception raised when the format of the file, specified by the 
        user is wrong
    '''
    pass

class TextReverse:
    def __init__(self, input_file, single):
        self._TEXT = ""

        if input_file is None:
            try:
                cprint("Write the text to be specified:", 'green')
                cprint("____________________________________________",'green')
                
                while(True):
                    self._TEXT += (input("")+"\n")
            
            except KeyboardInterrupt:
                cprint("____________________________________________",'green')
                pass
        else:
            if os.path.isfile(input_file) and os.path.exists(input_file):
                with open(input_file) as f:
                    self._TEXT = f.read()
            else:
                raise WrongFile()

        self._SINGLE = single

    def reverse(self):
        if self._SINGLE:
            self.reverse_single_words()
        else:
            self.reverse_all()

    def reverse_all(self):
        print(self._TEXT[::-1])
        print("", end='\n\n')

    def reverse_single_words(self):
        lines = self._TEXT.split("\n")

        for line in lines:
            reversed_words = [word[::-1] for word in line.split(" ")]

            if (len(reversed_words)>0):
                print(reversed_words[0], end='')

            for word in reversed_words[1:]:
                print(f" {word}", end='')
            
            print("", end='\n')

        print("", end='\n')


def args_parser():
    '''
    Parser of command line arguments
    '''
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-single","-s",
                        dest="single", 
                        help="""If specified, the program reverses each word
                                of the instead of reversing the whole text.""",
                        action='store_true')

    parser.add_argument("-file","-f",
                        dest="input_file", 
                        help="""If specified, the program reverses the text
                                inside the file specified""")

    #Parse command line arguments
    args = parser.parse_args()

    return args.input_file, args.single

def main():
    #Read command line arguments
    input_file, single = args_parser()
    
    try:
        text = TextReverse(input_file, single)
        text.reverse()
    except WrongFile:
        pass

if __name__=="__main__":
    main()