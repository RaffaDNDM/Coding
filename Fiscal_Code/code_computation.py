import requests
from bs4 import BeautifulSoup as bs
from tkinter import messagebox
from datetime import date

MONTHS = {'Gennaio':'A', 'Febbraio':'B', 'Marzo':'C', 'Aprile':'D', 'Maggio':'E', 'Giugno':'H', 'Luglio':'L', 'Agosto':'M', 'Settembre':'P', 'Ottobre':'R', 'Novembre':'S', 'Dicembre':'T'}
ODD_CODES = {'A':1,'B':0,'C':5,'D':7,'E':9,'F':13,'G':15,'H':17,'I':19,'J':21,'K':2,'L':4,'M':18,'N':20, 'O':11,'P':3,'Q':6,'R':8,'S':12,'T':14,'U':16,'V':10,'W':22,'X':25,'Y':24,'Z':23}
FEMALE_OFFSET = 40
VOWELS = ['A','E','I','O','U']

#I take 1,2,3 consonants
def three_letters_last(name):
    count=0
    letters = ''
    upper_name = name.upper().replace(' ', '')

    for char in upper_name:
        if count==3:
            break
        elif char not in VOWELS:
            letters = letters + char
            count = count +1

    for char in upper_name:
        if count==3:
            break
        elif char in VOWELS:
            letters = letters + char
            count = count +1

    while count < 3:
        letters = letters + 'X'
        count = count+1

    return letters


#I take 1,3,4 consonants
def three_letters_first(name):
    count=0
    letters = ''
    num_vowels = 0
    upper_name = name.upper().replace(' ', '')

    for vowel in VOWELS:
        num_vowels = num_vowels + upper_name.count(vowel)

    if (len(upper_name)-num_vowels) >= 4 :
        for char in upper_name:
            if count==4:
                break
            elif char not in VOWELS:
                if count!=1:
                    letters = letters + char
                count = count +1
    else:
        letters = three_letters_last(upper_name)

    return letters


def first_last_name(first_name, last_name):
    print(f'{first_name} {last_name}')
    return three_letters_last(last_name)+three_letters_first(first_name)


def birth(sex, day, month, year):
    print(sex)
    print(f'{day} {month} {year}')

    day_num = int(day)+(sex-1)*FEMALE_OFFSET
    if day_num < 10:
        day = '0'+str(day_num)
    else:
        day = str(day_num)

    return year[-2:]+MONTHS[month]+day


def city_code(city):
    print(city)
    r = requests.get('https://www.comuniecitta.it/cerca-codice-catastale?chiave='+city)
    content = bs(r.text, 'html.parser')
    trs = content.find_all(lambda tag: tag.name=='tr')

    for x in trs:
        if str(city[0]+city.lower()[1:]) in x.text:
            tds = x.find_all(lambda tag: tag.name=='td')
            return tds[2].text
    
    messagebox.showerror('ERRORE', 'Comune non trovato')
    return ''


def parity_check(fiscal_code):
    count = 0
    index = 1

    for char in fiscal_code:
        if index%2==0:
            if char.isalpha():
                count = count + ord(char) - ord('A')
            elif char.isnumeric():
                count = count + ord(char) - ord('0')
        else:
            if char.isalpha():
                count = count+ODD_CODES[char]
            elif char.isnumeric():
                count = count + ODD_CODES[chr(ord(char) - ord('0')+ord('A'))]

        index = index+1


    count = count % 26
    return chr(count+ord('A'))


def compute_code(first_name, last_name, sex, day, month, year, city):
    fiscal_code = ''
    fiscal_code = fiscal_code + first_last_name(first_name, last_name)
    fiscal_code = fiscal_code + birth(sex, day, month, year)
    fiscal_code = fiscal_code + city_code(city)
    
    messagebox.showinfo("Codice Fiscale", fiscal_code+parity_check(fiscal_code))


def read_birth(date_string):
    current_date = date.today().year % 2000
    year = ''

    if int(date_string[:2]) > current_date:
        year = '19'+date_string[:2]
    else:
        year = '20'+date_string[:2]

    day = int(date_string[-2:])

    male = True
    if day > 40:
        day = day-40
        male = False

    return male, str(day) +' '+  list(MONTHS.keys())[list(MONTHS.values()).index(date_string[2].upper())]+' '+year

def read_city_code(city_string):
    r = requests.get('https://www.comuniecitta.it/cerca-codice-catastale?chiave='+city_string)
    content = bs(r.text, 'html.parser')
    trs = content.find_all(lambda tag: tag.name=='tr')

    for x in trs:
        if str(city_string.upper()) in x.text:
            tds = x.find_all(lambda tag: tag.name=='td')
            return tds[0].text
    
    messagebox.showerror('ERRORE', 'Comune non trovato')
    return ''

def read_code(fiscal_code):
    print(fiscal_code)
    male, date = read_birth(fiscal_code[6:11]) 
    city_from_code = read_city_code(fiscal_code[11:15])
    
    sentence = 'Nata il '

    if male:
        sentence='Nato il '

    messagebox.showinfo("Codice Fiscale", sentence+date+' a '+city_from_code)


