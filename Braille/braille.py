from termcolor import colored, cprint
import csv


LINE = '___________________________________________________'

class Braille:
    __UNICODE_FILE = 'codes.csv'
    __NUM_PREFIX = 'SPECIAL_NUM'
    __UPPER_CASE = 'UPPER_CASE'

    __UNICODE_DICT = {}
    __IMG_CODE_DICT = {}

    def __init__(self):
        with open(self.__UNICODE_FILE, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f, delimiter=' ')

            for row in csv_reader:
                self.__UNICODE_DICT[row[0]] = row[1]

    def encode(self, text):
        if len(text) == 0:
            cprint('Invalid text', 'red', end='\n\n')
            return
        else:
            self.braille_encode(text)

    def braille_encode(self, text):
        encoded_txt = ''
        
        for c in text:
            if c != ' ':
                if c.isdigit():
                    encoded_txt += self.__UNICODE_DICT[self.__NUM_PREFIX]
                    encoded_txt += ' '
                elif c.isupper():
                    encoded_txt += self.__UNICODE_DICT[self.__UPPER_CASE]
                    encoded_txt += ' '
                
                c = c.lower()

                if c in self.__UNICODE_DICT:
                    encoded_txt += self.__UNICODE_DICT[c]
                else:
                    print(colored('Invalid symbol', 'red') + colored(c, 'green'), end='\n\n')
                    return
            else:
                encoded_txt += c

            encoded_txt += ' '

        cprint(encoded_txt, 'yellow', end='\n\n')

def main():
    global LINE

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