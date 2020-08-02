import pickle
import os
import shutil
from Log_Writer.log import logWriter

class Operation ():
    
    def __init__ (self):
        self.logWriter = logWriter
        self.modelsDirPath = 'Models'
    
    # Save the model 
    def saveModel (self, model, dirName, fileName):
        try:
            path = os.path.join(self.modelsDirPath, dirName)
        
            if os.path.isdir(path):
                shutil.rmtree(path)
                os.makedirs(path)
            
            if not os.path.isdir(path):
                os.makedirs(path)
                
            file = open(f'{self.modelsDirPath}/{dirName}/{fileName}.pkl', 'wb')
            pickle.dump(model, file)
            with open('Training_Logs/model_training.txt', 'a+') as f:
                self.logWriter(f, 'Model has been saved successfully.')
                
        except Exception as e:
            with open('Training_Logs/model_training.txt', 'a+') as f:
                self.logWriter(f, 'Something went wrong while saving the model.')
            raise e
    
    def loadModel (self, dirName, fileName):
        try:
            file = open(f'{self.modelsDirPath}/{dirName}/{fileName}.pkl', 'rb')
            loadedFile = pickle.load(file)
            
            with open('Training_Logs/model_training.txt', 'a+') as f:
                self.logWriter(f, 'Model has been loaded successfully.')
                
            return loadedFile
        
        except Exception as e:
            with open('Training_Logs/model_training.txt', 'a+') as f:
                self.logWriter(f, 'Something went wrong while loading  the model.')
            raise e
    
    def findModel (self, clusterLabel):
        try:
            modelFolders= [name for name in os.listdir(self.modelsDirPath) if os.path.isdir(f'{self.modelsDirPath}/{name}')]
            for folderName in modelFolders:
                intoList = folderName.split('_')
                if len(intoList) == 2 and clusterLabel == int(intoList[1]):
                    modelFolderName = '_'.join(intoList)
                    return modelFolderName
            with open('Training_Logs/model_training.txt', 'a+') as f:
                self.logWriter(f, 'Model has been loaded successfully.')
            
        except Exception as e:
            with open('Training_Logs/model_training.txt', 'a+') as f:
                self.logWriter(f, 'Something went wrong while loading  the model.')
            raise e