import emojis
emojified = emojis.encode("There is a :flex: in my boot !")
print(emojified)

from emoji_list import EMOJI_LIST
from termcolor import cprint

for k in EMOJI_LIST:
    cprint(k, color='red')
    
    count=0
    for emoji in EMOJI_LIST[k]:
        shortcut=emoji.replace(':','')

        if(count==3):
            print(emojis.encode(f'{shortcut:25} {emoji:1}'))
            count=0
        else:
            print(emojis.encode(f'{shortcut:25} {emoji:1}'), end=' | ')
            count+=1