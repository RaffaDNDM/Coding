from PIL import Image, ImageDraw, ImageFont
from sys import stdin
import argparse
from termcolor import cprint
import os

A4_SIZE = (3508, 2480)
POSITION_TEXT = (100, 100)
OUTPUT_FILE = 'output.txt'

def uniform_dir_path(directory):
    '''
    Return directory path with '/' at the end

    Args:
        directory (str): directory path that you want to uniform

    Returns:
        directory (str): modified directory path that ends with '/'

    '''
    if directory == '':
        return directory

    if directory.endswith('/') or directory.endswith('\\'):
        return directory
    else:
        return directory+'/'


def generate_script(text, max_length, input_path, filename, output_path):
    global A4_SIZE, POSITION_TEXT

    img = Image.new('RGB', A4_SIZE, color = (255, 255, 255))
    
    string_text = '\n'
    for x in text:
        string_text = string_text + x + '\n'

    fnt = ImageFont.truetype('Allura-Regular.otf', 150)
    d = ImageDraw.Draw(img)
    d.text(POSITION_TEXT, string_text, font=fnt, fill=(0, 0, 0))
    
    img = img.transpose(Image.FLIP_LEFT_RIGHT)

    if filename:
        img.save(output_path+filename.replace('.txt', '.png'))


def list_lines(f):
    #List of lines
    text = []
    #Max size of a line
    max_length = 0

    #Save each line, removing final '\n' character
    for line in f:
        updated_line = line.replace('\n', '')
        text.append(updated_line)
        #Max size of a line
        if max_length < len(updated_line):
            max_length = len(updated_line)

    return text, max_length


def get_input(input_file):
    #List of lines
    text = []
    #Max size of a line
    max_length = 0

    #If specified input file
    if input_file:

        #Save each line, removing final '\n' character
        with open(input_file) as f: 
            text, max_length = list_lines(f)

    else:

        try:
            text, max_length = list_lines(stdin)
        except KeyboardInterrupt:
            cprint('\n[Keyboard Interrupt]', 'blue', end=' ')
            print('The user blocks the input using', end=' ')
            cprint('CTRL+C', 'green', end='\n')
            print('[the text will be neglected, use EOF = CTRL+D]', end='\n\n')
            exit(0)

    return text, max_length


'''
Parser of command line arguments
'''
def args_parser():
    global OUTPUT_FILE

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-input", "-i",
                        dest="input", 
                        help="Path of the '.txt' file to be encrypted by Da Vinci")

    parser.add_argument("-output", "-o",
                        dest="output", 
                        help="""Path of the output folder where there will 
                                be the result encrypted image""")

    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    if args.input and (not os.path.isfile(args.input) or not args.input.endswith('.txt')):
        cprint('\n[Not existing FILE]', 'blue', end=' ')
        print('The path', end=' ')
        cprint(f'{args.input}', 'green', end=' ')
        print('is not a file', end='\n\n')
        parser.print_help()
        print('\n')
        exit(0)

    if args.input:
        filename = os.path.basename(args.input)
        output_path = uniform_dir_path(args.input[:-len(filename)])
    else:
        filename = OUTPUT_FILE
        output_path = ''

    #Check if output folder is specified
    if args.output:
        if not os.path.isdir(args.output):
            cprint('\n[Not existing FOLDER]', 'blue', end=' ')
            print('The path', end=' ')
            cprint(f'{args.output}', 'green', end=' ')
            print('is not a directory', end='\n\n')
            parser.print_help()
            print('\n')
            exit(0)
        else:
            output_path = uniform_dir_path(args.output)

    return args.input, output_path, filename


def main():
    #Parser of command line arguments
    input_path, output_path, filename = args_parser()    
    #Take input
    text, max_length = get_input(input_path)
    generate_script(text, max_length, input_path, filename, output_path)

    print(text)


if __name__=='__main__':
    main()