from email.mime import audio
import eyed3
import os
import shutil
import tkinter
from tkinter import filedialog
from termcolor import cprint

class AudioMP3:
    _mp3_folder=''

    AUDIO_INFO={
        "Title": "title",
        "Artist": "artist",
        "Album": "album",
        #"Album artist": "album-artist",
        "Track number": "track_num",
        #"Total track number": "track-total",
        #"Disc number": "disc-num",
        #"Total disc number": "disc-total",
        "Genre": "genre",
        #"Genre ID": "genre-id",
        #"Release year": "year",
        #"First comment that matches description and language.": "comment",
        "All comments that are matching description and language": "comments",
        "Lyrics": "lyrics",
        #"Relase date": "release-date",
        #"Original Relase date": "original-release-date",
        #"Recording date": "recording-date",
        #"Encoding date": "encoding-date",
        #"Tagging date": "tagging-date",
        #"Play count": "play-count",
        "Popularities": "popularities",
        "BPM": "bpm",
        "Publisher": "publisher",
        #"Unique File IDs": "ufids",
        #"User text frames": "texts",
        #"User URL frames": "user-urls",
        #"Artist URL": "artist-url",
        #"Audio source URL": "audio-source-url",
        #"Audio file URL": "audio-file-url",
        #"Internet radio URL": "internet-radio-url",
        #"Comercial URL": "commercial-url",
        #"Payment URL": "payment-url",
        #"Publisher URL": "publisher-url",
        #"Copyright URL": "copyright-url",
        #"Attached pictures (APIC)": "apic",
        #"Attached pictures URLs": "image-urls",
        #"Objects (GOBJ)": "gobj",
        "Privates": "privates",
        #"Music CD Identification": "mcdi",
        "Terms of Use": "terms_of_use"
    }

    def __init__(self, mp3_folder):
        self._mp3_folder = mp3_folder
        eyed3.log.setLevel("ERROR")

    def set_artist(self, artist):
        for f in os.listdir(self._mp3_folder):
            audiofile = eyed3.load(os.path.join(self._mp3_folder, f))    # no tag in this file, link returned False
            audiofile.tag.artist = artist
            audiofile.tag.save()

    def set_name(self, delimiter):
        for f in os.listdir(self._mp3_folder):
            if len(f.split(delimiter, 1))==2:
                os.rename(os.path.join(self._mp3_folder, f), os.path.join(self._mp3_folder, f.split(delimiter, 1)[1]))
                audiofile = eyed3.load(os.path.join(self._mp3_folder, f))
                audiofile.tag.title = f.split(delimiter, 1)[1]
                audiofile.tag.save()
        
    def get_info(self):
        for f in os.listdir(self._mp3_folder):
            audiofile = eyed3.load(os.path.join(self._mp3_folder, f))
            cprint(f, 'yellow')
            for k in self.AUDIO_INFO:
                try:
                    info = getattr(audiofile.tag, self.AUDIO_INFO[k])
                    if info:
                        cprint(f'{k}:', 'blue', end='\t')
                        print(info)
                except AttributeError:
                    print(f"[ERROR] {self.AUDIO_INFO[k]}")

            print("")

def main():
    artist='All That Remains'
    
    #Select folder with MP3 files
    tkinter.Tk().withdraw() # prevents an empty tkinter window from appearing
    mp3_folder = filedialog.askdirectory(title="Folder with MP3 files to be analysed")
    
    audio = AudioMP3(mp3_folder)
    audio.get_info()  
    #audio.set_artist(artist)
    #audio.set_name(delimiter=' - ')
    
if __name__=='__main__':
    main()
