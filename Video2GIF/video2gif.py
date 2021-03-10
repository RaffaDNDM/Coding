from moviepy.editor import VideoFileClip
import argparse
from termcolor import cprint

def video2gif(video_path, gif_path='output.gif'):
    '''
    Convert video to gif

    Args:
        video_path (str): Path of the input video file to be converted

        gif_path (str): Path of the output GIF file 
                        (including the name of the GIF file)
    '''

    video = VideoFileClip(video_path)
    video.write_gif(gif_path)

def args_parser():
    '''
    Parser of command line arguments
    '''

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-input", "-i", '-video', '-v', dest="input", help="Path of the existing video file to be converted.")
    parser.add_argument("-gif", dest="gif", help="Path of the output GIF file (output.gif by default).")

    #Parse command line arguments
    args = parser.parse_args()

    if not args.input:
        cprint('You need to specify the input video path', 'red')
        exit()

    return args.input, args.gif

def main():
    video_path, gif_path = args_parser()
    
    if not gif_path:
        video2gif(video_path)
    else:
        video2gif(video_path, gif_path)

if __name__=='__main__':
    main()