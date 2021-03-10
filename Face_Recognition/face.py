import face_recognition
import argparse
from termcolor import cprint, colored
from cv2 import cv2 as cv
import os
import numpy as np

class FaceRecognition:
    '''
    Face recognition implementation.

    Args:
        real_time (bool): True if real time recognition, False otherwise

    Attributes:
        TRAIN_FOLDER (str): Path of the folder where there are images for 
                            non-real time application

        path_img (str): Path of the image
                        -> NO REAL TIME
                           in which you want to recognize a person from the set
                           of recognized faces of the images in TRAIN_FOLDER
                        -> REAL TIME
                           with the face you want to recognized in the webcam stream
    '''

    TRAIN_FOLDER = 'dat/'
    #List of encodings (one for each face in the image)
    
    def __init__(self, real_time):
        self.path_img = 'a'
        self.real_time = real_time

        while not os.path.isfile(self.path_img) and not self.path_img[-4:] == '.jpg':
            cprint('Print the path of the image in which you want to recognize the face', 'blue')
            cprint('___________________________________________________________________', 'blue')
            self.path_img = input()
            cprint('___________________________________________________________________', 'blue')

        if self.real_time:
            self.TRAIN_ENCODINGS = []
            train_img = face_recognition.load_image_file(self.path_img)
            self.TRAIN_ENCODINGS.append(face_recognition.face_encodings(train_img)[0])
            self.TRAIN_LABELS = os.path.basename(self.path_img)[:-4]        
        else:
            self.TRAIN_ENCODINGS = []
            self.TRAIN_LABELS = []    

            for f in os.listdir(self.TRAIN_FOLDER):
                train_img = face_recognition.load_image_file(self.TRAIN_FOLDER+f)
                #I take only the encoding of the first face found in train_img
                self.TRAIN_ENCODINGS.append(face_recognition.face_encodings(train_img)[0])
                self.TRAIN_LABELS.append(f[:-4])

    def recognize(self):
        '''
        Face recognition application.
        '''

        #Real time recognition
        if self.real_time:
            webcam = cv.VideoCapture(0)
            success = True
            i=0

            while success:
                success, frame = webcam.read()

                if not success:
                    continue

                #Reduce size of each webcam frame
                small_frame = cv.resize(frame, None, fx=0.5, fy=0.5)
                #Convert frame from BGR to RGB
                rgb_small_frame = cv.cvtColor(small_frame, cv.COLOR_BGR2RGB)
                #Find the location of the face in the image
                face_locations = face_recognition.face_locations(rgb_small_frame)
                #Encode the recognized face
                frame_encodings = face_recognition.face_encodings(rgb_small_frame)

                if frame_encodings:
                    #Compare the face in the frame with the face in the img specified
                    results = face_recognition.compare_faces(self.TRAIN_ENCODINGS, frame_encodings[0])
                    
                    if results[0]:
                        #Draw green rectangle with name of person around 
                        #the face if there is a match
                        if face_locations:
                            top, right, bottom, left = face_locations[0]
                            cv.rectangle(small_frame, (left, top), (right, bottom), (0, 255, 0), 2)
                            cv.rectangle(small_frame, (left, bottom-10), (right, bottom), (0, 255, 0), cv.FILLED)
                            cv.putText(small_frame, self.TRAIN_LABELS, (left+2, bottom-2), cv.FONT_HERSHEY_COMPLEX, 0.2, (0,0,0))
                    else:
                        #Draw red rectangle around the face if there isn't a match
                        if face_locations:
                            top, right, bottom, left = face_locations[0]
                            cv.rectangle(small_frame, (left, top), (right, bottom), (0, 0, 255), 2)
                
                cv.imshow('Webcam video', small_frame)

                if cv.waitKey(1) & 0xFF == ord('q'):
                    break                

        #No real time recognition
        else:
            unknown_img = face_recognition.load_image_file(self.path_img)
            unknown_encoding = face_recognition.face_encodings(unknown_img)[0]

            #Compare a list of encodings of different imgaes with the encoding of new image
            #comparison_results[i]=True if the if face_distance < tolerance
            #(tolerance parameter of compare_faces is 0.6 by default)
            comparison_results = face_recognition.compare_faces(self.TRAIN_ENCODINGS, unknown_encoding)

            max_match = 0.0
            max_index = 0

            #For each match I print e results (lower number -> better match)
            if comparison_results:
                for i in range(len(comparison_results)):
                    if comparison_results[i]:
                        #Match percentage (100% if perfect match)
                        percentage = (1.0 -face_recognition.face_distance([self.TRAIN_ENCODINGS[i]], unknown_encoding))* 100.0
                        
                        if max_match < percentage:
                            max_match = percentage
                            max_index = i

                        print(colored(f'{self.TRAIN_LABELS[i]}','yellow'),f': {percentage}')
            else:
                cprint('\nNO MATCH', 'red')

            print(colored('\nBEST MATCH: ', 'red'),self.TRAIN_LABELS[max_index])


def args_parser():
    '''
    Parser of command line arguments
    '''

    #Parser of command line arguments
    parser = argparse.ArgumentParser()
    
    #Initialization of needed arguments
    parser.add_argument("-real", "-r", dest="real_time", help="If specified, real-time approach is applied using webcam.", action='store_true')

    #Parse command line arguments
    args = parser.parse_args()

    return args.real_time

def main():
    real_time = args_parser()
    fr = FaceRecognition(real_time)
    fr.recognize()

if __name__=='__main__':
    main()