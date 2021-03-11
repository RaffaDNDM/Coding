from termcolor import colored, cprint
import csv
import cv2 as cv
import numpy as np
import utility

class POSTNET:
    '''
    POSTNET barcode implement.

    Args:
        dat_folder (str): Path of the folder containing the csv files
                          needed to generate POSTNET barcode

    Attributes:
        __CODES_FILE (str): Name of the csv file containing the POSTNET
                            encoding for the digits of the Barcode
        
        __FIRST_LAST (str): Label used to identify the first and last special
                            symbol of the POSTNET

        __UNIT_SIZE (int): Size of a unit in term of pixels
        
        __WIDTH_SYMBOL (int): Width of a black bar in term of number of units
        
        __WIDTH_SPACE (int): Width of space between 2 bars in term of number 
                             of units
        
        __LINE_SIZE (int): Length of the long bar in term of number of units
        
        __QUIET_ZONE_SIZE (int): Quite zone size in term of number of units
        
        __TOTAL_WIDTH (int): Total width of the POSTNET Barcode image in term
                             of pixels
        
        __TOTAL_HEIGHT (int): Total height of the POSTNET Barcode image in term
                              of pixels

        __CODES (dict): Encoding of each digit with a POSTNET symbol, that is
                        a binary sequence where:
                        1 -> Long bar
                        0 -> Half-length bar 

    '''
    
    __CODES_FILE = 'codes.csv'
    __FIRST_LAST = 'LIMIT'

    __UNIT_SIZE = 2
    __WIDTH_SYMBOL = 2
    __WIDTH_SPACE = 2
    __LINE_SIZE = 20
    __QUIET_ZONE_SIZE = 20
    __TOTAL_WIDTH = (2*__QUIET_ZONE_SIZE+52*__WIDTH_SYMBOL+51*__WIDTH_SPACE)*__UNIT_SIZE
    __TOTAL_HEIGHT = (2*__QUIET_ZONE_SIZE+__LINE_SIZE)*__UNIT_SIZE

    __CODES = {}

    def __init__(self, dat_folder='../dat/POSTNET/'):
        dat_folder = utility.uniform_dir_path(dat_folder)

        #Create the dictionary of encoding for each digit
        with open(dat_folder+self.__CODES_FILE, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')

            for row in csv_reader:
                self.__CODES[row[0]] = row[1]

    def encode(self, code):
        '''
        Encode the code into a POSTNET barcode.

        Args:
            code (str): Code of 9 digits, escluding ' ' and '-'.
        '''
        
        #Remove the ' ' or '-' symbols in the code specified
        code = code.replace('-','')
        code = code.replace(' ','')
        
        if len(code) != 9 or not code.isnumeric():
            print('Invalid number', end='\n\n')
            return
        else:
            #Encode the POSTNET barcode
            code = self.create_barcode(code)
            cprint('Completed encoding:', 'yellow', end=' ')
            print(code[:-1]+colored(code[-1], 'green'), end='\n\n')

    def create_barcode(self, code):
        '''
        Create the POSTNET barcode from the code.

        Args:
            code (str): Code of 9 digits without parity digit.

        Returns:
            code (str): Code encoded with also parity digit computed.
        '''
        #Create the image for the POSTNET barcode
        img = np.zeros((self.__TOTAL_HEIGHT, self.__TOTAL_WIDTH, 3), np.uint8)

        #Instantiate all the pixels as white
        for i in range(0,len(img)):
            for j in range(0, len(img[0])):
                img[i][j]=(255,255,255)

        #Initial position on width for the barcode
        start_width =(self.__QUIET_ZONE_SIZE*self.__UNIT_SIZE)
        #Draw bars of the first special symbol
        start_width = self.draw_code(img, self.__CODES[self.__FIRST_LAST], start_width)
        
        sum = 0
        for c in code:
            sum += int(c)
            #Draw bars of a code digit
            start_width = self.draw_code(img, self.__CODES[c], start_width)
        
        #Compute parity digit
        parity = str(10-(sum%10))
        #Draw bars of the parity check digit
        start_width = self.draw_code(img, self.__CODES[parity], start_width)
        code += parity
        #Draw bars of the last special symbol
        start_width = self.draw_code(img, self.__CODES[self.__FIRST_LAST], start_width)

        #Show POSTNET barcode on a window
        cv.imshow('img', img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        cv.imwrite('../POSTNET.png', img)

        return code

    def draw_code(self, img, code, start_width):
        '''
        Draw the bars from the code of a symbol.

        Args:
            img (np.ndarray): Img in which the symbol will be drawn.

            code (str): Binary code of symbol to be drawn.

            start_width (int): Width position in pixels where the bars, 
                               related to code, will be drawn.

        Returns:
            start_width (int): Width position in pixels where the next 
                               symbol will start to be drawn.
        '''

        #Analyse the binary digit of the code
        for x in code:
            if x == '1':
                #If digit is 1, draw long bar
                cv.line(img, 
                        (start_width, self.__QUIET_ZONE_SIZE*self.__UNIT_SIZE),
                        (start_width, (self.__QUIET_ZONE_SIZE+self.__LINE_SIZE)*self.__UNIT_SIZE), 
                        (0,0,0), 
                        self.__UNIT_SIZE*self.__WIDTH_SYMBOL)
            elif x == '0':
                #If digit is 1, draw long bar
                cv.line(img, 
                        (start_width, (self.__QUIET_ZONE_SIZE+int(self.__LINE_SIZE/2))*self.__UNIT_SIZE),
                        (start_width, (self.__QUIET_ZONE_SIZE+self.__LINE_SIZE)*self.__UNIT_SIZE), 
                        (0,0,0), 
                        self.__UNIT_SIZE*self.__WIDTH_SYMBOL)
                
            #Update width to draw the next symbol
            start_width += ((self.__WIDTH_SPACE+self.__WIDTH_SYMBOL)*self.__UNIT_SIZE)

        return start_width