#from scipy.io import wavfile
# import matplotlib.pyplot as plt
# import numpy as np
# import math
import pydub
from pydub import AudioSegment
from pydub.playback import play
import os 
# import csv


dataDir = './data/'
dataFolders = ['spotted_dolphin','BlueWhale001-v2' , 'BowheadWhale001-v1' ]

def readAudio(fileDir):
    audioList = []
    
    for file in os.listdir(fileDir):
        if file.endswith(fileFormat):
            # print(os.path.join (fileDir,file)) # for debugging
            audio = AudioSegment.from_file(os.path.join (fileDir,file)) 
            audioList.append(audio)
            
    return audioList


for folderName in dataFolders:
    audioList = readAudio(os.path.join (dataDir , folderName))
    # print(audioList[-1]) # for debugging

