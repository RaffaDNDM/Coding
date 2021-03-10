from termcolor import colored, cprint
import csv
import colorama

LINE = '___________________________________________________'

class Braille:
    '''
    Braille encoder.

    Attributes:
        __UNICODE_FILE (str): Path of the unicode file with association
                              between Braille and ASCII characters

        __NUM_PREFIX (str): Prefix label to put before a Braille digit

        __UPPER_CASE (str): Prefix label to put before a Braille character
                            to obtain its upper case

        __UNICODE_DICT (dict): Dictionary with association between ASCII
                               characters and unicode Braille characters
    '''

    __UNICODE_FILE = 'codes.csv'
    __NUM_PREFIX = 'SPECIAL_NUM'
    __UPPER_CASE = 'UPPER_CASE'

    __UNICODE_DICT = {}

    def __init__(self):
        with open(self.__UNICODE_FILE, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f, delimiter=' ')

            for row in csv_reader:
                self.__UNICODE_DICT[row[0]] = row[1]

    def encode(self, text):
        '''
        Encode an ASCII text with Braille symbols.

        Args:
            text (str): message to be encoded
        '''

        if len(text) == 0:
            cprint('Invalid text', 'red', end='\n\n')
            return
        else:
            self.braille_encode(text)

    def braille_encode(self, text):
        '''
        Encode an ASCII text with Braille symbols.

        Args:
            text (str): message to be encoded
        '''

        encoded_txt = ''
        
        for c in text:
            if c != ' ':
                #Prefixes for digits and upper case characters
                if c.isdigit():
                    #Digit (add digit prefix)
                    encoded_txt += self.__UNICODE_DICT[self.__NUM_PREFIX]
                    encoded_txt += ' '
                elif c.isupper():
                    #Upper case character (add upper case prefix)
                    encoded_txt += self.__UNICODE_DICT[self.__UPPER_CASE]
                    encoded_txt += ' '
                
                #Encode character
                c = c.lower()

                if c in self.__UNICODE_DICT:
                    #Existing character encoding
                    encoded_txt += self.__UNICODE_DICT[c]
                else:
                    print(colored('Invalid symbol', 'red') + colored(c, 'green'), end='\n\n')
                    return
            else:
                #If character = SPACE, write it as it is
                encoded_txt += c

            #Add SPACE for better readability
            encoded_txt += ' '

        cprint(encoded_txt, 'yellow', end='\n\n')

def main():
    global LINE

    colorama.init()
    print('')
    b = Braille()
    
    while True:
        try:
            cprint(f'Insert the code (CTRL+C to exit)\n{LINE}', 'blue')
            text = input()
            cprint(LINE, 'blue')
            b.encode(text)
        except KeyboardInterrupt:
            cprint('\nExit from program\n', 'red')
            exit(0)

if __name__=='__main__':
    main()