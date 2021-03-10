import fpdf
import argparse
import os
from PIL import Image
from termcolor import cprint
import colorama

def uniform_dir_path(directory):
    '''
    Return directory path with '/' at the end

    Args:
        directory (str): directory path that you want to uniform

    Returns:
        directory (str): modified directory path that ends with '/'

    '''
    if directory.endswith('/') or directory.endswith('\\'):
        return directory
    else:
        return directory+'/'


def check_format_files(path_dir, img_format):
    '''
    Checks if there is at least one file with img_format extension
    in the folder specified by path_dir
    '''
    #List all the elements in path_dir
    files = os.listdir(path_dir)
    
    check_format = False

    #Checks if there is at least a file with img_format
    for f in files:
        if f.endswith('.'+img_format):
            check_format = True
        else:
            files.remove(f)

    return check_format, files


def create_pdf(input_path, output_path, subfolder_name, files):
    '''
    Create the pdf file using the images with specified
    names in files
    '''
    path_images = input_path

    #If recursive, the folder with images is 'path/subfolder_name'
    if subfolder_name!='':
        path_images = input_path+subfolder_name+'/'

    #List of tuples, one for each image (img, width, height)
    imgs_list = []
    #Find max size
    max_width = 0
    max_height = 0

    for img_name in files:
        with Image.open(path_images+img_name) as img:
            width, height = img.size

            if max_width < width:
                max_width = width
            if max_height < height:
                max_height = height

            imgs_list.append((path_images+img_name, width, height))

    #Create pdf
    pdf = fpdf.FPDF(unit='pt', format=(max_width, max_height))

    #Add images to pdf
    for (path, width, height) in imgs_list:
        pdf.add_page()
        pdf.image(path, 0, 0, width, height)

    #Save the pdf with the name of the folder with images
    if subfolder_name!='':
        pdf.output(output_path+subfolder_name+'.pdf', 'F')
    else:
        pdf.output(output_path+os.path.basename(input_path[:-1])+'.pdf', 'F')        


def convertion(input_path, output_path, recursive, img_format):
    '''
    Convertion of images in path with extension img_format
    '''

    if recursive:
        #List all the elements of the input_path
        subfolders = os.listdir(input_path)

        #No subfolders (input_path empty)
        if not subfolders:
            print('RECURSIVE ERROR: no subfolders in specified directory')
            exit(0)

        #For each element of the folder
        for f in subfolders:
            cprint(input_path+f, 'red', attrs=['bold',])

            #If the element is a subfolder
            if os.path.isdir(input_path+f):
                #Check if the subfolder has element with img_format
                check, files = check_format_files(input_path+f, img_format)
                #If so, create a pdf using all the images inside it
                if check:
                    print(files)
                    create_pdf(input_path, output_path, f, files)
    
    else:
        #Check if the folder has element with img_format
        check, files = check_format_files(input_path, img_format)
        #If so, create a pdf using all the images inside it
        if check:
            create_pdf(input_path, output_path, '', files)


def args_parser():
    '''
    Parser of command line arguments
    '''
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-input", "-i", 
                        dest="input", 
                        help="Path of directory with images or subfolders of images")

    parser.add_argument("-output", "-o", 
                        dest="output", 
                        help="""Path of the output folder where pdf files will be
                                stored (by default path specified in -dir option)""")    

    parser.add_argument("-format", "-f", 
                        dest="format", 
                        help="Format of images")
    
    parser.add_argument("-recursive", "-r", 
                        dest="recursive", 
                        help="Transformation of images to pdf for each subfolder", 
                        action='store_true')

    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the input path has been specified
    if not args.input:
        cprint('\n\n[MISSING DIRECTORY]', 'blue', end=' ')
        print('Missing path in -i option', end='\n\n')
        parser.print_help()
        print('\n')
        exit(0)

    #Check if the input path is a directory 
    if not os.path.isdir(args.input):
        cprint('[NOT EXISTING DIRECTORY]', 'blue', end=' ')
        print('The path', end=' ')
        cprint(f'{args.input}', 'green', end=' ')
        print(', specified in -i option, is not a directory', end='\n\n')
        parser.print_help()
        print('\n')
        exit(0)

    input_path = uniform_dir_path(args.input) 
    output_path = input_path

    #Check if the output path (not mandatory) is a directory 
    if  args.output:
        if not os.path.isdir(args.output):
            cprint('[NOT EXISTING DIRECTORY]', 'blue', end=' ')
            print('The path', end=' ')
            cprint(f'{args.output}', 'green', end=' ')
            print(', specified in -o option, is not a directory', end='\n\n')
            parser.print_help()
            print('\n')
            exit(0)
        else:
            output_path=uniform_dir_path(args.output)

    return input_path, output_path, args.recursive, args.format
        

def main():
    '''
    Main function.
    '''
    #Init colored print (otherwise powershell doesn't print colored string)
    colorama.init()
    #Argument parser
    input_path, output_path, recursive, img_format = args_parser()
    #Creation of PDF
    convertion(input_path, output_path, recursive, img_format)


if __name__=='__main__':
    main()