from termcolor import cprint, colored
import colorama

class WrongFormatCard (Exception):
    pass

class CreditCard:
    '''
    Define a Credit card

    Args:
        card_num (str): Number of the credit card

    Attributes:
        TYPE (str): Type of credit card (circuit)

        CARD_NUM (str): Number of the credit card

        VALID (bool): True if the number of the credit card respects
                      the Luhn algorithm 
                      (the right-most digit was computed with Luhn algorithm)
    '''

    def __init__(self, card_num : str):
        #Remove ' ' and '-' characters in the card number
        card_num = card_num.replace(' ', '')
        card_num = card_num.replace('-', '')

        if not card_num.isdigit() or len(card_num) < 13:
            raise WrongFormatCard()

        self.TYPE = ''
        self.CARD_NUM = card_num
        self.type_card()
        self.VALID = self.luhn_algorithm()

    def type_card(self):
        '''
        Evaluate the type of credit card from its number
        '''

        if self.CARD_NUM[0] == '4' and \
           (len(self.CARD_NUM) == 13 or len(self.CARD_NUM) == 16):
                self.TYPE = 'Visa'

        elif self.CARD_NUM[0] == '5' and \
             len(self.CARD_NUM) == 16:
                self.TYPE = 'Mastercard'

        elif self.CARD_NUM[0] == '6' and \
             len(self.CARD_NUM) == 16:
                self.TYPE = 'Discover'

        elif (self.CARD_NUM[:2] == '34' or self.CARD_NUM[:2] == '37') and \
             len(self.CARD_NUM) == 15:
                self.TYPE = 'American Express'

        elif (self.CARD_NUM[:2] == '30' or self.CARD_NUM[:2] == '36' or self.CARD_NUM[:2] == '38') and \
             len(self.CARD_NUM) == 15:
                self.TYPE = 'Diners Club and Carte Blanche'

        else:
            raise WrongFormatCard()

    def luhn_algorithm(self):
        '''
        Check if the last digit of the number of the credit card
        was computed with the Luhn algorithm as it should be

        Returns:
            valid (bool): True if the number of the credit card
                          respects the Luhn algorithm
        '''
        
        sum_double = 0

        for x in self.CARD_NUM[len(self.CARD_NUM)-2::-2]:
            #Double the value
            value = int(x)*2

            #Sum the digits
            for d in str(value):
                sum_double += int(d)

        sum_other = 0

        for x in self.CARD_NUM[len(self.CARD_NUM)-3::-2]:
            sum_other += int(x)

        #Sum previous results and multiply for 9
        final_sum = (sum_double + sum_other) * 9
        
        #Valid card if previous result Mod 10 is equal to the last
        #digit of the credit card number
        return (final_sum % 10) == int(self.CARD_NUM[-1])

    def info(self):
        '''
        Print info about the specified number of credit card
        '''

        cprint('Card type:', 'green', end=' ')
        print(self.TYPE)
        cprint('Valid:', 'yellow', end=' ')
        print(self.VALID)

def main():
    colorama.init()
    credit_card = None
    check = True

    while True:
        try:
            cprint('Insert the number of the credit card (CTRL+C to exit)', 'blue')
            card_num = input()
            cprint('___________________________________________________', 'blue')
            credit_card = CreditCard(card_num)
            credit_card.info()
            cprint('___________________________________________________\n', 'blue')
        except WrongFormatCard:
            cprint('Wrong format of the credit card number', 'red')
            cprint('___________________________________________________\n', 'blue')
        except KeyboardInterrupt:
            break

if __name__=='__main__':
    main()