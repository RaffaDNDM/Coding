from termcolor import colored, cprint
import colorama
from PIL import Image

LINE = '___________________________________________________'

class ASCIIArt:
    '''
    ASCII art generator from image.

    Attributes:
        __ASCII_ART (list): List of symbols to be used for different
                            levels of color.
    '''

    __ASCII_ART = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

    def scale(self, img, new_width=100):
        '''
        Scale an img to a new one with the new specified width.

        Args:
            img (Image): Image to be scaled.

            new_width (int): Number of pixels for the new specified width.

        Returns:
            resized_img (numpy.ndarray): Scaled img with width new_width.
        '''

        width, height = img.size
        ratio = height/width
        new_height = int(new_width*ratio)
        return img.resize((new_width, new_height))

    def convert_to_gray(self, img):
        '''
        Conver image to grayscale.

        Args:
            img (Image): Image to be converted.

        Returns:
            converted_img (numpy.ndarray): img converted to grayscale color space.
        '''
        return img.convert('L')

    def pixels_to_ASCII(self, img):
        '''
        Create ASCII text from image values.

        Args:
            img (Image): Image to be elaborated.

        Returns:
            characters (str): ASCII text obtained from img pixels.
        '''

        #Read image pixel values
        pixels = img.getdata()
        #Convert each pixel to an ASCII character
        characters = ''.join(self.__ASCII_ART[pixel//25] for pixel in pixels)

        return characters

    def encode(self, path, new_width=100):
        '''
        Convert an image, at the specified path, to an ASCII text.

        Args:
            path (str): Path of the image to be encoded.

            width (int): Width of the final scaled image, before the
                         ASCII text convertion.
        '''

        img = None

        try:
            #Open the image
            img = Image.open(path)
        except:
            print(colored("The file path",'yellow')+colored(path,'green')+colored("doesn't exist",'yellow'))
            return

        #Convert the image to grayscale space
        img = self.convert_to_gray(self.scale(img, new_width))
        #Convert the image to an ASCII text
        ASCII_img = self.pixels_to_ASCII(img)
        #Add the '\n' at the end of the ASCII text related to each row
        size = len(ASCII_img)
        ASCII_img = '\n'.join([ASCII_img[i*new_width : (i+1)*new_width] for i in range(0, size//new_width)])
        #Print the ASCII image on terminal
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