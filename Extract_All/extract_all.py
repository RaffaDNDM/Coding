import sys
import os
import argparse
import zipfile
import progressbar
from termcolor import cprint

'''
Parser of command line arguments
'''
def args_parser():

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-input", "-i", dest="input", help="Path the contains all the archieves to be extracted")
    parser.add_argument("-format", "-f", dest="format", help="Compression format (zip, rar, 7z, jar or tar)")
    parser.add_argument("-output", "-o", dest="output", help="Path the will contain extracted folders (by default input path)")

    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    if not args.input or not os.path.isdir(args.input) or not args.format:
        parser.print_help()
        exit(0)

    #Output folder
    output = ''
    if args.output:
        output = args.output
    else:
        output = args.input

    return args.input, output, args.format


'''
Extract all archieves in the input path with arch_format extension
'''
def zip_extraction(input_path, output_path, files, arch_format):
    count = 0
    #Progress Bar
    bar = progressbar.ProgressBar(maxval=20, \
                                  widgets=[progressbar.Bar('=', '[', ']'), ' ', \
                                  progressbar.Percentage()])
    bar.start()
    
    for f in files:
        #An output subfolder for each archieve
        output_subfolder = output_path+'/'+os.path.splitext(f)[0]
        #If output subfolder doesn't exist
        if not os.path.isdir(output_subfolder):
            os.mkdir(output_subfolder)
        #Archieve from its name
        archieve = zipfile.ZipFile(input_path+'/'+f)

        try:
            #Extract all files in the archieve in output path
            archieve.extractall(output_subfolder)
        except (zipfile.BadZipFile, UnicodeDecodeError):
            #Corrupted zip archieve or there is some corrupted file in it
            continue

        #Close the archieve
        archieve.close()
        #Completed extraction
        count = count +1
        #Update progress Bar
        bar.update(int(count/len(files) * 20))

    bar.finish()

'''
Extraction of archieves with arch_format extension in 
input_path to output_path 
'''
def extraction(input_path, output_path, arch_format):
    #Names of archieve files with extension
    files = [x  for x in os.listdir(input_path) if x.endswith(arch_format)]
    #No existing files in input_path with extension arch_format
    if not files:
        print('There are no files with format '+arch_format)
        exit(0)
    
    #Extraction depending on type of compression
    if arch_format == 'zip':
        zip_extraction(input_path, output_path, files, arch_format)
    else:
        print('Format unknown')
        exit(0)

'''
Main function.
'''
def main():
    #Argument parser
    input_path, output_path, arch_format = args_parser()
    #Creation of PDF
    extraction(input_path, output_path, arch_format)


if __name__=='__main__':
    main()