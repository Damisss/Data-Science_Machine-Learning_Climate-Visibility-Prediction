from Data_Preprocessing.preprocessing import DataPreprocessing
from Data_Preprocessing.clustering import DataClustering
from Training_Models.experimentation import FindBestModels
from sklearn.model_selection import train_test_split
from Log_Writer.log import logWriter
from File_Operations.methods import Operation
import matplotlib.pyplot as plt


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
            c =['wetbulbtempf','dewpointtempf','stationpressure']
            X, y = self.dataprocessing.preprocess('Training_Set_From_Db/training_set.csv', c, 'visibility')
            
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
                
                f, (ax1,ax2) = plt.subplots(1, 2, sharex=True )
                # histogram plot
                ax1.hist(y_test - y_pred)
                plt.xlabel('Visibility')
                # scatter plot
                ax2.scatter(y_test, y_pred)
                plt.xlabel('Actual Values')
                plt.ylabel('predict values')
                
                plt.savefig(f'Models/{modelDirName}/evalution_plot.png')
                # save model
                self.fileOperation.saveModel(model, modelDirName, modelDirName.lower())
                
            with open('Training_Logs/model_training_logs.txt', 'a+') as file:
                self.logWriter(file, f'Model training has been completed successfully.')
                
        except Exception as e:
            with open('Training_Logs/model_training_logs.txt', 'a+') as file:
                self.logWriter(file, f'Something went wrong while training the model: {e}')
            raise e
    


    
