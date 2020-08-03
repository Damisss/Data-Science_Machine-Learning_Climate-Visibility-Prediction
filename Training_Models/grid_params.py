# One could create a simple dictionary e.g a ={}.

class GridParams ():
    
    def __init__ (self):
        #regressor__xgbregressor__
        
        self.svr = {'c':range(1, 10), 'gamma': [0.001, 0.005, 0.1, 0.5] }
        
        self.xgboost =  {'max_depth': [3, 4, 5, 6, 7, 8, 10],
                         'learning_rate': [0.01, 0.05, 0.1, 0.2],
                         'colsample_bytree': [0.6, 0.7, 0.8],
                         'min_child_weight': [0.4, 0.5, 0.6],
                         'gamma': [0.0, 0.01, 0.1],
                         'reg_lambda': range(2, 10, 2),
                         'n_estimators': [100, 150, 200, 250],
                         }
        
        
        self.gradientboost = {'n_estimators': [100, 150, 200, 250],
                              'learning_rate':[0.01, 0.05, 0.1, 0.2], 
                              'min_samples_leaf':[2, 3],  
                              'min_samples_split':[14], 
                              'max_features':[0.7, .1, .05]
                             }
        
        self.randomforest = {'n_estimators':[150, 300, 600], 
                             'min_samples_leaf':[2, 3],  
                             'min_samples_split':[14, 12], 
                             'max_features':[0.7, 1],
                            'criterion': ['mse', 'mae']}
        
        self.extratrees= {'n_estimators': [100, 150, 200, 250], 
                          'criterion': ['mse', 'mae'],
                          'max_depth': range(2, 9, 1), 
                          'max_features': ['auto','sqrt', 'log2']}
        
        self.kneighbors = {'regressor_algorithm':['auto', 'ball_tree', 'kd_tree'],
                           'leaf_size': range(5, 40, 3),
                           'metric':['minkowski', 'precomputed'],
                           'n_neighbors':range(2, 15, 1),
                           'p': [2, 3, 5]}
