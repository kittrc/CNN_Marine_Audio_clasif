# Audio signal recognition model training- FMCC
## by Ruwan Abeywardhana. start on Feb-2022

# walk through audio file : to search for audio files in data folder # get file names
    # calculate FMCC
    # save FMCC data into .json file:  
     

        
##### setup

import json
import codecs
import numpy as np


##### import data

def ImportMfccData(pathMfccSave):
    objDataRead = codecs.open(pathMfccSave, 'r', encoding='utf-8').read()
    Rdata = json.loads(objDataRead)
    
    RX = np.array(Rdata['X'])
    RY = np.array(Rdata['Y'])
    Rmapping = Rdata['mapping']
    return RX,RY,Rmapping

pathMfccSave ='fmcc_marine_mamal.json'
X,Y,mapping = ImportMfccData(pathMfccSave)

# # for debugging
# print('data importing completed')
# print(np.unique(Y, return_counts=True))
# print(X.shape)


##### prepare data

from sklearn.model_selection import train_test_split
test_size = 0.25
validation_size = 0.2
def prepareData (X, Y, test_size, validation_size):
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size)
    X_train, X_validation, y_train, y_validation = train_test_split(X_train, y_train, test_size=validation_size)
        
    X_train = X_train[..., np.newaxis] 
    X_validation = X_validation[..., np.newaxis] 
    X_test = X_test[..., np.newaxis] 

    return X_train, X_validation, X_test, y_train, y_validation, y_test

X_train, X_validation, X_test, y_train, y_validation, y_test = prepareData (X, Y, test_size, validation_size)

