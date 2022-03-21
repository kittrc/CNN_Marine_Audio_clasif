# Audio signal processing - FMCC
## by Ruwan Abeywardhana. start on Feb-2022

# walk through audio file : to search for audio files in data folder # get file names
    # calculate FMCC
    # save FMCC data into .json file:  
     

        
# setup
import os
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.signal import get_window
import scipy.fftpack as fft
import pandas as pd
from sklearn.preprocessing import OrdinalEncoder
import json

##### predefined parametere

dirData ='./Data'
windowTime = 15 # signal length in seconds
sizeFFT = 2048
num_MelPoints = 20 # number of frequancy windows in mel spectrogram
dctFilterNum = 40 

###### labeling and save data
def  encodeLable (dirData):
    labelY =[]
    for mammalName in os.listdir(dirData): 
        labelY.append(mammalName)

    labelY = pd.array(labelY)
    pdY = labelY.reshape((len(labelY), 1))
    oe = OrdinalEncoder()
    oe.fit(pdY)
    encY = oe.transform(pdY)
    mapping = { labelY[i]:int(encY[i]) for i in range(len(labelY))}
    return mapping

##### audio signal pre-processing

# extend short signals

def AudioNormalize( audio):
    audio = audio / np.max(np.abs(audio))
    return audio


# windowing 
def AudioWindow (audio, sizeFFT=2048, sizeHop=10, Fs=44100):
    
    audio = np.pad(audio, int(sizeFFT / 2), mode='reflect')
    lenFrame = np.round(Fs * sizeHop / 1000).astype(int)
    numFrame = int((len(audio) - sizeFFT) / lenFrame) + 1
    audioFrames = np.zeros((numFrame,sizeFFT))
    
    for n in range(numFrame):
        audioFrames[n] = audio[n*lenFrame:n*lenFrame+sizeFFT]
    
    window = get_window("hann", sizeFFT, fftbins=True)
    audioWindow = audioFrames * window

    # # for debuggingg
    # plt.plot(audioWindow[-1])

    return audioWindow
    
##### frequancy domain analize

# FFT calculation 
def AudioFFT(audioWindow,sizeFFT):
    audioFFT = np.empty(( audioWindow.shape[0],int(1 + sizeFFT // 2)), dtype=np.complex64, order='F')
    for n in range(audioWindow.shape[0]):
        audioFFT[n] = fft.fft(audioWindow[n], axis=0)[:audioFFT.shape[1]]
    audioFFT = np.abs(audioFFT)
    audioPower = np.square(audioFFT)
    return audioPower # audioFFT or audioPower as required

# mel frequancy

def freq_to_mel(freq):
    return 2595.0 * np.log10(1.0 + freq / 700.0)

def met_to_freq(mels):
    return 700.0 * (10.0**(mels / 2595.0) - 1.0)


def GetFilterPoints(frqMin, frqMax, num_MelPoints, sizeFFT, Fs):
    melMin = freq_to_mel(frqMin)
    melMax = freq_to_mel(frqMax)
    
    mels = np.linspace(melMin, melMax, num=num_MelPoints+2)
    freqs = met_to_freq(mels)
    
    return np.floor((sizeFFT + 1) / Fs * freqs).astype(int), freqs

# normalized filter(weigted maks) for each mel window
def GetFilters(melPoints, melFrq,sizeFFT):
    melFilters = np.zeros((len(melPoints)-2,int(1+sizeFFT/2)))
    
    # filter shap triangular
    for n in range(len(melPoints)-2):
        melFilters[n, melPoints[n] : melPoints[n + 1]] = np.linspace(0, 1, melPoints[n + 1] - melPoints[n]) # incline line or ramp shape
        melFilters[n, melPoints[n + 1] : melPoints[n + 2]] = np.linspace(1, 0, melPoints[n + 2] - melPoints[n + 1]) # decline or sawtooth
    
    enorm = 2.0 / (melFrq[2:len(melFrq)] - melFrq[:len(melFrq)-2])
    melFilters *= enorm[:, np.newaxis]
    return melFilters

# get mel spectrum
def MelSpecrum(audioWindow,sizeFFT,Fs):
    audioPower = AudioFFT(audioWindow,sizeFFT) # fft or fft-power
    melPoints, melFrq = GetFilterPoints(0, Fs/2, num_MelPoints, sizeFFT, Fs) 
    melFilters = GetFilters(melPoints, melFrq, sizeFFT)
    #
    audioFiltered = np.dot(melFilters, np.transpose(audioPower))
    melSpecrum = 10.0 * np.log10(audioFiltered)
    return melSpecrum
        

# DCT - Cepstral Coefficents

def Dct(dctFilterNum, filterLen):
    basis = np.empty((dctFilterNum,filterLen))
    basis[0, :] = 1.0 / np.sqrt(filterLen)
    
    samples = np.arange(1, 2 * filterLen, 2) * np.pi / (2.0 * filterLen)

    for i in range(1, dctFilterNum):
        basis[i, :] = np.cos(i * samples) * np.sqrt(2.0 / filterLen)
        
    return basis



#####  main programe


##### walk data folder
X = []
Y = []
mapping = encodeLable (dirData)


for mammalName in os.listdir(dirData): # every folder in data directory named after sea mamals 

    for audioFileName in os.listdir(os.path.join(dirData,mammalName)): # every wav audio files save in the directory
        audioFileDir = os.path.join(dirData , mammalName , audioFileName)
        Fs, audio = wavfile.read(audioFileDir) # import audio data

        ## pre-processing
        audio = AudioNormalize(audio)
        audioWindow = AudioWindow (audio, sizeFFT=sizeFFT, sizeHop=15, Fs=Fs)

        ## frequancy domain analize 
        # mel spectrogram
        melSpecrum = MelSpecrum(audioWindow,sizeFFT,Fs) 
        # FMCC
        dctFilters = Dct(dctFilterNum, num_MelPoints)
        mfcc = np.dot(dctFilters, melSpecrum)
        #
        chunkSize = int(1000//windowTime)
        higgLim = chunkSize*mfcc.shape[1]//chunkSize
        cutoffHigh = mfcc.shape[1]//chunkSize*chunkSize
        fmccReshaped = mfcc[:,0:cutoffHigh].reshape([dctFilterNum,chunkSize,mfcc.shape[1]//chunkSize])
        for i in range (fmccReshaped.shape[2]):
            X.append(fmccReshaped[:,:,i])
            Y.append(mapping[mammalName])
    

        
        # # for debugging
        # print(len(audio) / Fs)
        # print(mfcc.shape)
        # plt.figure(figsize=(15,4))
        # plt.plot(np.linspace(0, len(audio) / sample_rate, num=len(audio)), audio)
        # plt.grid(True)        


#### save data

import codecs
pathMfcSave ='fmcc_marine_mamal.json'
def mfccSaveToJson(pathMfcSave,X,Y,mapping):
    json.dump({'X' : np.array(X).tolist(),'Y' : np.array(Y).tolist(),'mapping' :mapping}, 
              codecs.open(pathMfcSave, 'w', encoding='utf-8'), 
              separators=(',', ':'), 
              sort_keys=True, 
              indent=4) 

mfccSaveToJson(pathMfcSave,X,Y,mapping)