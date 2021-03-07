from pytube import YouTube
from termcolor import cprint, colored
import sys
import os

class YoutubeDownloader:
    def __init__(self, links):
        self.links = links

    def select_type(self):
        while True:
            cprint('Select the type of download you want to perform', 'blue')
            print(colored('0) ', 'green')+'Only audio')
            print(colored('1) ', 'green')+'Only video')
            print(colored('2) ', 'green')+'Both audio and video')

            cprint('_______________________________________________', 'blue')
            try:
                choice = int(input())
                cprint('_______________________________________________', 'blue')            
            
                if choice >=0 and choice < 3:
                    return choice

            except:
                pass

    def read_path(self):
        download_path = 'a'

        while not os.path.isdir(download_path):        
            cprint('Select the type of download you want to perform', 'blue')
            cprint('_______________________________________________', 'blue')
            download_path = input()
            cprint('_______________________________________________', 'blue')

        return download_path

    def download(self):
        choice = self.select_type()
        download_path = self.read_path()

        for link in self.links:
            try:            
                yt = YouTube(link)
                '''
                #Title of video
                print('Title: ', yt.title)
                #Number of views of video
                print('Number of views: ', yt.views)
                #Length of the video
                print('Length of video: ', yt.length, 'seconds')
                #Description of video
                print('Description: ', yt.description)
                #Rating
                print('Ratings: ', yt.rating)    
                '''

                ys = None

                if choice == 0:
                    ys = yt.streams.get_highest_resolution()
                elif choice == 1:
                    ys = yt.streams.filter(only_audio=True).get_highest_resolution()
                elif choice == 2:
                    ys = yt.streams.filter(only_video=True).get_highest_resolution()

                ys.download(download_path)
            except Exception as e:  
                print(e) 

def main():
    if len(sys.argv) < 2:
        print('You need to specify the links of the videos that you want to download')
        exit(0)

    downloader = YoutubeDownloader(sys.argv[1:])
    downloader.download()

if __name__=='__main__':
    main()