import requests
import urllib
from termcolor import cprint, colored

#Proxy site used as a shortner
SHORTNER_SITE = 'http://tinyurl.com/api-create.php'

def tiny_url(url):
    '''
    Shortner of a URL.

    Args:
        url (str): URL to be shorten

    Returns:
        shorten_url (str): Short version of url
    '''

    global SHORTNER_SITE

    try:
        request = SHORTNER_SITE + '?' + urllib.parse.urlencode({'url':url})
        response = requests.get(request)

        cprint('\nOld URL:', 'green', end=' ')
        print(url)
        cprint('New URL:', 'green', end=' ')
        print(response.text)
    
    except Exception:
        print('\nError on request')

def main():
    cprint('\nInsert the URL you want to shorten', 'blue')
    cprint('__________________________________', 'blue')
    url = input()
    tiny_url(url)
    cprint('__________________________________', 'blue', end='\n\n')

if __name__=='__main__':
    main()