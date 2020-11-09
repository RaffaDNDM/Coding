import requests
from bs4 import BeautifulSoup as bs
from tkinter import messagebox
from datetime import date
from parameters import *

def three_letters_last(name):
    """Computation of letters from last name"""

    count=0
    letters = ''
    #Remove spaces
    upper_name = name.upper().replace(' ', '')
    
    #Take first 3 consonants
    for char in upper_name:
        if count==3:
            break
        elif char not in VOWELS:
            letters = letters + char
            count = count +1

    #If not already selected 3 letters, append vowels
    for char in upper_name:
        if count==3:
            break
        elif char in VOWELS:
            letters = letters + char
            count = count +1

    #If name shorter than 2 characters, append 'X'
    while count < 3:
        letters = letters + 'X'
        count = count+1

    return letters


def three_letters_first(name):
    """Computation of letters from first name"""    

    count=0
    letters = ''
    num_vowels = 0
    upper_name = name.upper().replace(' ', '')

    #Number of vowels in name
    for vowel in VOWELS:
        num_vowels = num_vowels + upper_name.count(vowel)

    #If name composed by 4 or more consonants
    #Take first, third and fourth consonants 
    if (len(upper_name)-num_vowels) >= 4 :
        for char in upper_name:
            if count==4:
                break
            elif char not in VOWELS:
                if count!=1:
                    letters = letters + char
                count = count +1
    #Otherwise take letters as in last name
    else:
        letters = three_letters_last(upper_name)

    return letters


def first_last_name(first_name, last_name):
    """Computation of fiscal code first part"""

    print(f'{first_name} {last_name}')
    return three_letters_last(last_name)+three_letters_first(first_name)


def birth(sex, day, month, year):
    """Computation of fiscal code second part"""

    print(f'{SEX_STRINGS[sex]}     {day} {month} {year}')

    #Day definition 
    #male --> day     female ---> day + 40
    day_num = int(day)+(sex-1)*FEMALE_OFFSET

    if day_num < 10:
        #Padding of day string 
        day = '0'+str(day_num)
    else:
        day = str(day_num)

    return year[-2:]+MONTHS[month]+day


def city_code(city):
    """Evaluation of cadastral code of specificied city"""

    print(city)
    #Request the cadastral code of city  
    r = requests.get('https://www.comuniecitta.it/cerca-codice-catastale?chiave='+city)
    content = bs(r.text, 'html.parser')
    #Obtain all table rows
    trs = content.find_all(lambda tag: tag.name=='tr')

    for x in trs:
        #Analyse table row with specified city name
        if str(city[0]+city.lower()[1:]) in x.text:
            tds = x.find_all(lambda tag: tag.name=='td')
            return tds[2].text

    #No city name found
    messagebox.showerror('ERRORE', 'Comune non trovato')
    return ''


def parity_check(fiscal_code):
    """Computation of last character of fiscal code"""
    
    count = 0
    index = 1

    #Mapping of each letter to a number
    #and sum all the numbers obtained
    for char in fiscal_code:
        #If even position
        if index%2==0:
            #Alpha char -> position in alphabet [0, 25]
            if char.isalpha():
                count = count + ord(char) - ord('A')
            #Number char -> number
            elif char.isnumeric():
                count = count + ord(char) - ord('0')

        #If odd position
        else:
            #Alpha char -> ODD_CODES[Alpha char]
            if char.isalpha():
                count = count+ODD_CODES[char]
            #Number char -> position in ODD_CODES[['A',... ,'L']]
            elif char.isnumeric():
                count = count + ODD_CODES[chr(ord(char) - ord('0') + ord('A'))]

        index = index+1

    #Mapping to one of the 26 alphabetic characters
    count = count % 26
    return chr(count+ord('A'))


def compute_code(first_name, last_name, sex, day, month, year, city):
    """Compute fiscal code from user information"""

    fiscal_code = ''
    #Computation of 6 letters based on first and last names
    fiscal_code = fiscal_code + first_last_name(first_name, last_name)
    #Computation of 5 letters based on sex and birthday
    fiscal_code = fiscal_code + birth(sex, day, month, year)
    #Computation of cadastral code from city name    
    cadastral_code = city_code(city)

    #No city name found    
    if cadastral_code!='':
        fiscal_code = fiscal_code + cadastral_code
        messagebox.showinfo("Codice Fiscale", fiscal_code+parity_check(fiscal_code))


def read_birth(date_string):
    """Evaluate sex, day, month and year from date substring"""

    #Current year
    current_date = date.today().year % 2000
    year = ''

    #1900 or 2000
    if int(date_string[:2]) > current_date:
        year = '19'+date_string[:2]
    else:
        year = '20'+date_string[:2]

    #Day obtained from date string
    day = int(date_string[-2:])

    #Sex evaluating the value of the day
    male = True
    if day > 40:
        day = day-40
        male = False

    return male, str(day) +' '+  list(MONTHS.keys())[list(MONTHS.values()).index(date_string[2].upper())]+' '+year


def read_city_code(city_code):
    """Search of city, related to city code, on the web"""

    #Request the city name  
    r = requests.get('https://www.comuniecitta.it/cerca-codice-catastale?chiave='+city_code)
    content = bs(r.text, 'html.parser')
    #Obtain all table rows
    trs = content.find_all(lambda tag: tag.name=='tr')

    for x in trs:
        #Analyse table row with specified cadastral code
        if str(city_code.upper()) in x.text:
            tds = x.find_all(lambda tag: tag.name=='td')
            return tds[0].text
    
    #No cadastral code found
    messagebox.showerror('ERRORE', 'Comune non trovato')
    return ''


def read_code(fiscal_code):
    """Analysis of sex, birthday and city from fiscal code"""

    print(fiscal_code)
    #Evaluation of sex and bithday
    male, date = read_birth(fiscal_code[6:11]) 
    #Evaluation of city name from cadastral code
    city_from_code = read_city_code(fiscal_code[11:15])
    
    if city_from_code!='':
        #Sentence based on sex
        sentence = 'Nata il '
        if male:
            sentence='Nato il '

        #Window with information obtained
        messagebox.showinfo("Codice Fiscale", sentence+date+' a '+city_from_code)