import os
import argparse

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

def args_parser():
    '''
    Parser of command line arguments
    '''

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-input", "-i", dest="input", help="Path the contains files (e.g. 1.jpg) to be ordered")
    parser.add_argument("-format", "-f", dest="format", help="Extension of the files (e.g. jpg)")
    parser.add_argument("-recursive", "-r", 
                    dest="recursive", 
                    help="Rename of files in subfolders of each folder", 
                    action='store_true')

    #Parse command line arguments
    args = parser.parse_args()
    
    #Check if the arguments have been specified on command line
    if not args.input or not os.path.isdir(args.input) or not args.format:
        parser.print_help()
        exit(0)

    return uniform_dir_path(args.input), args.format, args.recursive


def rename(input_path, file_format, recursive):
    zero = '0'
    
    if recursive:
        subfolders_list = [x for x in os.listdir(input_path) if os.path.isdir(input_path+x)]
        print(subfolders_list)

        for subfolder in subfolders_list:
            files = [x[:-len(file_format)-1] for x in os.listdir(input_path+subfolder) if x.endswith('.'+file_format)]
            #print(files)
            if len(files) >= 100:
                for x in files:
                    if int(x) < 100 and len(x) == 2:
                        os.rename(input_path+subfolder+'/'+x+'.'+file_format,
                            input_path+subfolder+'/'+zero+x+'.'+file_format)
                    else:
                        continue
    else:
        files = [x[:-len(file_format)-1] for x in os.listdir(input_path) if x.endswith('.'+file_format)]

        if len(files) >= 100:
            for x in files:
                if int(x) < 100 and len(x) == 2:
                    os.rename(input_path+'/'+x+'.'+file_format,
                        input_path+'/'+zero+x+'.'+file_format)
                else:
                    continue

'''
Main function.
'''
def main():
    #Argument parser
    input_path, file_format, recursive = args_parser()
    #Creation of PDF
    rename(input_path, file_format, recursive)


if __name__=='__main__':
    main()