from termcolor import cprint, colored
from EAN13 import EAN13
from POSTNET import POSTNET
import colorama

LINE = '___________________________________________________'

def main():
    global LINE
    
    colorama.init()
    print('')
    encoder = None
    option = -1

    while True:
        try:
            cprint(f'Select the type of barcode you want to generate\n{LINE}', 'blue')
            print(colored('0) ','yellow')+'EAN13')
            print(colored('1) ','yellow')+'POSTNET')
            cprint(LINE, 'blue')
            option = int(input())

            if option == 0:
                encoder = EAN13()
                cprint(LINE, 'blue', end='\n\n')
                break

            elif option == 1:
                encoder = POSTNET()
                cprint(LINE, 'blue', end='\n\n')
                break

        except ValueError:
            pass
        
        print('', end='\n\n')

    while True:
        try:
            cprint(f'Insert the code (CTRL+C to exit)\n{LINE}', 'blue')
            code = input()
            cprint(LINE, 'blue')
            encoder.encode(code)
        except KeyboardInterrupt:
            cprint('\nExit from program\n', 'red')
            exit(0)

if __name__=='__main__':
    main()