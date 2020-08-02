from Data_Preprocessing.preprocessing import DataPreprocessing
from Data_Preprocessing.clustering import DataClustering
from Training_Models.experimentation import FindBestModels
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from Log_Writer.log import logWriter
from File_Operations.methods import Operation
import pandas as pd



class TrainingModels ():
    
    def __init__ (self):
        self.dataprocessing = DataPreprocessing()
        self.dataClustering = DataClustering()
        self.findBestModel = FindBestModels()
        self.logWriter = logWriter
        self.fileOperation = Operation()
    
    #get data ready for ML model
    def prepareData (self):
        try:
            # c is the list of column to be moved due multi collinarity. Please have a look in EDA section.
            columnsToBeDeleted =['wetbulbtempf','dewpointtempf','stationpressure']
            X, y = self.dataprocessing.preprocess('Data_From_Db/training_set.csv', columnsToBeDeleted, 'visibility')
            
            numberOfCluster = self.dataClustering.getOptimumNumberOfCluster(X)
            dataClustered = self.dataClustering.performClustering(X, numberOfCluster)
            dataClustered['visiblity'] = y
            uniqueListOfClusterLabels = dataClustered['cluster'].unique()
            
            with open('Training_Logs/model_training_logs.txt', 'a+') as file:
                self.logWriter(file, f'Data is ready to be passed to a ML model.')
            
            return dataClustered, uniqueListOfClusterLabels
            
        except Exception as e:
            with open('Training_Logs/model_training_logs.txt', 'a+') as file:
                self.logWriter(file, f'Something went wrong while getting data ready for a ML model: {e}')
            raise e
            
    #Run all training process
    def run (self):
        try:
            dataClustered, uniqueListOfClusterLabels = self.prepareData()
            
            # for each cluster we perform experimentation, find best model, train it then evaluate on test data and save the model.
            for i in uniqueListOfClusterLabels:
                data = dataClustered[dataClustered['cluster'] == i]
                cluster_features = data.drop(['cluster', 'visiblity'], axis=1)
                cluster_label = data['visiblity']
                X_train, X_test, y_train, y_test = train_test_split(cluster_features, cluster_label, test_size=.2, random_state=42)
                # get promissing model
                promising_model = self.findBestModel.experimentations(X_train, y_train, 10, 'neg_mean_squared_error')
                
                # find best model after some hyper parametrs tuning
                best_model = self.findBestModel.hyperparametersTuning(promising_model, X_train, y_train, 5)
                # Finally, train the best model,
                name, _ = [(name, _) for name, _ in promising_model.items()][0]
                modelDirName = name + '_' + str(i)
                
                model = self.findBestModel.trainAndEvaluateBestModel(best_model, X_train, y_train)
                #make prediction on testsets
                y_pred = model.predict(X_test)
                
                # save model
                self.fileOperation.saveModel(model, modelDirName, modelDirName.lower())
                
                # create an csv file for model  evaluation on test set.
                df = pd.DataFrame()
                df['True Values'] = y_test
                df['Predict Values'] = y_pred
                df['Prediction Errors'] = y_test - y_pred 
                # Mean Squared, Error will be the same value in every row. 
                df['Mean Squared, Error'] = mean_squared_error(y_test, y_pred)
                df.to_csv(f'Models/{modelDirName}/evaluation.csv')
                
            with open('Training_Logs/model_training_logs.txt', 'a+') as file:
                self.logWriter(file, f'Model training has been completed successfully.')
                
        except Exception as e:
            with open('Training_Logs/model_training_logs.txt', 'a+') as file:
                self.logWriter(file, f'Something went wrong while training the model: {e}')
            raise e
    


    
