import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from Log_Writer.log import logWriter
from File_Operations.methods import Operation


class DataClustering ():
    
    def __init__ (self):
        self.logWriter = logWriter
        self.fileOperation = Operation()
    
    def getOptimumNumberOfCluster (self, data):
        try:
            inertia = []
            for i in range (1, 11):
                k_means = KMeans(n_clusters=i, random_state=0)
                k_means.fit(data)
                inertia.append(k_means.inertia_)
            
            plt.plot(range(1,11), inertia)
            plt.title('Elbow Approach')
            plt.xlabel('Number of cluster')
            plt.ylabel('Inertia')
            plt.savefig('Data_Preprocessing/elow_plot.png')
            
            self.kn = KneeLocator(range(1, 11), inertia, curve='convex', direction='decreasing')
            
            with open('Data_Preprocessing_Logs/preprocessing_logs.txt', 'a+') as file:
                self.logWriter(file, f'The optimum number of clusters is: {self.kn.knee}')
                
            return self.kn.knee
        
        except Exception as e:
            with open('Data_Preprocessing_Logs/preprocessing_logs.txt', 'a+') as file:
                self.logWriter(file, f'Something went  wrong while  clustering data : {e}')
            raise e
            
    def performClustering (self, data, clusterNumber):
        try:
            k_means = KMeans(n_clusters=clusterNumber)
            y_k_means = k_means.fit_predict(data)
            
            self.fileOperation.saveModel(y_k_means, 'Cluster', 'model')
            
            data['cluster'] = y_k_means
            with open('Data_Preprocessing_Logs/preprocessing_logs.txt', 'a+') as file:
                self.logWriter(file, f'The data has been clustered successfuly.')
                
            return data 
        
        except Exception as e:
            
            with open('Data_Preprocessing_Logs/preprocessing_logs.txt', 'a+') as file:
                self.logWriter(file, f'Something went  wrong while  clustering data : {e}')
            raise e

