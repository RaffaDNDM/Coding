import sys
import os
import argparse
import zipfile
import gzip
import tarfile
import py7zr
import progressbar
from termcolor import cprint
import colorama

'''
Parser of command line arguments
'''
def args_parser():
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-input", "-i", dest="input", help="Path the contains all the archieves to be extracted")
    parser.add_argument("-output", "-o", dest="output", help="Path the will contain extracted folders (by default input path)")

    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    if not args.input or not os.path.isdir(args.input):
        parser.print_help()
        exit(0)

    #Output folder
    output = ''
    if args.output:
        output = args.output
    else:
        output = args.input

    return args.input, output


'''
Extract an archieve looking to its extension
'''
def extract_file(input_filename, output_filename):
    #Archieve from its name
    if input_filename.endswith('.zip'):
        with zipfile.ZipFile(input_filename, 'r') as archieve:
            try:
                #Extract all files in the archieve in output path
                archieve.extractall(output_filename)
            except (zipfile.BadZipFile, UnicodeDecodeError):
                return

    elif input_filename.endswith('.7z'):
        with py7zr.SevenZipFile(input_filename, mode='r') as archieve:
            archieve.extractall(path=output_filename)

    elif input_filename.endswith('.tar'):
        with tarfile.open(input_filename, 'r') as archieve:
            archieve.extractall(output_filename)

    elif input_filename.endswith('.tar.gz') or input_filename.endswith('.tgz'):
        with tarfile.open(input_filename, 'r:gz') as archieve:
            archieve.extractall(output_filename)

    elif input_filename.endswith('.tar.xz'):
        with tarfile.open(input_filename, 'r:xz') as archieve:
            archieve.extractall(output_filename)

    elif input_filename.endswith('.gz') and not input_filename.endswith('.tar.gz'):
        with open(output_filename, "wb") as out_f, gzip.GzipFile(input_filename) as archieve:
            out_f.write(archieve.read())

    else:
        print('Extension for ', end='')
        cprint('{input_filename}', 'red', end='')
        print(' unkown')


'''
Extract all archieves in the input path with arch_format extension
'''
def extract_from_dir(input_path, output_path, files):
    count = 0
    #Progress Bar
    bar = progressbar.ProgressBar(maxval=20, \
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', \
                                  progressbar.Percentage()])
    bar.start()
    
    for f in files:
        #An output subfolder for each archieve
        output_filename = output_path+'/'+os.path.splitext(f)[0]
        #If output subfolder doesn't exist
        if not os.path.isdir(output_filename):
            os.mkdir(output_filename)
        
        extract_file(input_path+'/'+f, output_filename)

        #Completed extraction
        count += 1
        #Update progress Bar
        bar.update(int(count/len(files) * 20))

    bar.finish()




'''
Extraction of archieves with in input_path to output_path 
'''
def extraction(input_path, output_path):
    files = [x for x in os.listdir(input_path) if os.path.isfile(input_path+'/'+x)]
    
    #No existing files in input_path with extension arch_format
    if not files:
        print('There are no files in input folder')
        exit(0)
    
    extract_from_dir(input_path, output_path, files)


'''
Main function.
'''
def main():
    #Init colored print (otherwise powershell doesn't print colored string)
    colorama.init()
    #Argument parser
    input_path, output_path = args_parser()
    #Creation of PDF
    extraction(input_path, output_path)


if __name__=='__main__':
    main()