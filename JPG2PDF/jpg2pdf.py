import fpdf
import argparse
import os
from PIL import Image

'''
Checks if there is at least one file with img_format extension
in the folder specified by path_dir
'''
def check_format_files(path_dir, img_format):
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


'''
Creates the pdf file using the images with specified
names in files
'''
def create_pdf(path, subfolder_name, files):
    path_images = path

    #If recursive, the folder with images is 'path/subfolder_name'
    if subfolder_name!='':
        path_images = path+'/'+subfolder_name

    #Obtain size of first image (equal to other images sizes)
    with Image.open(path_images+'/'+files[0]) as first_img:
        width, height = first_img.size

    #Create pdf with size of images
    pdf = fpdf.FPDF(unit='pt', format=(width, height))

    #Add one image for each page of the PDF
    for image in files:
        pdf.add_page()
        pdf.image(path_images+'/'+image,0,0)

    #Save the pdf with the name of the folder with images
    if subfolder_name!='':
        pdf.output(path+'/'+subfolder_name+'.pdf', 'F')
    else:
        pdf.output(path+'/'+os.path.basename(path)+'.pdf', 'F')        


'''
Parser of command line arguments
'''
def args_parser():

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-dir", "-d", dest="dir", help="Path of directory with images or subfolders of images")
    parser.add_argument("-format", "-f", dest="format", help="Format of images")
    parser.add_argument("-recursive", "-r", dest="recursive", help="Transformation of images to pdf for each subfolder", action='store_true')

    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    if not args.dir or not os.path.isdir(args.dir):
        parser.print_help()
        exit(0)

    return args.dir, args.recursive, args.format


def convertion(path, recursive, img_format):

    if recursive:
        #List all the elements of the path
        subfolders = os.listdir(path)

        #No subfolders (path empty)
        if not subfolders:
            print('RECURSIVE ERROR: no subfolders in specified directory')
            exit(0)

        #For each element of the folder
        for f in subfolders:
            print(path+'/'+f)

            #If the element is a subfolder
            if os.path.isdir(path+'/'+f):
                #Check if the subfolder has element with img_format
                check, files = check_format_files(path+'/'+f, img_format)
                #If so, create a pdf using all the images inside it
                if check:
                    print(files)
                    create_pdf(path, f, files)
    
    else:
        #Check if the folder has element with img_format
        check, files = check_format_files(path, img_format)
        #If so, create a pdf using all the images inside it
        if check:
            create_pdf(path, '', files)
        

def main():
    #Argument parser
    path, recursive, img_format = args_parser()
    #Creation of PDF
    convertion(path, recursive, img_format)


if __name__=='__main__':
    main()