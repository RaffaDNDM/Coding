from termcolor import colored, cprint
import colorama
from PIL import Image

LINE = '___________________________________________________'

class ASCIIArt:
    __ASCII_ART = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

    def scale(self, img, new_width=100):
        width, height = img.size
        ratio = height/width
        new_height = int(new_width*ratio)
        return img.resize((new_width, new_height))

    def convert_to_gray(self, img):
        return img.convert('L')

    def pixels_to_ASCII(self, img):
        pixels = img.getdata()
        characters = ''.join(self.__ASCII_ART[pixel//25] for pixel in pixels)
        return characters

    def encode(self, path, new_width=100):
        img = None

        try:
            img = Image.open(path)
        except:
            print(colored("The file path",'yellow')+colored(path,'green')+colored("doesn't exist",'yellow'))
            return

        img = self.convert_to_gray(self.scale(img, new_width))
        ASCII_img = self.pixels_to_ASCII(img)
        size = len(ASCII_img)
        ASCII_img = '\n'.join([ASCII_img[i*new_width : (i+1)*new_width] for i in range(0, size//new_width)])

        print(ASCII_img)

def main():
    global LINE

    colorama.init()
    print('')
    a = ASCIIArt()
    
    while True:
        try:
            cprint(f'Insert the path of an image (CTRL+C to exit)\n{LINE}', 'blue')
            text = input()
            cprint(LINE, 'blue')
            a.encode(text)
        except KeyboardInterrupt:
            cprint('\nExit from program\n', 'red')
            exit(0)

if __name__=='__main__':
    main()