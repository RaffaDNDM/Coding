from termcolor import colored, cprint
import pandas_datareader as pdr
import mplfinance as mplf
import datetime
import csv
import matplotlib.pyplot as plt 

LINE = '___________________________________________________'

class Cryptocurrency:
    '''
    Display cost of cryptocurrencies over time.

    Attributes:
        __CRYPTO_FILE (str): Path of the file containing the name of the
                             most known cryptocurrencies with their codes

        __CRYPTO_CODES (dict): Dictionary of cryptocurrencies and their codes

        CURRENCY (str): Currency code (EUR=euros, USD=US dollars)
    '''
   
    __CRYPTO_FILE = 'crypto_list.csv'
    __CRYPTO_CODES = {}
    CURRENCY = 'EUR'

    def __init__(self):
        with open(self.__CRYPTO_FILE, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')

            for row in csv_reader:
                self.__CRYPTO_CODES[row[0]] = row[1]

    def select_crypto(self):
        '''
        Select a specific type of cryptocurrency.
        '''
        
        global LINE

        option = -1
        
        while option<0 or option>=len(self.__CRYPTO_CODES):
            try:
                cprint(f'Select the type of cryptocurrency\n{LINE}', 'blue')

                i=0
                for k in self.__CRYPTO_CODES:
                    print(colored(f'{i}) ', 'yellow')+k)
                    i+=1

                cprint(LINE, 'blue')

                option = int(input())

            except ValueError:
                pass
        
        return option

    def plot_crypto(self):
        '''
        Plot the values of a cryptocurrency over time.
        '''

        option = self.select_crypto()
        crypto = list(self.__CRYPTO_CODES.values())[option]
        
        #From 1st January 2020 until now
        start = datetime.datetime(2020,1,1)
        end = datetime.datetime.now()

        #Plot value of Bitcoin over years
        data = pdr.DataReader(f'{crypto}-{self.CURRENCY}', 'yahoo', start, end)
        mplf.plot(data, type='candle', volume=True, style='yahoo')

    def compare_cryptos(self):
        '''
        Plot the values of 2 cryptocurrencies over time.
        '''

        option1 = self.select_crypto()
        option2 = option1
        
        while option1==option2:
            option2 = self.select_crypto()

        crypto1 = list(self.__CRYPTO_CODES.values())[option1]
        crypto2 = list(self.__CRYPTO_CODES.values())[option2]   

        #From 1st January 2020 until now
        start = datetime.datetime(2020,1,1)
        end = datetime.datetime.now()  

        #Plot value of Bitcoin over years
        data1 = pdr.DataReader(f'{crypto1}-{self.CURRENCY}', 'yahoo', start, end)
        data2 = pdr.DataReader(f'{crypto2}-{self.CURRENCY}', 'yahoo', start, end)
        
        plt.yscale('log')
        plt.plot(data1['Close'], label=list(self.__CRYPTO_CODES.keys())[option1])
        plt.plot(data2['Close'], label=list(self.__CRYPTO_CODES.keys())[option2])
        plt.legend(loc='upper left')
        plt.show()
        
def select_option():
    '''
    Select the type of plot you want:
    0) to plot a single cryptocurrency
    1) to plot the comparison of 2 cryptocurrencies
    '''
    
    global LINE
    option = -1
    
    while option<0 or option>=2:
        try:
            cprint(f'Select the type of plot\n{LINE}', 'blue')
            print(colored('0) ', 'yellow')+'Plot a cryptocurrency')
            print(colored('1) ', 'yellow')+'Compare two cryptocurrency values')
            cprint(LINE, 'blue')
            
            option = int(input())

        except ValueError:
            pass
    
    return option

def main():
    cc = Cryptocurrency()
    option = select_option()
    
    if option==0:
        cc.plot_crypto()
    elif option==1:
        cc.compare_cryptos()

if __name__=='__main__':
    main()