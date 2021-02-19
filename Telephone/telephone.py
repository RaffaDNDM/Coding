from termcolor import colored, cprint
import csv

LINE = '___________________________________________________'

class TelephoneParser:
    __ZONES_FILENAME = 'prefix_zones.csv'
    __ZONES = {}

    def __init__(self):
        with open(self.__ZONES_FILENAME, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')

            for row in csv_reader:
                if row[0] not in self.__ZONES:
                    self.__ZONES[row[0]] = [(row[1],row[2])]
                else:
                    self.__ZONES[row[0]].append((row[1],row[2]))

    def info(self, phone_num):
        #Invalid number <3 digits or >12 digits
        if len(phone_num) < 3 or len(phone_num)>15:
            print('Prefix not found', end='\n\n')
            return

        if phone_num[:3] == '+39':
            phone_num = phone_num[3:]

        if len(phone_num) < 6:
            print('Prefix not found', end='\n\n')
            return

        prefix = ''

        for i in range(2, 6):
            if phone_num[:i] in self.__ZONES:
                prefix = phone_num[:i]
                break

        if prefix == '':
            print('Prefix not found', end='\n\n')
        else:
            self.print_zones(prefix)

    def print_zones(self, prefix : str):
        for (region, town) in self.__ZONES[prefix]:
            print(colored(region, 'yellow')+f'-> {town}')

        print(' ')

def main():
    global LINE

    print('')
    parser = TelephoneParser()
    
    while True:
        try:
            cprint(f'Insert the phone number (CTRL+C to exit)\n{LINE}', 'blue')
            phone_num = input()
            cprint(LINE, 'blue')
            parser.info(phone_num)
        except KeyboardInterrupt:
            cprint('\nExit from program\n', 'red')
            exit(0)

if __name__=='__main__':
    main()