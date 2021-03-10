from pytube import YouTube
from termcolor import cprint, colored
import sys
import os

class YoutubeDownloader:
    '''
    Downloader of Youtube videos.

    Args:
        links (list): List of URLs of videos to be downloaded

    Attributes:
        LINKS (list): List of URLs of videos to be downloaded
    '''

    def __init__(self, links):
        self.LINKS = links

    def select_type(self):
        '''
        Select type of video to be downloaded

        Returns:
            choice (int): Option of download selected
                          0) Only audio
                          1) Only video
                          2) Both audio and video
        '''

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
        '''
        Read the path of the folder where the user wants to store 
        the downloaded videos (including the name of the file).

        Returns:
            download_path (str): path of the folders where the user 
                                 wants to store the downloaded videos
                                 (including the name of the file)
        '''

        download_path = 'a'

        while not os.path.isdir(download_path):        
            cprint('Select the path where the downloaded video will be', 'blue')
            cprint('_______________________________________________', 'blue')
            download_path = input()
            cprint('_______________________________________________', 'blue')

        return download_path

    def download(self):
        '''
            Download the videos related to all the specified links.
        '''

        #Select the type of download
        choice = self.select_type()
        #Select the folder where videos will be stored
        download_path = self.read_path()

        #Dowload all the videos
        for link in self.LINKS:
            try:            
                #Youtube object from the link
                yt = YouTube(link)
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

                ys = None

                #Select the best resolution available for the selected
                #type of download (audio, video, audio+video)
                if choice == 0:
                    ys = yt.streams.get_highest_resolution()
                elif choice == 1:
                    ys = yt.streams.filter(only_audio=True).get_highest_resolution()
                elif choice == 2:
                    ys = yt.streams.filter(only_video=True).get_highest_resolution()

                #Download the video
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