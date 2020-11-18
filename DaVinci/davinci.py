from PIL import Image, ImageDraw, ImageFont
from sys import stdin
import argparse
from termcolor import cprint
import os

POSITION_TEXT = (50, 20)
OUTPUT_FILE = 'output.txt'
PARCHMENT_IMG = 'dat/parchment.jpg'
STYLES_FOLDER = 'dat/styles/'

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


def generate_script(text, max_length, input_path, filename, output_path, style):
    '''
    Generate Da Vinci's mirror script
    '''

    global POSITION_TEXT, PARCHMENT_IMG, STYLES_FOLDER, STYLES

    print('Generating script...')
    img = Image.open(PARCHMENT_IMG)
    img2 = img.copy()

    string_text = '\n'
    for x in text:
        string_text = string_text + x + '\n'

    fnt = ImageFont.truetype(STYLES_FOLDER+STYLES[style], 40)
    d = ImageDraw.Draw(img2)
    d.text(POSITION_TEXT, string_text, font=fnt, fill=(0, 0, 0))
    
    img2 = img2.transpose(Image.FLIP_LEFT_RIGHT)
    img2.save(output_path+filename.replace('.txt', '.png'))
    print('Completed creation of script', 'red', end='\n\n')


def list_lines(f):
    '''
    Return list composed by lines in stream specified by f
    '''

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
    '''
    Get input in interactive mode or from a file
    '''    

    #List of lines
    text = []
    #Max size of a line
    max_length = 0

    #If specified input file
    if input_file:

        print('Opening', end=' ')
        cprint('{input_file}', end=' ')
        print('text file to read its content', end='\n\n')

        #Save each line of input_file, removing final '\n' character
        with open(input_file) as f: 
            text, max_length = list_lines(f)

    else:

        try:
            cprint('Write the input text', 'red', end=' ')
            print('(', end='')
            cprint('CTRL+D', 'green', end=' ')
            print('to stop insertion and generate script)')
            cprint('_________________________________________________________________', 'red')

            #Save each line of std_in, removing final '\n' character
            text, max_length = list_lines(stdin)
            cprint('_________________________________________________________________', 'red', end='\n\n')

        except KeyboardInterrupt:
            cprint('\n[Keyboard Interrupt]', 'blue', end=' ')
            print('The user blocks the input using', end=' ')
            cprint('CTRL+C', 'green', end='\n')
            print('[the text will be neglected, use EOF = CTRL+D]', end='\n\n')
            exit(0)

    return text, max_length


def select_style():
    '''
    Select style from style files in styles folder
    '''
    
    global STYLES_FOLDER, STYLES
    check = True
    STYLES  = os.listdir(STYLES_FOLDER)
    STYLES.sort()
    files_no_extension = [x[:-4] for x in STYLES]

    while check:
        try:
            cprint('\nSelect which style you want by inserting the corresponding number', 'red')
            cprint('_________________________________________________________________', 'red')
            count=0
            for f in files_no_extension:
                cprint(f'{count})', 'yellow', end=' ')         
                print(f)
                count = count + 1
            
            cprint('_________________________________________________________________', 'red')
            num = int(input())
            
            if num>=0 and num < len(files_no_extension):
                check = False

        except ValueError:
            cprint('[VALUE ERROR]', 'blue', end=' ')
            print('you must enter an integer')
        except KeyboardInterrupt:
            exit(0)

    print('')
    return num


def args_parser():
    '''
    Parser of command line arguments
    '''

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
    #Select style
    style = select_style()
    #Take input
    text, max_length = get_input(input_path)
    generate_script(text, max_length, input_path, filename, output_path, style)

    print(text)


if __name__=='__main__':
    main()