from termcolor import colored, cprint
import csv
import cv2 as cv
import numpy as np
import utility

class POSTNET:
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

        with open(dat_folder+self.__CODES_FILE, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')

            for row in csv_reader:
                self.__CODES[row[0]] = row[1]

    def encode(self, code):
        code = code.replace('-','')
        code = code.replace(' ','')
        
        if len(code) != 9 or not code.isnumeric():
            print('Invalid number', end='\n\n')
            return
        else:
            code = self.create_barcode(code)
            cprint('Completed encoding:', 'yellow', end=' ')
            print(code[:-1]+colored(code[-1], 'green'), end='\n\n')

    def create_barcode(self, code):
        
        #Parity check digit
        
        img = np.zeros((self.__TOTAL_HEIGHT, self.__TOTAL_WIDTH, 3), np.uint8)
        
        for i in range(0,len(img)):
            for j in range(0, len(img[0])):
                img[i][j]=(255,255,255)

        start_width =(self.__QUIET_ZONE_SIZE*self.__UNIT_SIZE)
        start_width = self.draw_code(img, self.__CODES[self.__FIRST_LAST], start_width)
        
        sum = 0
        for c in code:
            sum += int(c)
            start_width = self.draw_code(img, self.__CODES[c], start_width)
        
        #Draw parity digit
        parity = str(10-(sum%10))
        start_width = self.draw_code(img, self.__CODES[parity], start_width)
        code += parity

        start_width = self.draw_code(img, self.__CODES[self.__FIRST_LAST], start_width)

        cv.imshow('img', img)
        cv.waitKey(0)
        cv.destroyAllWindows()
        cv.imwrite('../POSTNET.png', img)

        return code

    def draw_code(self, img, code, start_width):
        for x in code:
            if x == '1':
                cv.line(img, 
                        (start_width, self.__QUIET_ZONE_SIZE*self.__UNIT_SIZE),
                        (start_width, (self.__QUIET_ZONE_SIZE+self.__LINE_SIZE)*self.__UNIT_SIZE), 
                        (0,0,0), 
                        self.__UNIT_SIZE*self.__WIDTH_SYMBOL)
            elif x == '0':
                cv.line(img, 
                        (start_width, (self.__QUIET_ZONE_SIZE+int(self.__LINE_SIZE/2))*self.__UNIT_SIZE),
                        (start_width, (self.__QUIET_ZONE_SIZE+self.__LINE_SIZE)*self.__UNIT_SIZE), 
                        (0,0,0), 
                        self.__UNIT_SIZE*self.__WIDTH_SYMBOL)
                
            start_width += ((self.__WIDTH_SPACE+self.__WIDTH_SYMBOL)*self.__UNIT_SIZE)

        return start_width