import os
import argparse

'''
Parser of command line arguments
'''
def args_parser():
    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-input", "-i", dest="input", help="Path the contains files (e.g. 1.jpg) to be ordered")
    parser.add_argument("-format", "-f", dest="format", help="Extension of the files (e.g. jpg)")

    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    if not args.input or not os.path.isdir(args.input) or not args.format:
        parser.print_help()
        exit(0)

    return args.input, args.format


def num_order(input_path, file_format):
    files = [x[:-len(file_format)-1] for x in os.listdir(input_path) if x.endswith('.'+file_format)]
    zeros = '0'

    for x in files:
        if int(x) < 100:
            os.rename(input_path+'/'+x+'.'+file_format,
                  input_path+'/'+zeros+x+'.'+file_format)
        else:
            continue

'''
Main function.
'''
def main():
    #Argument parser
    input_path, file_format = args_parser()
    #Creation of PDF
    num_order(input_path, file_format)


if __name__=='__main__':
    main()